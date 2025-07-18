# CityGlow Calls API

This app uses a **Pydantic-only** approach for API documentation and validation.

## Architecture

### 📋 **Pydantic Schemas** (`schemas.py`)
- Define request/response models with validation
- Automatic JSON schema generation
- Type safety and IDE support

### 🛠 **Services** (`services/`)
- Business logic functions
- Return Pydantic models directly
- Reusable across views

### 🌐 **Views** (`views/`)
- Use Pydantic for validation
- Use `OpenApiRequest`/`OpenApiResponse` for documentation
- No DRF serializers needed!

### 🔧 **Utils** (`utils.py`)
- `pydantic_to_openapi_schema()` converts Pydantic models to OpenAPI schemas
- Used with drf-spectacular for clean documentation

## Benefits

✅ **Single Source of Truth**: Only Pydantic models, no duplication  
✅ **Type Safety**: Full typing throughout the stack  
✅ **Clean Documentation**: Direct Pydantic → OpenAPI schema generation  
✅ **Fast Validation**: Pydantic's high-performance validation  
✅ **Future Ready**: Easy to extend with complex validation rules

## Usage Pattern

```python
# 1. Define Pydantic models
class MyRequest(BaseModel):
    name: str = Field(..., description="User name")

class MyResponse(BaseModel):
    message: str
    
# 2. Use in views with OpenApiRequest/OpenApiResponse
@extend_schema(
    request=OpenApiRequest(request=pydantic_to_openapi_schema(MyRequest)),
    responses={200: OpenApiResponse(response=pydantic_to_openapi_schema(MyResponse))}
)
def my_view(request):
    # Validate with Pydantic
    data = MyRequest(**request.data)
    
    # Business logic returns Pydantic model
    result = MyService.do_something(data.name)
    
    # Convert to dict for DRF Response
    return Response(result.model_dump())
```

No more duplicate serializers! 🎉 