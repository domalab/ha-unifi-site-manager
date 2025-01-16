"""Constants for the UniFi Site Manager integration."""
from __future__ import annotations

from datetime import timedelta
from typing import Final

DOMAIN: Final = "unifi_site_manager"
MANUFACTURER: Final = "Ubiquiti Inc."
DEFAULT_API_HOST: Final = "https://api.ui.com"
DEFAULT_SCAN_INTERVAL: Final = timedelta(minutes=1)

# Entry Config
CONF_API_KEY: Final = "api_key"
CONF_SITE_ID: Final = "site_id"

# Device Classes
DEVICE_CLASS_CLIENTS: Final = "clients"
DEVICE_CLASS_GATEWAY: Final = "gateway"
DEVICE_CLASS_NETWORK: Final = "network"
DEVICE_CLASS_PROTECT: Final = "protect"

# API Headers
UNIFI_API_HEADERS: Final = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

# Device Attributes
ATTR_MAC_ADDRESS: Final = "mac_address"
ATTR_IP_ADDRESS: Final = "ip_address"
ATTR_HOSTNAME: Final = "hostname"
ATTR_FIRMWARE_VERSION: Final = "firmware_version"
ATTR_MODEL: Final = "model"
ATTR_SERIAL_NUMBER: Final = "serial_number"
ATTR_LAST_SEEN: Final = "last_seen"
ATTR_IS_ONLINE: Final = "is_online"
ATTR_SITE_ID: Final = "site_id"
ATTR_SITE_NAME: Final = "site_name"
ATTR_HOST_ID: Final = "host_id"
ATTR_TYPE: Final = "type"
ATTR_RELEASE_CHANNEL: Final = "release_channel"

# ISP Metrics
ATTR_ISP_NAME: Final = "isp_name"
ATTR_ISP_ORGANIZATION: Final = "isp_organization"
ATTR_DOWNLOAD_SPEED: Final = "download_speed"
ATTR_UPLOAD_SPEED: Final = "upload_speed"
ATTR_LATENCY_AVG: Final = "latency_avg"
ATTR_LATENCY_MAX: Final = "latency_max"
ATTR_PACKET_LOSS: Final = "packet_loss"
ATTR_UPTIME: Final = "uptime"

# Site Statistics
ATTR_TOTAL_DEVICES: Final = "total_devices"
ATTR_OFFLINE_DEVICES: Final = "offline_devices"
ATTR_WIFI_CLIENTS: Final = "wifi_clients"
ATTR_WIRED_CLIENTS: Final = "wired_clients"
ATTR_GUEST_CLIENTS: Final = "guest_clients"

# Controller Types
CONTROLLER_TYPE_NETWORK: Final = "network"
CONTROLLER_TYPE_PROTECT: Final = "protect"
CONTROLLER_TYPE_ACCESS: Final = "access"
CONTROLLER_TYPE_TALK: Final = "talk"
CONTROLLER_TYPE_CONNECT: Final = "connect"
CONTROLLER_TYPE_INNERSPACE: Final = "innerspace"

# Controller States
CONTROLLER_STATE_ACTIVE: Final = "active"
CONTROLLER_STATE_INACTIVE: Final = "inactive"

# Error Messages
ERROR_AUTH_INVALID: Final = "invalid_auth"
ERROR_CANNOT_CONNECT: Final = "cannot_connect"
ERROR_UNKNOWN: Final = "unknown"

# Service Names
SERVICE_REFRESH: Final = "refresh"

# Entity Categories
ENTITY_CATEGORY_CONFIG: Final = "config"
ENTITY_CATEGORY_DIAGNOSTIC: Final = "diagnostic"
ENTITY_CATEGORY_SYSTEM: Final = "system"

# Icons
ICON_GATEWAY: Final = "mdi:router-wireless"
ICON_NETWORK: Final = "mdi:network"
ICON_CLIENTS: Final = "mdi:account-group"
ICON_PROTECT: Final = "mdi:camera"
ICON_SPEED_TEST: Final = "mdi:speedometer"
ICON_LATENCY: Final = "mdi:timer-outline"
ICON_PACKET_LOSS: Final = "mdi:connection"
ICON_UPTIME: Final = "mdi:clock-outline"

# Metric Types
METRIC_TYPE_5M: Final = "5m"
METRIC_TYPE_1H: Final = "1h"

# State Classes
STATE_CLASS_MEASUREMENT: Final = "measurement"
STATE_CLASS_TOTAL: Final = "total"
STATE_CLASS_TOTAL_INCREASING: Final = "total_increasing"

# Update Intervals
SCAN_INTERVAL_FAST: Final = timedelta(seconds=30)
SCAN_INTERVAL_NORMAL: Final = timedelta(minutes=1)
SCAN_INTERVAL_SLOW: Final = timedelta(minutes=5)
SCAN_INTERVAL_METRICS: Final = timedelta(minutes=5)

# Unit Conversions
KBPS_TO_MBPS: Final = 1000  # Convert Kbps to Mbps
MS_TO_S: Final = 1000  # Convert milliseconds to seconds

# Sensor Units
UNIT_BYTES_PER_SEC: Final = "B/s"
UNIT_KBPS: Final = "kbps"
UNIT_MBPS: Final = "Mbps"
UNIT_MS: Final = "ms"
UNIT_PERCENTAGE: Final = "%"

# Configuration
CONF_SCAN_INTERVAL = "scan_interval"
CONF_CACHE_TTL = "cache_ttl"
CONF_METRICS_INTERVAL = "metrics_interval"

# Defaults
DEFAULT_SCAN_INTERVAL = 60  # seconds
DEFAULT_CACHE_TTL = 300  # seconds
DEFAULT_METRICS_INTERVAL = 300  # seconds

# Services
SERVICE_REFRESH = "refresh"
SERVICE_CLEAR_CACHE = "clear_cache"
SERVICE_RESET_ERRORS = "reset_errors"
SERVICE_UPDATE_SITE = "update_site"
SERVICE_REBOOT_DEVICE = "reboot_device"