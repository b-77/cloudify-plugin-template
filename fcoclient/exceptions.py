# coding=UTF-8

"""Some placeholder Exceptions."""


class NonRecoverableError(Exception):

    """A non-recoverable error that should cause the workflow to stop."""

    def __init__(self, message):
        """Create a new NonRecoverableError."""
        super(Exception, self).__init__(message)


class RecoverableError(Exception):

    """A recoverable error that should cause the workflow to retry."""

    def __init__(self, message, retry_after):
        """Create a new RecoverableError."""
        super(Exception, self).__init__(message)

        self.retry_after = retry_after
