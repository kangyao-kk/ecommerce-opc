class SessionDomainError(Exception):
    pass


class InvalidSessionTitleError(SessionDomainError):
    pass


class SessionAlreadyArchivedError(SessionDomainError):
    pass

class SessionNotFoundError(SessionDomainError):
    pass
