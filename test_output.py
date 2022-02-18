# pylint: disable=W0621
"""Asynchronous Python client for a NET2GRID device."""

import asyncio

from gridnet import Device, GridNet, SmartBridge


async def main():
    """Test."""
    async with GridNet(
        host="example.com",
    ) as gridnet:
        smartbridge: SmartBridge = await gridnet.smartbridge()
        device: Device = await gridnet.device()
        print(smartbridge)
        print()
        print(f"Power flow: {smartbridge.power_flow}")
        print(f"Energy consumption: {smartbridge.energy_consumption_total}")
        print(f"Energy production: {smartbridge.energy_production_total}")
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
