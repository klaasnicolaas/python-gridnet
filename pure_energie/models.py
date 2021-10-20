"""Models for Pure Energie Meter."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass
class SmartMeter:
    """Object representing an SmartMeter response from Pure Energie Meter."""

    power_flow: int
    energy_consumption_total: float
    energy_production_total: float

    @staticmethod
    def from_dict(data: dict[str, Any]) -> SmartMeter:
        """Return SmartMeter object from the Pure Energie Meter API response.

        Args:
            data: The data from the Pure Energie Meter API.

        Returns:
            A SmartMeter object.
        """
        data = json.loads(data)
        data = data["elec"]

        def convert(value):
            """Convert the unit of measurement.

            Args:
                value: input value.

            Returns:
                Value in kWh rounded with 1 decimal.
            """
            value = value / 1000
            return round(value, 1)

        return SmartMeter(
            power_flow=data["power"]["now"].get("value"),
            energy_consumption_total=convert(data["import"]["now"].get("value")),
            energy_production_total=convert(data["export"]["now"].get("value")),
        )


@dataclass
class Device:
    """Object representing an Device response from Pure Energie Meter."""

    pem_id: str
    model: str
    firmware: str
    manufacturer: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Device:
        """Return Device object from the Pure Energie Meter API response.

        Args:
            data: The data from the Pure Energie Meter API.

        Returns:
            A Device object.
        """
        data = json.loads(data)

        return Device(
            pem_id=data.get("id"),
            model=data.get("model"),
            firmware=data.get("fw"),
            manufacturer=data.get("mf"),
        )
