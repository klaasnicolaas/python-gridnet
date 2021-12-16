# pylint: disable=W0621
"""Asynchronous Python client for the Pure Energie Meter API."""

import asyncio

from pure_energie import Device, PureEnergie, SmartMeter


async def main():
    """Test."""
    async with PureEnergie(
        host="example.com",
    ) as pem:
        smartmeter: SmartMeter = await pem.smartmeter()
        device: Device = await pem.device()
        print(smartmeter)
        print()
        print(f"Power flow: {smartmeter.power_flow}")
        print(f"Energy consumption: {smartmeter.energy_consumption_total}")
        print(f"Energy production: {smartmeter.energy_production_total}")
        print()
        print(device)
        print(f"ID: {device.pem_id}")
        print(f"Model: {device.model}")
        print(f"Batch: {device.batch}")
        print(f"Firmware version: {device.firmware}")
        print(f"Hardware version: {device.hardware}")
        print(f"Manufacturer: {device.manufacturer}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
