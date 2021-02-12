""" This module provides the exceptions."""


class DOIError(Exception):
    """
    Base class for exceptions in this module.

    """


class ExternalError(DOIError):
    """
    Exceptions resulting from communication with external services.

    """
