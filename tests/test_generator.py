"""Tests for API generator."""

import pytest
from src.generator import generate_api_from_schema, parse_simple_schema, InMemoryDB


def test_parse_simple_schema():
    """Test parsing simple schema."""
    schema = {
        "users": {
            "name": "string",
            "email": "string"
        }
    }
    resources = parse_simple_schema(schema)
    assert "users" in resources
    assert resources["users"]["name"] == "string"


def test_in_memory_db():
    """Test in-memory database operations."""
    db = InMemoryDB()
    
    # Create
    item = db.create("users", {"name": "John", "email": "john@example.com"})
    assert item["id"] == 1
    assert item["name"] == "John"
    
    # Get all
    items = db.get_all("users")
    assert len(items) == 1
    
    # Get by ID
    item = db.get_by_id("users", 1)
    assert item["name"] == "John"
    
    # Update
    updated = db.update("users", 1, {"name": "Jane", "email": "jane@example.com"})
    assert updated["name"] == "Jane"
    
    # Delete
    deleted = db.delete("users", 1)
    assert deleted["name"] == "Jane"
    
    # Get all should be empty
    items = db.get_all("users")
    assert len(items) == 0


def test_generate_api():
    """Test API generation."""
    schema = {
        "products": {
            "name": "string",
            "price": "number"
        }
    }
    
    app = generate_api_from_schema(schema)
    assert app is not None
    
    # Check that routes are registered
    routes = [route.path for route in app.routes]
    assert "/products" in routes
    assert "/products/{item_id}" in routes


