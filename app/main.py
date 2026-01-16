from fastapi import FastAPI

from app.middlewares.logging_middleware import LoggingMiddleware
from app.logging import initialize_logger
from app.routers.chat_router import chat_router

app = FastAPI()

app.add_middleware(LoggingMiddleware)

app.include_router(chat_router)

initialize_logger(app)

