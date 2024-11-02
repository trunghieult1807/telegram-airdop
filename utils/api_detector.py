import os
import re
import json
import requests
from bs4 import BeautifulSoup
from furl import furl

DATA_DIR = 'api_data'

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def fetch_page_html(url, headers=None):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def extract_js_files(html, ignore_js_scripts=set()):
    soup = BeautifulSoup(html, 'html.parser')
    scripts = [script['src'] for script in soup.find_all('script') if script.get('src') and script['src'] not in ignore_js_scripts]
    return scripts

def extract_api_endpoints(js_content, api_list=[]):
    api_patterns = [
        (
            r'\b[a-zA-Z0-9_$]+\.(?:get|post|put|delete|patch|request|fetch)\(\s*'  # Matches method calls
            r'(?:["\']([^"\']+)["\']|`([^`]+)`)'  # Matches static strings or template literals
            r'(?:\s*,\s*{[^}]*})?\s*\)'  # Matches optional object arguments
        ),
        # r'https?://[^\s"\']+',
    ]
    
    endpoints = set()
    for api_pattern in api_patterns:    
        matches = re.findall(api_pattern, js_content)
        for match in matches:
            endpoints.add(match[0] if match[0] else match[1])
    for api in api_list:
        if api in js_content:
            endpoints.add(api)
            
    endpoints = list(endpoints)
    endpoints.sort()
    return endpoints

def clean_url(url):
    strip_interpolation = re.sub(r'\$\{[^}]+\}', '', url)
    normalized_url = furl(strip_interpolation).remove(query=True)
    normalized_url.path.normalize()
    return normalized_url.url

def check_invalid_apis(target_apis, valid_apis):
    cleaned_apis = set(clean_url(url) for url in valid_apis)
    invalid_apis = []
    for api in target_apis:
        if clean_url(api) not in cleaned_apis:
            invalid_apis.append(api)
    return invalid_apis

def save_api_data(api_data, filename):
    with open(filename, 'w') as f:
        json.dump(api_data, f, indent=2)

def load_api_data(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, 'r') as f:
        return json.load(f)

class ApiDetector:
    def __init__(self, app_name, app_url, target_apis=set(), ignore_js_scripts=set(), headers=None, headerjs=None):
        api_path = os.path.join(DATA_DIR, app_name)
        if not os.path.exists(api_path):
            os.makedirs(api_path)
        self.api_path = api_path
        self.app_name = app_name
        self.app_url = app_url
        self.target_apis = target_apis
        self.ignore_js_scripts = ignore_js_scripts
        self.headers = headers
        self.headerjs = headerjs
        
        # Properties
        self.analyzed_api_file = os.path.join(DATA_DIR, self.app_name, 'api_data.json')
        self.new_analyzed_api_file = os.path.join(DATA_DIR, self.app_name, 'api_data.new.json')
        self.invalid_apis_file = os.path.join(DATA_DIR, self.app_name, 'invalid_apis.json')
        
    def crawl_api_usage(self):
        html = fetch_page_html(self.app_url, self.headers)
        js_files = extract_js_files(html, self.ignore_js_scripts)
        api_data = {}
        for js_file in js_files:
            try:
                js_url = js_file if js_file.startswith('http') else requests.compat.urljoin(self.app_url, js_file)
                response = requests.get(js_url, headers=self.headerjs)
                response.raise_for_status()
                content = response.text
                endpoints = extract_api_endpoints(content, self.target_apis)
                api_data[js_file] = endpoints
            except requests.exceptions.RequestException as e:
                api_data[js_file] = f"Failed to download {e}"
                
        return api_data
    
    def first_time_check(self):
        return not os.path.exists(self.analyzed_api_file)
    
    def check_api(self):
        old_js_api_calls = load_api_data(self.analyzed_api_file)
        valid_apis = [url for urls in old_js_api_calls.values() for url in urls]
        invalid_apis = check_invalid_apis(self.target_apis, valid_apis)
        
        if len(invalid_apis) > 0:
            js_api_calls = self.crawl_api_usage()
            save_api_data(invalid_apis, self.invalid_apis_file)
            save_api_data(js_api_calls, self.new_analyzed_api_file)
            return False
        
        return True
    
    def init_api_data(self):
        js_api_calls = self.crawl_api_usage()
        save_api_data(js_api_calls, self.new_analyzed_api_file)
    
    def mark_safe(self):
        if not os.path.exists(self.new_analyzed_api_file):
            return True
        
        js_api_calls = load_api_data(self.new_analyzed_api_file)
        valid_apis = [url for urls in js_api_calls.values() for url in urls]
        invalid_apis = check_invalid_apis(self.target_apis, valid_apis)
        
        if len(invalid_apis) > 0:
            return False
        
        if os.path.exists(self.analyzed_api_file):
            os.remove(self.analyzed_api_file)
        if os.path.exists(self.invalid_apis_file):
            os.remove(self.invalid_apis_file)
        os.rename(self.new_analyzed_api_file, self.analyzed_api_file)
        
        return True
