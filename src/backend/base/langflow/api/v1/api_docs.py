"""API documentation endpoints for Langflow."""

from pathlib import Path

import anyio
from fastapi import APIRouter
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.requests import Request

router = APIRouter(prefix="/api-docs", tags=["API Documentation"])


@router.get("/openapi.json")
async def get_openapi_spec(request: Request) -> JSONResponse:
    """Get the OpenAPI specification for the Langflow API.

    This endpoint returns the complete OpenAPI 3.0 specification
    for all API endpoints in Langflow, similar to the Vercel openapi.json.ts pattern.

    Returns:
        JSONResponse: The OpenAPI specification in JSON format
    """
    app = request.app

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="Langflow API - Build AI flows visually",
        routes=app.routes,
        servers=[
            {
                "url": str(request.base_url).rstrip("/"),
                "description": "Current environment",
            }
        ],
    )

    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}

    openapi_schema["components"]["securitySchemes"]["ApiKeyAuth"] = {
        "type": "apiKey",
        "in": "header",
        "name": "x-api-key",
        "description": "API key authentication",
    }

    openapi_schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "JWT token authentication",
    }

    if "security" not in openapi_schema:
        openapi_schema["security"] = []

    openapi_schema["security"].append({"ApiKeyAuth": []})
    openapi_schema["security"].append({"BearerAuth": []})

    return JSONResponse(content=openapi_schema)


@router.get("/", response_class=HTMLResponse)
async def get_swagger_ui() -> HTMLResponse:
    """Serve the Swagger UI page for interactive API documentation.

    This endpoint serves an HTML page with Swagger UI that loads the OpenAPI
    specification from the /api/v1/api-docs/openapi.json endpoint.

    Returns:
        HTMLResponse: The Swagger UI HTML page
    """
    html_file = anyio.Path(Path(__file__).parent / "swagger_ui.html")

    if not await html_file.exists():
        return HTMLResponse(
            content="<html><body><h1>Swagger UI not found</h1></body></html>",
            status_code=404,
        )

    html_content = await html_file.read_text(encoding="utf-8")

    return HTMLResponse(content=html_content)
