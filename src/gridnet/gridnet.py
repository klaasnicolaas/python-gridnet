"""Asynchronous Python client for NET2GRID devices."""
from __future__ import annotations

import asyncio
import json
import socket
from dataclasses import dataclass
from importlib import metadata
from typing import Any, Self, cast

from aiohttp import ClientError, ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from .exceptions import GridNetConnectionError
from .models import Device, SmartBridge


@dataclass
class GridNet:
    """Main class for handling connections with the devices."""

    host: str
    request_timeout: float = 10.0
    session: ClientSession | None = None

    _close_session: bool = False

    async def _request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        data: dict[str, Any] | None = None,
    ) -> Any:
        """Handle a request to the device.

        Args:
        ----
            uri: Request URI, without '/', for example, 'status'
            method: HTTP Method to use.
            data: Dictionary of data to send to the API.

        Returns:
        -------
            A Python dictionary (text) with the response from
            a device.

        Raises:
        ------
            GridNetConnectionError: An error occurred while
                communicating with the device.
        """
        version = metadata.version(__package__)
        url = URL.build(scheme="http", host=self.host, path="/").join(URL(uri))

        headers = {
            "User-Agent": f"PythonGridNet/{version}",
            "Accept": "application/json, text/plain, */*",
        }

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with asyncio.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    json=data,
                    headers=headers,
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            msg = f"Timeout occurred while connecting to {self.host}"
            raise GridNetConnectionError(
                msg,
            ) from exception
        except (
            ClientError,
            socket.gaierror,
        ) as exception:
            msg = f"Error occurred while communicating with {self.host}"
            raise GridNetConnectionError(
                msg,
            ) from exception

        return cast(dict[str, Any], json.loads(await response.text()))

    async def device(self) -> Device:
        """Get the latest values from a the device.

        Returns
        -------
            A Device data object from the API.
        """
        data = await self._request("info")
        return Device.from_dict(data)

    async def smartbridge(self) -> SmartBridge:
        """Get the latest values from a the device.

        Returns
        -------
            A SmartBridge data object from the API.
        """
        data = await self._request("meter/now")
        return SmartBridge.from_dict(data)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The GridNet object.
        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.
        """
        await self.close()
