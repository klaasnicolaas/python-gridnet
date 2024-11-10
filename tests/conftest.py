"""Fixture for the Gridnet tests."""

from collections.abc import AsyncGenerator

import pytest
from aiohttp import ClientSession

from gridnet import GridNet


@pytest.fixture(name="gridnet_client")
async def client() -> AsyncGenerator[GridNet, None]:
    """Fixture for the GridNet client."""
    async with (
        ClientSession() as session,
        GridNet(host="127.0.0.1", session=session) as gridnet_client,
    ):
        yield gridnet_client
