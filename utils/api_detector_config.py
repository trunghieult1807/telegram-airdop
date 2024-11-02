from typing import Set, Dict
from pydantic import BaseModel


class ApiDetectorConfig(BaseModel):
    app_url: str
    target_apis: Set[str] = {}
    ignore_js_scripts: Set[str] = {}
    headers: Dict[str, str] = {}
    headers_js: Dict[str, str] = {}
