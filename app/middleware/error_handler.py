# app/middleware/error_handler.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import logging


def register_error_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers.
    """

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logging.exception("Unhandled exception: %s", exc)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
