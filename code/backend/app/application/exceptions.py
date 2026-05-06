class ApplicationError(Exception):
    pass


class NotFoundError(ApplicationError):
    pass


class ConflictError(ApplicationError):
    pass


class InvalidStateTransitionError(ApplicationError):
    pass


class ValidationError(ApplicationError):
    pass


class AuthenticationError(ApplicationError):
    pass
