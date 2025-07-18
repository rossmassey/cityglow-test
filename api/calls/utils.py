from typing import Type, Dict, Any

from pydantic import BaseModel


def pydantic_to_openapi_schema(pydantic_model: Type[BaseModel]) -> Dict[str, Any]:
    """
    Convert a Pydantic model to OpenAPI schema dict that drf-spectacular can use.
    
    This leverages Pydantic's built-in JSON schema generation.
    """
    # Pydantic 2.x way to get JSON schema
    schema = pydantic_model.model_json_schema()

    # Remove the title if it's just the class name to avoid duplication
    if 'title' in schema and schema['title'] == pydantic_model.__name__:
        del schema['title']

    return schema
