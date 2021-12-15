"""Asynchronous Python client for Pure Energie Meter API."""
from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any, Mapping

from aiohttp.client import ClientError, ClientResponseError, ClientSession
from async_timeout import timeout
from yarl import URL

from .exceptions import PureEnergieMeterConnectionError
from .models import Device, SmartMeter


@dataclass
class PureEnergie:
    """Main class for handling connections with the Pure Energie Meter API."""

    def __init__(
        self, host: str, request_timeout: int = 10, session: ClientSession | None = None
    ) -> None:
        """Initialize connection with the Pure Energie Meter API.

        Args:
            host: Hostname or IP address of Pure Energie Meter device.
            request_timeout: An integer with the request timeout in seconds.
            session: Optional, shared, aiohttp client session.
        """
        self._session = session
        self._close_session: bool = False

        self.host = host
        self.request_timeout = request_timeout

    async def request(
        self,
        uri: str,
        *,
        params: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        """Handle a request to a Pure Energie device.

        Args:
            uri: Request URI, without '/', for example, 'status'
            params: Extra options to improve or limit the response.

        Returns:
            A Python dictionary (text) with the response from
            the Pure Energie device.

        Raises:
            PureEnergieMeterConnectionError: An error occurred while
                communicating with the Pure Energie device.
        """
        url = URL.build(scheme="http", host=self.host, path="/").join(URL(uri))

        headers = {
            "Accept": "application/json, text/plain, */*",
        }

        if self._session is None:
            self._session = ClientSession()
            self._close_session = True

        try:
            async with timeout(self.request_timeout):
                response = await self._session.request(
                    "GET",
                    url,
                    params=params,
                    headers=headers,
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            raise PureEnergieMeterConnectionError(
                "Timeout occurred while connecting to Pure Energie Meter device"
            ) from exception
        except (ClientError, ClientResponseError) as exception:
            raise PureEnergieMeterConnectionError(
                "Error occurred while communicating with the Pure Energie Meter device"
            ) from exception

        return await response.text()

    async def device(self) -> Device:
        """Get the latest values from the Pure Energie Meter.

        Returns:
            A Device data object from the Pure Energie device API.
        """
        data = await self.request("info")
        data = json.loads(data)
        return Device.from_dict(data)

    async def smartmeter(self) -> SmartMeter:
        """Get the latest values from the Pure Energie Meter.

        Returns:
            A SmartMeter data object from the Pure Energie device API.
        """
        data = await self.request("meter/now")
        data = json.loads(data)
        return SmartMeter.from_dict(data)

    async def close(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> PureEnergie:
        """Async enter.

        Returns:
            The Pure Energie Meter object.
        """
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit.

        Args:
            _exc_info: Exec type.
        """
        await self.close()
