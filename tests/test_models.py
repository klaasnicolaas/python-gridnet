"""Test the models."""
import aiohttp
import pytest

from net2grid import Device, Net2Grid, SmartMeter

from . import load_fixtures


@pytest.mark.asyncio
async def test_device(aresponses):
    """Test request from a NET2GRID device - Device object."""
    aresponses.add(
        "example.com",
        "/info",
        "GET",
        aresponses.Response(
            text=load_fixtures("device.json"),
            status=200,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Net2Grid(host="example.com", session=session)
        device: Device = await client.device()
        assert device
        assert device.n2g_id == "84df:0c11:9999:3795"
        assert device.model == "SBWF3102"
        assert device.batch == "SBP-HMX-210318"
        assert device.firmware == "1.6.16"
        assert device.hardware == 1
        assert device.manufacturer == "NET2GRID"


@pytest.mark.asyncio
async def test_smartmeter(aresponses):
    """Test request from a NET2GRID device - SmartMeter object."""
    aresponses.add(
        "example.com",
        "/meter/now",
        "GET",
        aresponses.Response(
            text=load_fixtures("smartmeter.json"),
            status=200,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Net2Grid(host="example.com", session=session)
        smartmeter: SmartMeter = await client.smartmeter()
        assert smartmeter
        assert smartmeter.power_flow == 338
        assert smartmeter.energy_consumption_total == 17762.1
        assert smartmeter.energy_production_total == 21214.6
