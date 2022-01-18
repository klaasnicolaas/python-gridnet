"""Asynchronous Python client for NET2GRID devices."""
from __future__ import annotations

import asyncio
import json
import socket
from dataclasses import dataclass
from importlib import metadata
from typing import Any

import async_timeout
from aiohttp.client import ClientError, ClientResponseError, ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from .exceptions import Net2GridConnectionError
from .models import Device, SmartMeter


@dataclass
class Net2Grid:
    """Main class for handling connections with the NET2GRID devices."""

    host: str
    request_timeout: int = 10
    session: ClientSession | None = None

    _close_session: bool = False

    async def request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        data: dict | None = None,
    ) -> dict[str, Any]:
        """Handle a request to a NET2GRID device.

        Args:
            uri: Request URI, without '/', for example, 'status'
            method: HTTP Method to use.
            data: Dictionary of data to send to the NET2GRID API.

        Returns:
            A Python dictionary (text) with the response from
            a NET2GRID device.

        Raises:
            Net2GridConnectionError: An error occurred while
                communicating with the NET2GRID device.
        """
        version = metadata.version(__package__)
        url = URL.build(scheme="http", host=self.host, path="/").join(URL(uri))

        headers = {
            "User-Agent": f"PythonNet2Grid/{version}",
            "Accept": "application/json, text/plain, */*",
        }

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    json=data,
                    headers=headers,
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            raise Net2GridConnectionError(
                "Timeout occurred while connecting to the NET2GRID device"
            ) from exception
        except (
            ClientError,
            ClientResponseError,
            socket.gaierror,
        ) as exception:
            raise Net2GridConnectionError(
                "Error occurred while communicating with the NET2GRID device"
            ) from exception

        return await response.text()

    async def device(self) -> Device:
        """Get the latest values from a NET2GRID device.

        Returns:
            A Device data object from the API.
        """
        data = await self.request("info")
        data = json.loads(data)
        return Device.from_dict(data)

    async def smartmeter(self) -> SmartMeter:
        """Get the latest values from a NET2GRID device.

        Returns:
            A SmartMeter data object from the API.
        """
        data = await self.request("meter/now")
        data = json.loads(data)
        return SmartMeter.from_dict(data)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Net2Grid:
        """Async enter.

        Returns:
            The NET2GRID object.
        """
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit.

        Args:
            _exc_info: Exec type.
        """
        await self.close()
