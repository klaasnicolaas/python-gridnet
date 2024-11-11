"""Test the models."""

from aresponses import ResponsesMockServer
from syrupy.assertion import SnapshotAssertion

from gridnet import Device, GridNet, SmartBridge

from . import load_fixtures


async def test_device(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    gridnet_client: GridNet,
) -> None:
    """Test request from the device - Device object."""
    aresponses.add(
        "127.0.0.1",
        "/info",
        "GET",
        aresponses.Response(
            text=load_fixtures("device.json"),
            status=200,
        ),
    )
    device: Device = await gridnet_client.device()
    assert device == snapshot


async def test_smartbridge(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    gridnet_client: GridNet,
) -> None:
    """Test request from the device - SmartBridge object."""
    aresponses.add(
        "127.0.0.1",
        "/meter/now",
        "GET",
        aresponses.Response(
            text=load_fixtures("smartbridge.json"),
            status=200,
        ),
    )
    smartbridge: SmartBridge = await gridnet_client.smartbridge()
    assert smartbridge == snapshot
