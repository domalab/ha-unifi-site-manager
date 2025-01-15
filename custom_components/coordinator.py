"""Data update coordinator for UniFi Site Manager integration."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    UnifiSiteManagerAPI,
    UnifiSiteManagerAPIError,
    UnifiSiteManagerAuthError,
    UnifiSiteManagerConnectionError,
    UnifiSiteManagerRateLimitError,
)
from .const import (
    DOMAIN,
    SCAN_INTERVAL_METRICS,
    SCAN_INTERVAL_NORMAL,
    METRIC_TYPE_5M,
)

_LOGGER = logging.getLogger(__name__)


class UnifiSiteManagerDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching UniFi Site Manager data."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        api: UnifiSiteManagerAPI,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL_NORMAL,
        )
        self.api = api
        self.config_entry = entry
        self._available = True
        self.data = {
            "sites": {},
            "hosts": {},
            "metrics": {},
            "last_update": None,
        }
        self._metric_update_lock = asyncio.Lock()
        self._site_update_lock = asyncio.Lock()
        self._host_update_lock = asyncio.Lock()

    async def _async_update_sites(self) -> None:
        """Update sites data."""
        async with self._site_update_lock:
            try:
                sites = await self.api.async_get_sites()
                self.data["sites"] = {site["siteId"]: site for site in sites}
                _LOGGER.debug("Updated %s sites", len(sites))
            except UnifiSiteManagerAuthError as err:
                self._available = False
                raise ConfigEntryAuthFailed from err
            except UnifiSiteManagerAPIError as err:
                self._available = False
                raise UpdateFailed(f"Error updating sites: {err}") from err

    async def _async_update_hosts(self) -> None:
        """Update hosts data."""
        async with self._host_update_lock:
            try:
                hosts = await self.api.async_get_hosts()
                self.data["hosts"] = {host["id"]: host for host in hosts}
                _LOGGER.debug("Updated %s hosts", len(hosts))
            except UnifiSiteManagerAPIError as err:
                self._available = False
                raise UpdateFailed(f"Error updating hosts: {err}") from err

    async def _async_update_metrics(self) -> None:
        """Update ISP metrics data."""
        async with self._metric_update_lock:
            try:
                # Use timezone-aware datetime
                end_time = datetime.now(timezone.utc)
                start_time = end_time - SCAN_INTERVAL_METRICS

                metrics = {}
                for site_id in self.data["sites"]:
                    try:
                        site_metrics = await self.api.async_get_isp_metrics(
                            METRIC_TYPE_5M,
                            site_id=site_id,
                            begin_timestamp=start_time,
                            end_timestamp=end_time,
                        )
                        if site_metrics:
                            metrics[site_id] = site_metrics
                    except UnifiSiteManagerRateLimitError as err:
                        _LOGGER.warning(
                            "Rate limit reached while updating metrics for site %s: %s",
                            site_id,
                            err,
                        )
                        continue
                    except UnifiSiteManagerAPIError as err:
                        _LOGGER.error(
                            "Error updating metrics for site %s: %s",
                            site_id,
                            err,
                        )
                        continue

                self.data["metrics"] = metrics
                _LOGGER.debug("Updated metrics for %s sites", len(metrics))

            except UnifiSiteManagerAPIError as err:
                self._available = False
                raise UpdateFailed(f"Error updating metrics: {err}") from err

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        try:
            # Update sites first as we need site IDs for metrics
            await self._async_update_sites()
            
            # Update hosts and metrics concurrently
            await asyncio.gather(
                self._async_update_hosts(),
                self._async_update_metrics(),
            )

            self._available = True
            self.data["last_update"] = datetime.utcnow()
            return self.data

        except UnifiSiteManagerConnectionError as err:
            self._available = False
            raise UpdateFailed(f"Connection error: {err}") from err
        except Exception as err:  # pylint: disable=broad-except
            self._available = False
            _LOGGER.exception("Unexpected error updating coordinator")
            raise UpdateFailed(f"Unexpected error: {err}") from err

    async def async_refresh_metrics(self) -> None:
        """Refresh only the metrics data."""
        await self._async_update_metrics()
        self.async_update_listeners()

    @property
    def available(self) -> bool:
        """Return coordinator availability."""
        return self._available

    def get_host(self, host_id: str) -> dict[str, Any] | None:
        """Get host data by ID."""
        return self.data.get("hosts", {}).get(host_id)

    def get_site(self, site_id: str) -> dict[str, Any] | None:
        """Get site data by ID."""
        return self.data.get("sites", {}).get(site_id)

    def get_site_metrics(self, site_id: str) -> dict[str, Any] | None:
        """Get metrics data for a site."""
        return self.data.get("metrics", {}).get(site_id)