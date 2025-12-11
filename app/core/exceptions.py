# app/core/exceptions.py
from fastapi import HTTPException, status


def unauthorized(detail: str = "Not authorized") -> HTTPException:
    """
    Return a standardized 401 HTTPException.

    Args:
        detail: detail message.

    Returns:
        HTTPException with 401 status.
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def forbidden(detail: str = "Forbidden") -> HTTPException:
    """Return 403 HTTPException."""
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
