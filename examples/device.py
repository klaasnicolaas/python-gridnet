# pylint: disable=W0621
"""Asynchronous Python client for a NET2GRID device."""

import asyncio

from gridnet import Device, GridNet


async def main() -> None:
    """Test device output."""
    async with GridNet(
        host="127.0.0.1",
    ) as gridnet:
        device: Device = await gridnet.device()
        print(device)
        print(f"ID: {device.n2g_id}")
        print(f"Model: {device.model}")
        print(f"Batch: {device.batch}")
        print(f"Firmware version: {device.firmware}")
        print(f"Hardware version: {device.hardware}")
        print(f"Manufacturer: {device.manufacturer}")


if __name__ == "__main__":
    asyncio.run(main())
