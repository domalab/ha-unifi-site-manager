# UniFi Site Manager Integration for Home Assistant

[![HACS Integration][hacsbadge]][hacs]
[![GitHub Last Commit](https://img.shields.io/github/last-commit/domalab/ha-unifi-site-manager?style=for-the-badge)](https://github.com/domalab/ha-unifi-site-manager/commits/main)
[![License](https://img.shields.io/github/license/domalab/ha-unifi-site-manager?style=for-the-badge)](./LICENSE)

A Home Assistant integration for UniFi's Site Manager API, providing comprehensive monitoring of UniFi sites, hosts, and network performance metrics.

## Features

- 🌐 Monitor all your UniFi sites from a single dashboard
- 📊 Track network performance metrics (download/upload speeds, latency, packet loss)
- 📡 Monitor UniFi host status and controller states
- 🔄 Real-time updates with configurable update intervals
- 🚨 Track device connectivity and updates availability

## Installation

### HACS (Recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=domalab&repository=ha-unifi-site-manager&category=integration)

### Manual Installation

1. Copy the `custom_components/unifi_site_manager` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to Home Assistant's Integrations page
2. Click "Add Integration"
3. Search for "UniFi Site Manager"
4. Follow the configuration steps:
   - Enter your UniFi Site Manager API key
   - The integration will automatically discover your sites and create entities

### Getting an API Key

1. Log in to your UniFi account at unifi.ui.com
2. Navigate to Settings
3. Select the "API Key" section
4. Create a new API key
5. Copy the key immediately (it will only be shown once)

## Available Entities

### Sensors

- Download Speed (Mbps)
- Upload Speed (Mbps)
- Average Latency (ms)
- Maximum Latency (ms)
- Packet Loss (%)
- WAN Uptime (%)
- Total Devices

### Binary Sensors

- Site Online Status
- All Devices Online Status
- Updates Available
- Host Connection Status
- Network Controller Status
- Protect Controller Status

## Services

### unifi_site_manager.refresh

Force an immediate refresh of the integration data.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| refresh_type | string | "all" | Type of data to refresh: "all", "sites", "hosts", or "metrics" |

## API Rate Limiting

The UniFi Site Manager API has a rate limit of 100 requests per minute. The integration handles this automatically by:

- Tracking remaining API calls
- Implementing backoff when limits are reached
- Efficiently batching requests where possible

## Troubleshooting

1. **Integration Not Updating**: Check your API key permissions and network connectivity
2. **API Rate Limits**: Increase update intervals if you're managing many sites
3. **Missing Data**: Verify your UniFi account has access to the expected sites
4. **Authentication Errors**: Ensure your API key is valid and has the necessary permissions

## Contributions

This project welcomes contributions and suggestions. Please fork the repository and submit a pull request with your suggested changes.

## License

This project is licensed under the Apache License - see the LICENSE file for details.

---

[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
