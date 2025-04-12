import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path

from fastapi.openapi.docs import get_swagger_ui_html

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotels_router
from src.api.auth import router as auth_router
from src.api.rooms import router as room_router
from src.api.bookings import router as booking_router

app = FastAPI(debug=True)

app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(room_router)
app.include_router(booking_router)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,  # type: ignore
        title=app.title + " - Swagger UI",  # type: ignore
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,  # type: ignore
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
