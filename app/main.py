from fastapi import FastAPI

from app.middlewares.logging_middleware import LoggingMiddleware
from app.logging import initialize_logger
app = FastAPI()

app.add_middleware(LoggingMiddleware)

initialize_logger(app)

