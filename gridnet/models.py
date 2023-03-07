"""Models for GridNet."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class SmartBridge:
    """Object representing an SmartBridge response from the device."""

    power_flow: int
    energy_consumption_total: float
    energy_production_total: float

    @staticmethod
    def from_dict(data: dict[str, Any]) -> SmartBridge:
        """Return SmartBridge object from the API response.

        Args:
        ----
            data: Response data from the API.

        Returns:
        -------
            A SmartBridge object.
        """
        data = data["elec"]

        def convert(value: float) -> float:
            """Convert the unit of measurement.

            Args:
            ----
                value: input value.

            Returns:
            -------
                Value in kWh rounded with 1 decimal.
            """
            value = value / 1000
            return float(round(value, 1))

        return SmartBridge(
            power_flow=data["power"]["now"].get("value"),
            energy_consumption_total=convert(data["import"]["now"].get("value")),
            energy_production_total=convert(data["export"]["now"].get("value")),
        )


@dataclass
class Device:
    """Object representing an Device response from the device."""

    n2g_id: str
    model: str
    batch: str
    firmware: str
    hardware: int
    manufacturer: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Device:
        """Return Device object from the API response.

        Args:
        ----
            data: Response data from the API.

        Returns:
        -------
            A Device object.
        """
        return Device(
            n2g_id=data["id"],
            model=data["model"],
            batch=data["batch"],
            firmware=data["fw"],
            hardware=data["hw"],
            manufacturer=data["mf"],
        )
