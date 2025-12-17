"""API generator from schemas."""

from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, create_model
import json


class InMemoryDB:
    """Simple in-memory database."""
    
    def __init__(self):
        self.data: Dict[str, List[Dict[str, Any]]] = {}
        self.counters: Dict[str, int] = {}
    
    def get_all(self, resource: str) -> List[Dict[str, Any]]:
        """Get all items for a resource."""
        return self.data.get(resource, [])
    
    def get_by_id(self, resource: str, item_id: int) -> Dict[str, Any]:
        """Get item by ID."""
        items = self.data.get(resource, [])
        for item in items:
            if item.get('id') == item_id:
                return item
        raise HTTPException(status_code=404, detail="Item not found")
    
    def create(self, resource: str, item: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new item."""
        if resource not in self.data:
            self.data[resource] = []
            self.counters[resource] = 0
        
        self.counters[resource] += 1
        item['id'] = self.counters[resource]
        self.data[resource].append(item)
        return item
    
    def update(self, resource: str, item_id: int, item: Dict[str, Any]) -> Dict[str, Any]:
        """Update an item."""
        items = self.data.get(resource, [])
        for i, existing_item in enumerate(items):
            if existing_item.get('id') == item_id:
                item['id'] = item_id
                items[i] = item
                return item
        raise HTTPException(status_code=404, detail="Item not found")
    
    def delete(self, resource: str, item_id: int) -> Dict[str, Any]:
        """Delete an item."""
        items = self.data.get(resource, [])
        for i, item in enumerate(items):
            if item.get('id') == item_id:
                deleted = items.pop(i)
                return deleted
        raise HTTPException(status_code=404, detail="Item not found")


def parse_simple_schema(schema: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    """Parse a simple JSON schema format."""
    resources = {}
    for resource_name, fields in schema.items():
        if isinstance(fields, dict):
            resources[resource_name] = fields
    return resources


def parse_openapi_schema(schema: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    """Parse OpenAPI 3.0 schema."""
    resources = {}
    
    if 'components' in schema and 'schemas' in schema['components']:
        for schema_name, schema_def in schema['components']['schemas'].items():
            if 'properties' in schema_def:
                fields = {}
                for field_name, field_def in schema_def['properties'].items():
                    field_type = field_def.get('type', 'string')
                    if isinstance(field_type, dict):
                        field_type = 'string'
                    fields[field_name] = field_type
                resources[schema_name.lower()] = fields
    
    return resources


def create_pydantic_model(resource_name: str, fields: Dict[str, str]) -> type:
    """Create a Pydantic model from field definitions."""
    field_definitions = {}
    
    for field_name, field_type in fields.items():
        if field_name == 'id':
            continue  # ID is auto-generated
        
        python_type = str
        if field_type == 'number' or field_type == 'integer':
            python_type = int
        elif field_type == 'boolean':
            python_type = bool
        
        field_definitions[field_name] = (python_type, ...)
    
    return create_model(f"{resource_name.title()}Model", **field_definitions)


def generate_api_from_schema(schema: Dict[str, Any]) -> FastAPI:
    """Generate a FastAPI app from a schema."""
    app = FastAPI(title="Mock API", version="1.0.0")
    db = InMemoryDB()
    
    # Determine schema type
    if 'openapi' in schema or 'swagger' in schema:
        resources = parse_openapi_schema(schema)
    else:
        resources = parse_simple_schema(schema)
    
    if not resources:
        raise ValueError("No resources found in schema")
    
    # Generate endpoints for each resource
    for resource_name, fields in resources.items():
        # Create Pydantic model
        Model = create_pydantic_model(resource_name, fields)
        
        # GET all
        @app.get(f"/{resource_name}", tags=[resource_name])
        def get_all():
            return db.get_all(resource_name)
        
        # GET by ID
        @app.get(f"/{resource_name}/{{item_id}}", tags=[resource_name])
        def get_by_id(item_id: int):
            return db.get_by_id(resource_name, item_id)
        
        # POST create
        @app.post(f"/{resource_name}", tags=[resource_name])
        def create_item(item: Model):
            item_dict = item.model_dump()
            return db.create(resource_name, item_dict)
        
        # PUT update
        @app.put(f"/{resource_name}/{{item_id}}", tags=[resource_name])
        def update_item(item_id: int, item: Model):
            item_dict = item.model_dump()
            return db.update(resource_name, item_id, item_dict)
        
        # DELETE
        @app.delete(f"/{resource_name}/{{item_id}}", tags=[resource_name])
        def delete_item(item_id: int):
            return db.delete(resource_name, item_id)
    
    return app


