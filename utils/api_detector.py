import os
import re
import json
import requests
from bs4 import BeautifulSoup

DATA_DIR = 'api_data'

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def fetch_page_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_js_files(html, ignore_js_scripts=set()):
    soup = BeautifulSoup(html, 'html.parser')
    scripts = [script['src'] for script in soup.find_all('script') if script.get('src') and script['src'] not in ignore_js_scripts]
    return scripts

def extract_api_endpoints(js_content):
    api_pattern = (
        r'\b[a-zA-Z0-9_$]+\.(?:get|post|put|delete|patch|request|fetch)\(\s*'  # Matches method calls
        r'(?:["\']([^"\']+)["\']|`([^`]+)`)'  # Matches static strings or template literals
        r'(?:\s*,\s*{[^}]*})?\s*\)'  # Matches optional object arguments
    )
    matches = re.findall(api_pattern, js_content)
    endpoints = [
        match[0] if match[0] else match[1]
        for match in matches
    ]
    endpoints.sort()
    return endpoints

def clean_url(url):
    url = url.split('?')[0]
    url = re.sub(r'\$\{.*?\}', '', url)
    url = re.sub(r'//+', '/', url)
    return url

def save_api_data(api_data, filename):
    with open(filename, 'w') as f:
        json.dump(api_data, f, indent=2)

def load_api_data(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, 'r') as f:
        return json.load(f)

class ApiDetector:
    def __init__(self, app_name, app_url, target_apis=set(), ignore_js_scripts=set()):
        api_path = os.path.join(DATA_DIR, app_name)
        if not os.path.exists(api_path):
            os.makedirs(api_path)
            
        self.api_path = api_path
        self.app_name = app_name
        self.app_url = app_url
        self.target_apis = target_apis
        self.ignore_js_scripts = ignore_js_scripts
        
    def verify_apis(self, js_api_calls):
        cleaned_urls = set(clean_url(url) for urls in js_api_calls.values() for url in urls)
        changed_apis = []
        for api in self.target_apis:
            if api not in cleaned_urls:
                changed_apis.append(api)
        return changed_apis
    
    def crawl_api_usage(self):
        html = fetch_page_html(self.app_url)
        js_files = extract_js_files(html, self.ignore_js_scripts)
        api_data = {}
        for js_file in js_files:
            try:
                js_url = js_file if js_file.startswith('http') else requests.compat.urljoin(self.app_url, js_file)
                response = requests.get(js_url)
                response.raise_for_status()
                content = response.text
                endpoints = extract_api_endpoints(content)
                api_data[js_file] = endpoints
            except requests.exceptions.RequestException as e:
                api_data[js_file] = f"Failed to download {e}"
                
        return api_data
    
    def check_api(self):
        old_js_api_calls = load_api_data(os.path.join(DATA_DIR, self.app_name, "api_data.json"))
        invalid_apis = self.verify_apis(old_js_api_calls)
        if len(invalid_apis) > 0:
            js_api_calls = self.crawl_api_usage()
            save_api_data(js_api_calls, os.path.join(DATA_DIR, self.app_name, "api_data.new.json"))
            return False
        return True
