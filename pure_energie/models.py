"""Models for Pure Energie Meter."""
from __future__ import annotations

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
    batch: str
    firmware: str
    hardware: int
    manufacturer: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Device:
        """Return Device object from the Pure Energie Meter API response.

        Args:
            data: The data from the Pure Energie Meter API.

        Returns:
            A Device object.
        """

        return Device(
            pem_id=data.get("id"),
            model=data.get("model"),
            batch=data.get("batch"),
            firmware=data.get("fw"),
            hardware=data.get("hw"),
            manufacturer=data.get("mf"),
        )
