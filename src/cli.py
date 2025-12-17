#!/usr/bin/env python3
"""CLI entry point for mock-api-gen."""

import json
import yaml
from pathlib import Path
import click
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.generator import generate_api_from_schema


@click.command()
@click.argument('schema_file', type=click.Path(exists=True))
@click.option('--port', '-p', default=8000, help='Port to run the server on')
@click.option('--host', '-h', default='127.0.0.1', help='Host to bind to')
@click.option('--reload', is_flag=True, help='Enable auto-reload')
def main(schema_file, port, host, reload):
    """Generate a mock REST API from a JSON schema or OpenAPI spec."""
    
    schema_path = Path(schema_file)
    
    # Load schema
    try:
        if schema_path.suffix in ['.yaml', '.yml']:
            with open(schema_path, 'r') as f:
                schema = yaml.safe_load(f)
        else:
            with open(schema_path, 'r') as f:
                schema = json.load(f)
    except Exception as e:
        click.echo(f"Error loading schema file: {e}", err=True)
        return
    
    # Generate API
    app = generate_api_from_schema(schema)
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    click.echo(f"🚀 Starting mock API server on http://{host}:{port}")
    click.echo(f"📚 API Documentation: http://{host}:{port}/docs")
    click.echo(f"📖 ReDoc: http://{host}:{port}/redoc")
    click.echo("\nPress CTRL+C to stop the server")
    
    # Run server
    uvicorn.run(app, host=host, port=port, reload=reload)


if __name__ == '__main__':
    main()


