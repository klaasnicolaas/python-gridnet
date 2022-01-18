"""Basic tests for the NET2GRID device."""
import asyncio
from unittest.mock import patch

import aiohttp
import pytest

from net2grid import Net2Grid
from net2grid.exceptions import Net2GridConnectionError, Net2GridError

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
        net2grid = Net2Grid("example.com", session=session)
        await net2grid.request("test")
        await net2grid.close()


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
    async with Net2Grid("example.com") as net2grid:
        await net2grid.request("test")


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
        net2grid = Net2Grid("example.com", session=session)
        response = await net2grid.request("test")
        assert response == "OK"


@pytest.mark.asyncio
async def test_timeout(aresponses):
    """Test request timeout from NET2GRID."""
    # Faking a timeout by sleeping
    async def response_handler(_):
        await asyncio.sleep(0.2)
        return aresponses.Response(
            body="Goodmorning!", text=load_fixtures("smartmeter.json")
        )

    aresponses.add("example.com", "/meter/now", "GET", response_handler)

    async with aiohttp.ClientSession() as session:
        client = Net2Grid(host="example.com", session=session, request_timeout=0.1)
        with pytest.raises(Net2GridConnectionError):
            assert await client.smartmeter()


@pytest.mark.asyncio
async def test_client_error():
    """Test request client error from NET2GRID."""
    async with aiohttp.ClientSession() as session:
        client = Net2Grid(host="example.com", session=session)
        with patch.object(
            session, "request", side_effect=aiohttp.ClientError
        ), pytest.raises(Net2GridConnectionError):
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
        client = Net2Grid(host="example.com", session=session)
        with pytest.raises(Net2GridError):
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
        client = Net2Grid(host="example.com", session=session)
        with pytest.raises(Net2GridError):
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
        client = Net2Grid(host="example.com", session=session)
        with pytest.raises(Net2GridError):
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
        client = Net2Grid(host="example.com", session=session)
        with pytest.raises(Net2GridError):
            assert await client.request("test")
