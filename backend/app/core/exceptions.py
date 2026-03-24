class AppError(Exception):
    def __init__(self, message: str, *, status_code: int = 500, code: str = "internal_error") -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code


class AuthenticationError(AppError):
    def __init__(self, message: str = "Invalid Firebase token") -> None:
        super().__init__(message, status_code=401, code="authentication_error")


class StorageError(AppError):
    def __init__(self, message: str = "Unable to store file") -> None:
        super().__init__(message, status_code=502, code="storage_error")


class PersistenceError(AppError):
    def __init__(self, message: str = "Unable to persist data") -> None:
        super().__init__(message, status_code=502, code="persistence_error")
