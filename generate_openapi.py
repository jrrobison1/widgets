#!/usr/bin/env python3
"""Generate OpenAPI spec"""

import json
from src.widgets.main import app

def generate_openapi_spec():
    """Generate and save OpenAPI spec"""
    openapi_spec = app.openapi()
    
    with open("openapi.json", "w") as f:
        json.dump(openapi_spec, f, indent=2)
    
    print("OpenAPI specification generated: openapi.json")
    print(f"Title: {openapi_spec['info']['title']}")
    print(f"Version: {openapi_spec['info']['version']}")
    print(f"Endpoints: {len(openapi_spec['paths'])} paths")

if __name__ == "__main__":
    generate_openapi_spec() 