# pylint: disable=W0621
"""Asynchronous Python client for the NET2GRID API."""

import asyncio

from net2grid import Device, Net2Grid, SmartMeter


async def main():
    """Test."""
    async with Net2Grid(
        host="example.com",
    ) as net2grid:
        smartmeter: SmartMeter = await net2grid.smartmeter()
        device: Device = await net2grid.device()
        print(smartmeter)
        print()
        print(f"Power flow: {smartmeter.power_flow}")
        print(f"Energy consumption: {smartmeter.energy_consumption_total}")
        print(f"Energy production: {smartmeter.energy_production_total}")
        print()
        print(device)
        print(f"ID: {device.n2g_id}")
        print(f"Model: {device.model}")
        print(f"Batch: {device.batch}")
        print(f"Firmware version: {device.firmware}")
        print(f"Hardware version: {device.hardware}")
        print(f"Manufacturer: {device.manufacturer}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
