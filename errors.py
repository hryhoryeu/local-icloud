from fastapi import HTTPException, status


class AlreadyExistsError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class UnauthorizedError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class BadRequestError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class PermissionDenied(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class InvalidTokenError(UnauthorizedError):
    pass
