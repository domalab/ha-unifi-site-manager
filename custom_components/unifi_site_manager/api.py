"""API Client for UniFi Site Manager."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any

import async_timeout
from aiohttp import ClientError, ClientResponse, ClientSession
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DEFAULT_API_HOST, UNIFI_API_HEADERS

_LOGGER = logging.getLogger(__name__)

# First define the base exception class
class UnifiSiteManagerAPIError(Exception):
    """General API error."""

# Then define the subclasses
class UnifiSiteManagerServerError(UnifiSiteManagerAPIError):
    """API server error."""

class UnifiSiteManagerGatewayError(UnifiSiteManagerAPIError):
    """API gateway error."""

class UnifiSiteManagerConnectionError(UnifiSiteManagerAPIError):
    """API connection error."""

class UnifiSiteManagerAuthError(UnifiSiteManagerAPIError):
    """API authentication error."""

class UnifiSiteManagerRateLimitError(UnifiSiteManagerAPIError):
    """API rate limit error."""

class UnifiSiteManagerAPI:
    """UniFi Site Manager API client."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        host: str = DEFAULT_API_HOST,
        session: ClientSession | None = None,
    ) -> None:
        """Initialize the API client."""
        self._hass = hass
        self._api_key = api_key
        self._host = host
        self._session = session or async_get_clientsession(hass)
        self._rate_limit_remaining = 100  # Default rate limit
        self._rate_limit_reset: datetime | None = None
        self._request_lock = asyncio.Lock()

    def _update_rate_limit(self, response: ClientResponse) -> None:
        """Update rate limit information from response headers."""
        if "X-RateLimit-Remaining" in response.headers:
            self._rate_limit_remaining = int(response.headers["X-RateLimit-Remaining"])
        if "X-RateLimit-Reset" in response.headers:
            self._rate_limit_reset = datetime.fromtimestamp(
                int(response.headers["X-RateLimit-Reset"])
            )

    async def _handle_rate_limit(self) -> None:
        """Handle rate limiting."""
        if self._rate_limit_remaining <= 0 and self._rate_limit_reset:
            wait_time = (self._rate_limit_reset - datetime.now()).total_seconds()
            if wait_time > 0:
                _LOGGER.warning(
                    "Rate limit reached. Waiting %s seconds before next request",
                    wait_time,
                )
                await asyncio.sleep(wait_time)

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Make an API request."""
        async with self._request_lock:
            await self._handle_rate_limit()

            headers = {
                **UNIFI_API_HEADERS,
                "X-API-Key": self._api_key,
            }

            if "headers" in kwargs:
                headers.update(kwargs.pop("headers"))

            url = f"{self._host}{endpoint}"

            try:
                async with async_timeout.timeout(10):
                    async with self._session.request(
                        method,
                        url,
                        headers=headers,
                        **kwargs,
                    ) as resp:
                        self._update_rate_limit(resp)

                        if resp.status == 401:
                            raise ConfigEntryAuthFailed("Invalid API key")
                        
                        if resp.status == 429:
                            retry_after = int(resp.headers.get("Retry-After", 60))
                            raise UnifiSiteManagerRateLimitError(
                                f"Rate limit exceeded, retry after {retry_after} seconds"
                            )
                        
                        if resp.status == 503:
                            raise UnifiSiteManagerServerError(
                                "UniFi Site Manager service is unavailable"
                            )
                        
                        if resp.status == 504:
                            raise UnifiSiteManagerGatewayError(
                                "UniFi Site Manager gateway timeout"
                            )
                        
                        if 500 <= resp.status < 600:
                            raise UnifiSiteManagerServerError(
                                f"Server error: {resp.status}"
                            )
                        
                        resp.raise_for_status()
                        return await resp.json()

            except asyncio.TimeoutError as err:
                raise UnifiSiteManagerConnectionError(
                    f"Timeout error requesting data from {url}"
                ) from err
            except ClientError as err:
                raise UnifiSiteManagerConnectionError(
                    f"Error requesting data from {url}: {str(err)}"
                ) from err

    async def async_get_sites(self) -> list[dict[str, Any]]:
        """Get all sites."""
        response = await self._request("GET", "/ea/sites")
        return response.get("data", [])

    async def async_get_hosts(self) -> list[dict[str, Any]]:
        """Get all hosts."""
        response = await self._request("GET", "/ea/hosts")
        return response.get("data", [])

    async def async_get_host(self, host_id: str) -> dict[str, Any]:
        """Get host by ID."""
        response = await self._request("GET", f"/ea/hosts/{host_id}")
        return response.get("data", {})

    async def async_get_isp_metrics(
        self,
        metric_type: str,
        site_id: str | None = None,
        begin_timestamp: datetime | None = None,
        end_timestamp: datetime | None = None,
        duration: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get ISP metrics."""
        params = {}
        if begin_timestamp:
            params["beginTimestamp"] = begin_timestamp.isoformat() + "Z"
        if end_timestamp:
            params["endTimestamp"] = end_timestamp.isoformat() + "Z"
        if duration:
            params["duration"] = duration

        if site_id:
            # Use query endpoint for specific site
            data = {
                "sites": [
                    {
                        "siteId": site_id,
                        **({"beginTimestamp": params.get("beginTimestamp")} if begin_timestamp else {}),
                        **({"endTimestamp": params.get("endTimestamp")} if end_timestamp else {}),
                    }
                ]
            }
            response = await self._request(
                "POST",
                f"/ea/isp-metrics/{metric_type}/query",
                json=data,
            )
            return response.get("data", {}).get("metrics", [])

        # Use GET endpoint for all sites
        response = await self._request(
            "GET",
            f"/ea/isp-metrics/{metric_type}",
            params=params,
        )
        return response.get("data", [])

    async def async_validate_api_key(self) -> bool:
        """Validate API key by making a test request."""
        try:
            await self.async_get_sites()
            return True
        except (UnifiSiteManagerAuthError, ConfigEntryAuthFailed):
            return False