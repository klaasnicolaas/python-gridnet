"""Basic tests for the API."""
# pylint: disable=protected-access
import asyncio
from unittest.mock import patch

import aiohttp
import pytest
from aresponses import Response, ResponsesMockServer

from gridnet import GridNet
from gridnet.exceptions import GridNetConnectionError, GridNetError

from . import load_fixtures


@pytest.mark.asyncio
async def test_json_request(aresponses: ResponsesMockServer) -> None:
    """Test JSON response is handled correctly."""
    aresponses.add(
        "example.com",
        "/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"status": "ok"}',
        ),
    )
    async with aiohttp.ClientSession() as session:
        client = GridNet("example.com", session=session)
        await client._request("test")
        await client.close()


@pytest.mark.asyncio
async def test_internal_session(aresponses: ResponsesMockServer) -> None:
    """Test JSON response is handled correctly."""
    aresponses.add(
        "example.com",
        "/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"status": "ok"}',
        ),
    )
    async with GridNet("example.com") as client:
        await client._request("test")


@pytest.mark.asyncio
async def test_timeout(aresponses: ResponsesMockServer) -> None:
    """Test request timeout from the API."""
    # Faking a timeout by sleeping
    async def response_handler(_: aiohttp.ClientResponse) -> Response:
        await asyncio.sleep(0.2)
        return aresponses.Response(
            body="Goodmorning!", text=load_fixtures("smartbridge.json")
        )

    aresponses.add("example.com", "/meter/now", "GET", response_handler)

    async with aiohttp.ClientSession() as session:
        client = GridNet(host="example.com", session=session, request_timeout=0.1)
        with pytest.raises(GridNetConnectionError):
            assert await client.smartbridge()


@pytest.mark.asyncio
async def test_client_error() -> None:
    """Test request client error from the API."""
    async with aiohttp.ClientSession() as session:
        client = GridNet(host="example.com", session=session)
        with patch.object(
            session, "request", side_effect=aiohttp.ClientError
        ), pytest.raises(GridNetConnectionError):
            assert await client._request("test")


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [401, 403])
async def test_http_error401(aresponses: ResponsesMockServer, status: int) -> None:
    """Test HTTP 401 response handling."""
    aresponses.add(
        "example.com",
        "/meter/now",
        "GET",
        aresponses.Response(text="Give me energy!", status=status),
    )

    async with aiohttp.ClientSession() as session:
        client = GridNet(host="example.com", session=session)
        with pytest.raises(GridNetError):
            assert await client._request("test")


@pytest.mark.asyncio
async def test_http_error400(aresponses: ResponsesMockServer) -> None:
    """Test HTTP 404 response handling."""
    aresponses.add(
        "example.com",
        "/meter/now",
        "GET",
        aresponses.Response(text="Give me energy!", status=404),
    )

    async with aiohttp.ClientSession() as session:
        client = GridNet(host="example.com", session=session)
        with pytest.raises(GridNetError):
            assert await client._request("test")


@pytest.mark.asyncio
async def test_http_error500(aresponses: ResponsesMockServer) -> None:
    """Test HTTP 500 response handling."""
    aresponses.add(
        "example.com",
        "/meter/now",
        "GET",
        aresponses.Response(
            body=b'{"status":"nok"}',
            status=500,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = GridNet(host="example.com", session=session)
        with pytest.raises(GridNetError):
            assert await client._request("test")


@pytest.mark.asyncio
async def test_no_success(aresponses: ResponsesMockServer) -> None:
    """Test a message without a success message throws."""
    aresponses.add(
        "example.com",
        "/meter/now",
        "GET",
        aresponses.Response(
            status=200,
            text='{"message": "no success"}',
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = GridNet(host="example.com", session=session)
        with pytest.raises(GridNetError):
            assert await client._request("test")
