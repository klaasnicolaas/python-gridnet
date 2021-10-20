"""Exceptions for Pure Energie Meter."""


class PureEnergieMeterError(Exception):
    """Generic Pure Energie Meter exception."""


class PureEnergieMeterConnectionError(PureEnergieMeterError):
    """Pure Energie Meter connection exception."""
