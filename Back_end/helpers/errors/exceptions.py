class AppError(Exception):
    status_code = 400
    error_type = "APP_ERROR"

    def __init__(self, message, error_type=None):
        self.message = message
        if error_type:
            self.error_type = error_type
        super().__init__(message)


class NotFoundError(AppError):
    status_code = 404
    error_type = "NOT_FOUND"


class BusinessRuleError(AppError):
    status_code = 400
    error_type = "BUSINESS_RULE"

class ForbiddenError(AppError):
    status_code = 401
    error_type = "FORBIDDEN"