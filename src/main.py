import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_manager
from src.api.hotels import router as hotels_router
from src.api.auth import router as auth_router
from src.api.rooms import router as room_router
from src.api.bookings import router as booking_router
from src.api.facilities import router as facility_router
from src.api.images import router as image_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    # при выключении
    await redis_manager.close()

app = FastAPI(docs_url=None, lifespan=lifespan)

app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(room_router)
app.include_router(facility_router)
app.include_router(booking_router)
app.include_router(image_router)


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
