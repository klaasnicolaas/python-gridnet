"""Exceptions for GridNet."""


class GridNetError(Exception):
    """Generic GridNet exception."""


class GridNetConnectionError(GridNetError):
    """GridNet connection exception."""
