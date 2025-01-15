"""Base entity for the UniFi Site Manager integration."""
from __future__ import annotations

from typing import Any

from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import UnifiSiteManagerDataUpdateCoordinator


class UnifiSiteManagerEntity(CoordinatorEntity[UnifiSiteManagerDataUpdateCoordinator]):
    """Base entity for UniFi Site Manager integration."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: UnifiSiteManagerDataUpdateCoordinator,
        description: EntityDescription,
        site_id: str | None = None,
        host_id: str | None = None,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.entity_description = description
        self._site_id = site_id
        self._host_id = host_id

        # Set unique_id based on what type of entity this is
        if site_id:
            self._attr_unique_id = f"{site_id}_{description.key}"
            site_data = coordinator.get_site(site_id)
            name = site_data.get("meta", {}).get("name", site_id)
            stats = site_data.get("statistics", {})
            
            self._attr_device_info = DeviceInfo(
                identifiers={(DOMAIN, site_id)},
                name=name,
                manufacturer=MANUFACTURER,
                model="UniFi Site",
                entry_type=DeviceEntryType.SERVICE,
                configuration_url=f"https://unifi.ui.com/site/{site_id}",
                sw_version=stats.get("firmwareVersion"),
                suggested_area="Network",
            )
        elif host_id:
            self._attr_unique_id = f"{host_id}_{description.key}"
            host_data = coordinator.get_host(host_id)
            if not host_data:
                return
            
            name = host_data.get("hostname") or host_data.get("name", host_id)
            reported_state = host_data.get("reportedState", {})
            hw_data = reported_state.get("hardware", {})
            
            self._attr_device_info = DeviceInfo(
                identifiers={(DOMAIN, host_id)},
                name=name,
                manufacturer=MANUFACTURER,
                model=hw_data.get("name", "UniFi Device"),
                hw_version=str(hw_data.get("hwrev", "")),
                sw_version=hw_data.get("firmwareVersion", ""),
                serial_number=hw_data.get("serialno", ""),
                configuration_url=f"https://{reported_state.get('hostname', '')}",
                suggested_area="Network",
                via_device=(DOMAIN, host_data.get("parentId")) if host_data.get("parentId") else None,
            )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self._site_id:
            site_data = self.coordinator.get_site(self._site_id)
            if not site_data:
                self._attr_available = False
                self.async_write_ha_state()
                return
        elif self._host_id:
            host_data = self.coordinator.get_host(self._host_id)
            if not host_data:
                self._attr_available = False
                self.async_write_ha_state()
                return

        self._attr_available = True
        self.async_write_ha_state()

    @property
    def site_data(self) -> dict[str, Any] | None:
        """Get site data."""
        if not self._site_id:
            return None
        return self.coordinator.get_site(self._site_id)

    @property
    def host_data(self) -> dict[str, Any] | None:
        """Get host data."""
        if not self._host_id:
            return None
        return self.coordinator.get_host(self._host_id)

    @property
    def site_metrics(self) -> dict[str, Any] | None:
        """Get site metrics."""
        if not self._site_id:
            return None
        metrics = self.coordinator.get_site_metrics(self._site_id)
        if not metrics or not metrics[0].get("data"):
            return None
        return metrics[0]["data"]


class UnifiSiteManagerSiteEntity(UnifiSiteManagerEntity):
    """Base entity for UniFi Site Manager site entities."""

    def __init__(
        self,
        coordinator: UnifiSiteManagerDataUpdateCoordinator,
        description: EntityDescription,
        site_id: str,
    ) -> None:
        """Initialize the site entity."""
        super().__init__(coordinator, description, site_id=site_id)


class UnifiSiteManagerHostEntity(UnifiSiteManagerEntity):
    """Base entity for UniFi Site Manager host entities."""

    def __init__(
        self,
        coordinator: UnifiSiteManagerDataUpdateCoordinator,
        description: EntityDescription,
        host_id: str,
    ) -> None:
        """Initialize the host entity."""
        super().__init__(coordinator, description, host_id=host_id)