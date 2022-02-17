"""Basic tests for the API."""
import asyncio
from unittest.mock import patch

import aiohttp
import pytest

from gridnet import GridNet
from gridnet.exceptions import GridNetConnectionError, GridNetError

from . import load_fixtures


@pytest.mark.asyncio
async def test_json_request(aresponses):
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
        await client.request("test")
        await client.close()


@pytest.mark.asyncio
async def test_internal_session(aresponses):
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
        await client.request("test")


@pytest.mark.asyncio
async def test_text_request(aresponses):
    """Test non JSON response is handled correctly."""
    aresponses.add(
        "example.com",
        "/test",
        "GET",
        aresponses.Response(status=200, text="OK"),
    )
    async with aiohttp.ClientSession() as session:
        client = GridNet("example.com", session=session)
        response = await client.request("test")
        assert response == "OK"


@pytest.mark.asyncio
async def test_timeout(aresponses):
    """Test request timeout from the API."""
    # Faking a timeout by sleeping
    async def response_handler(_):
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
async def test_client_error():
    """Test request client error from the API."""
    async with aiohttp.ClientSession() as session:
        client = GridNet(host="example.com", session=session)
        with patch.object(
            session, "request", side_effect=aiohttp.ClientError
        ), pytest.raises(GridNetConnectionError):
            assert await client.request("test")


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [401, 403])
async def test_http_error401(aresponses, status):
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
            assert await client.request("test")


@pytest.mark.asyncio
async def test_http_error400(aresponses):
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
            assert await client.request("test")


@pytest.mark.asyncio
async def test_http_error500(aresponses):
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
            assert await client.request("test")


@pytest.mark.asyncio
async def test_no_success(aresponses):
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
            assert await client.request("test")
