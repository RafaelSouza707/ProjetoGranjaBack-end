class AppError(Exception):
    status_code = 400

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class NotFoundError(AppError):
    status_code = 404


class BusinessRuleError(AppError):
    status_code = 400