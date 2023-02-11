"""Test the models."""
from aiohttp import ClientSession
from aresponses import ResponsesMockServer

from gridnet import Device, GridNet, SmartBridge

from . import load_fixtures


async def test_device(aresponses: ResponsesMockServer) -> None:
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

    async with ClientSession() as session:
        client = GridNet(host="127.0.0.1", session=session)
        device: Device = await client.device()
        assert device
        assert device.n2g_id == "84df:0c11:9999:3795"
        assert device.model == "SBWF3102"
        assert device.batch == "SBP-HMX-210318"
        assert device.firmware == "1.6.16"
        assert device.hardware == 1
        assert device.manufacturer == "NET2GRID"


async def test_smartbridge(aresponses: ResponsesMockServer) -> None:
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

    async with ClientSession() as session:
        client = GridNet(host="127.0.0.1", session=session)
        smartbridge: SmartBridge = await client.smartbridge()
        assert smartbridge
        assert smartbridge.power_flow == 338
        assert smartbridge.energy_consumption_total == 17762.1
        assert smartbridge.energy_production_total == 21214.6
