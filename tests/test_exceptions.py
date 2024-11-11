"""Test exceptions for GridNet package."""

# pylint: disable=protected-access
import pytest
from aresponses import ResponsesMockServer

from gridnet import GridNet
from gridnet.exceptions import GridNetError


@pytest.mark.parametrize("status", [401, 403, 404])
async def test_http_error400(
    aresponses: ResponsesMockServer, status: int, gridnet_client: GridNet
) -> None:
    """Test HTTP 40X response handling."""
    aresponses.add(
        "127.0.0.1",
        "/meter/now",
        "GET",
        aresponses.Response(text="Give me energy!", status=status),
    )
    with pytest.raises(GridNetError):
        assert await gridnet_client._request("test")


async def test_http_error500(
    aresponses: ResponsesMockServer, gridnet_client: GridNet
) -> None:
    """Test HTTP 500 response handling."""
    aresponses.add(
        "127.0.0.1",
        "/meter/now",
        "GET",
        aresponses.Response(
            body=b'{"status":"nok"}',
            status=500,
        ),
    )
    with pytest.raises(GridNetError):
        assert await gridnet_client._request("test")


async def test_no_success(
    aresponses: ResponsesMockServer, gridnet_client: GridNet
) -> None:
    """Test a message without a success message throws."""
    aresponses.add(
        "127.0.0.1",
        "/meter/now",
        "GET",
        aresponses.Response(
            status=200,
            text='{"message": "no success"}',
        ),
    )
    with pytest.raises(GridNetError):
        assert await gridnet_client._request("test")
