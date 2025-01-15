"""Support for UniFi Site Manager sensors."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Final

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    UnitOfDataRate,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import (
    ATTR_DOWNLOAD_SPEED,
    ATTR_ISP_NAME,
    ATTR_LATENCY_AVG,
    ATTR_LATENCY_MAX,
    ATTR_PACKET_LOSS,
    ATTR_TOTAL_DEVICES,
    ATTR_UPLOAD_SPEED,
    ATTR_UPTIME,
    DOMAIN,
    ICON_CLIENTS,
    ICON_LATENCY,
    ICON_PACKET_LOSS,
    ICON_SPEED_TEST,
    ICON_UPTIME,
    KBPS_TO_MBPS,
    STATE_CLASS_MEASUREMENT,
)
from .entity import UnifiSiteManagerSiteEntity


@dataclass(frozen=True, kw_only=True)
class UnifiSensorEntityDescription(SensorEntityDescription):
    """Class describing UniFi sensor entities."""

    value_fn: Callable[[dict[str, Any]], StateType | datetime]


SITE_SENSORS: Final[tuple[UnifiSensorEntityDescription, ...]] = (
    UnifiSensorEntityDescription(
        key="download_speed",
        translation_key="download_speed",
        icon=ICON_SPEED_TEST,
        native_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=STATE_CLASS_MEASUREMENT,
        value_fn=lambda data: data.get("wan", {}).get("download_kbps", 0) / KBPS_TO_MBPS,
    ),
    UnifiSensorEntityDescription(
        key="upload_speed",
        translation_key="upload_speed",
        icon=ICON_SPEED_TEST,
        native_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=STATE_CLASS_MEASUREMENT,
        value_fn=lambda data: data.get("wan", {}).get("upload_kbps", 0) / KBPS_TO_MBPS,
    ),
    UnifiSensorEntityDescription(
        key="latency_average",
        translation_key="latency_average",
        icon=ICON_LATENCY,
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        device_class=SensorDeviceClass.DURATION,
        state_class=STATE_CLASS_MEASUREMENT,
        value_fn=lambda data: data.get("wan", {}).get("avgLatency"),
    ),
    UnifiSensorEntityDescription(
        key="latency_max",
        translation_key="latency_max",
        icon=ICON_LATENCY,
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        device_class=SensorDeviceClass.DURATION,
        state_class=STATE_CLASS_MEASUREMENT,
        value_fn=lambda data: data.get("wan", {}).get("maxLatency"),
    ),
    UnifiSensorEntityDescription(
        key="packet_loss",
        translation_key="packet_loss",
        icon=ICON_PACKET_LOSS,
        native_unit_of_measurement=PERCENTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
        value_fn=lambda data: data.get("wan", {}).get("packetLoss", 0),
    ),
    UnifiSensorEntityDescription(
        key="uptime",
        translation_key="uptime",
        icon=ICON_UPTIME,
        native_unit_of_measurement=PERCENTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
        value_fn=lambda data: data.get("wan", {}).get("uptime", 0),
    ),
    UnifiSensorEntityDescription(
        key="total_devices",
        translation_key="total_devices",
        icon=ICON_CLIENTS,
        state_class=STATE_CLASS_MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("counts", {}).get("totalDevice", 0),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the UniFi Site Manager sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities: list[UnifiSiteManagerSensor] = []

    # Add site-level sensors
    for site_id, site_data in coordinator.data["sites"].items():
        for description in SITE_SENSORS:
            site_metrics = coordinator.get_site_metrics(site_id)
            if site_metrics and site_metrics[0].get("data"):
                entities.append(
                    UnifiSiteManagerSensor(
                        coordinator=coordinator,
                        description=description,
                        site_id=site_id,
                    )
                )

    async_add_entities(entities)


class UnifiSiteManagerSensor(UnifiSiteManagerSiteEntity, SensorEntity):
    """Representation of a UniFi Site Manager Sensor."""

    entity_description: UnifiSensorEntityDescription

    @property
    def native_value(self) -> StateType | datetime:
        """Return the state of the sensor."""
        metrics = self.site_metrics
        if not metrics:
            return None
        
        return self.entity_description.value_fn(metrics)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        metrics = self.site_metrics
        if not metrics:
            return {}
        
        metrics_data = metrics.get("wan", {})
        site_data = self.site_data or {}
        
        return {
            ATTR_ISP_NAME: metrics_data.get("ispName"),
            ATTR_DOWNLOAD_SPEED: metrics_data.get("download_kbps"),
            ATTR_UPLOAD_SPEED: metrics_data.get("upload_kbps"),
            ATTR_LATENCY_AVG: metrics_data.get("avgLatency"),
            ATTR_LATENCY_MAX: metrics_data.get("maxLatency"),
            ATTR_PACKET_LOSS: metrics_data.get("packetLoss"),
            ATTR_UPTIME: metrics_data.get("uptime"),
            ATTR_TOTAL_DEVICES: site_data.get("statistics", {}).get("counts", {}).get("totalDevice", 0),
        }