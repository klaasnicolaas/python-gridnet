# pylint: disable=W0621
"""Asynchronous Python client for a NET2GRID device."""

import asyncio

from gridnet import GridNet, SmartBridge


async def main() -> None:
    """Test smartbridge output."""
    async with GridNet(
        host="127.0.0.1",
    ) as gridnet:
        smartbridge: SmartBridge = await gridnet.smartbridge()
        print(smartbridge)
        print()
        print(f"Power flow: {smartbridge.power_flow}")
        print(f"Energy consumption: {smartbridge.energy_consumption_total}")
        print(f"Energy production: {smartbridge.energy_production_total}")


if __name__ == "__main__":
    asyncio.run(main())
