# mock-api-gen

Generate instant REST APIs from JSON schemas or OpenAPI specs. Perfect for frontend development, testing, and prototyping.

## Features

- 🚀 Generate CRUD endpoints automatically
- 📝 Support for JSON schema and OpenAPI/Swagger specs
- 💾 In-memory database with optional persistence
- 🌐 CORS enabled by default
- ⚙️ Customizable port and host
- 🔄 Hot reload support

## Installation

```bash
pip install -e .
```

Or install globally:
```bash
pip install .
```

## Usage

### Basic Usage

Generate an API from a JSON schema:

```bash
mock-api-gen schema.json
```

### With Custom Port

```bash
mock-api-gen schema.json --port 8000
```

### From OpenAPI Spec

```bash
mock-api-gen api-spec.yaml --port 3000
```

## Schema Format

### Simple JSON Schema

```json
{
  "users": {
    "id": "number",
    "name": "string",
    "email": "string"
  },
  "posts": {
    "id": "number",
    "title": "string",
    "content": "string",
    "userId": "number"
  }
}
```

### OpenAPI/Swagger Format

The tool also supports standard OpenAPI 3.0 YAML files.

## Generated Endpoints

For each resource, the following endpoints are automatically generated:

- `GET /{resource}` - List all items
- `GET /{resource}/{id}` - Get item by ID
- `POST /{resource}` - Create new item
- `PUT /{resource}/{id}` - Update item
- `DELETE /{resource}/{id}` - Delete item

## Examples

### Example 1: Simple API

```bash
# Create schema.json
echo '{"products": {"id": "number", "name": "string", "price": "number"}}' > schema.json

# Generate API
mock-api-gen schema.json

# Test the API
curl http://localhost:8000/products
```

### Example 2: Multiple Resources

```json
{
  "users": {
    "id": "number",
    "name": "string",
    "email": "string"
  },
  "posts": {
    "id": "number",
    "title": "string",
    "userId": "number"
  }
}
```

This generates endpoints for both `/users` and `/posts`.

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please open an issue or submit a pull request.


