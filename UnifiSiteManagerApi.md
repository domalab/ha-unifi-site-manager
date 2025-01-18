# Site Manager API Documentation

## Getting Started

The **Site Manager API** was created to enable developers to programmatically monitor and manage UniFi deployments at scale. It provides robust tools to access and control your UniFi devices’ data, allowing you to retrieve detailed information, monitor performance, and manage your network infrastructure efficiently.

### API Version

- **Version 0.1**: Focuses on extracting data from the UniFi Site Manager (unifi.ui.com).
- **Future Versions**: Will expand to include more granular configurations, allowing management of individual sites and the devices within those sites.

Your feedback is crucial in helping us enhance and customize the API to better meet your needs.

## Authentication

An **API Key** is a unique identifier used to authenticate API requests. These keys ensure secure access to your UniFi account and its associated devices. Each key is tied to the UI account that created it, enabling secure and personalized API interactions.

### Obtaining an API Key

1. Sign in to the UniFi Site Manager at [unifi.ui.com](https://unifi.ui.com).
2. From the left navigation bar, click on **API**.
3. Click **Create API Key**.
4. Copy the key and store it securely, as it will only be displayed once.
5. Click **Done** to ensure the key is hashed and securely stored.

### Using the API Key

Include the API key in the `X-API-Key` header.

**Example:**

```bash
curl -X GET 'https://api.ui.com/ea/hosts' \
  -H 'X-API-KEY: YOUR_API_KEY' \
  -H 'Accept: application/json'
```

## Rate Limiting

The API rate limit is set to **100 requests per minute**. Exceeding this limit will result in a `429 Too Many Requests` status code.

---

## API Endpoints

### List Hosts

#### GET `/ea/hosts`

Retrieve a list of all hosts associated with the UI account making the API call.

**Parameters:**

- `X-API-KEY` *(string, required)*: API key

**Example:**

```bash
curl -X GET 'https://api.ui.com/ea/hosts' \
  -H 'Accept: application/json' \
  -H 'X-API-KEY: YOUR_API_KEY'
```

**Responses:**

- `200 OK`

  ```json
  {
    "data": [
      {
        "hardwareId": "eae0f123-0000-5111-b111-f833f56eade5",
        "id": "900A6F00301100000000074A6BA90000000007A3387E0000000063EC9853:123456789",
        "ipAddress": "192.168.220.114",
        "isBlocked": false,
        "lastConnectionStateChange": "2024-06-23T03:59:52Z",
        "latestBackupTime": "2024-06-22T11:55:10Z",
        "owner": true,
        "registrationTime": "2024-04-17T07:27:14Z",
        "reportedState": {
          "anonid": "c2705509-58a5-40c9-8b2e-d29c8574ff08",
          "apps": [
            {
              "controllerStatus": "READY",
              "name": "users",
              "port": 9080,
              "swaiVersion": 2,
              "type": "app",
              "version": "1.8.42+3695"
            }
          ],
          "availableChannels": [
            "release",
            "beta",
            "release-candidate"
          ],
          "controller_uuid": "900A6F00301100000000074A6BA90000000007A3387E0000000063EC9853:123456789",
          "controllers": [
            {
              "controllerStatus": "READY",
              "installState": "installed",
              "isConfigured": true,
              "name": "network",
              "port": 8081,
              "releaseChannel": "beta",
              "status": "ok",
              "swaiVersion": 3,
              "type": "controller",
              "version": "8.4.20"
            }
          ],
          "deviceState": "setup",
          "directConnectDomain": "f4e2c6c23f1307bc5608082112aa0651cbf10.id.ui.direct",
          "firmwareUpdate": {
            "latestAvailableVersion": null
          },
          "hardware": {
            "name": "UniFi Dream Machine SE",
            "mac": "F4E2C6C23F13",
            "serialno": "f4e2c6c23f13",
            "uuid": "eae0f123-0000-5111-b111-f833f56eade5"
          },
          "state": "connected",
          "timezone": "Europe/Riga"
        },
        "type": "console"
      }
    ],
    "httpStatusCode": 200
  }
  ```

- `401 Unauthorized`

  ```json
  {
    "code": "unauthorized",
    "httpStatusCode": 401,
    "message": "unauthorized"
  }
  ```

- `429 Rate Limit Exceeded`

  ```json
  {
    "code": "rate_limit",
    "httpStatusCode": 429,
    "message": "rate limit exceeded, retry after 5.372786998s"
  }
  ```

---

### Get Host by ID

#### GET `/ea/hosts/{id}`

Retrieve detailed information about a specific host by ID.

**Parameters:**

- `id` *(string, required)*: Host ID
- `X-API-KEY` *(string, required)*: API key

**Example:**

```bash
curl -X GET 'https://api.ui.com/ea/hosts/{id}' \
  -H 'Accept: application/json' \
  -H 'X-API-KEY: YOUR_API_KEY'
```

**Responses:**

- `200 OK`

  ```json
  {
    "data": {
      "hardwareId": "eae0f123-0000-5111-b111-f833f56eade5",
      "id": "900A6F00301100000000074A6BA90000000007A3387E0000000063EC9853:123456789",
      "ipAddress": "192.168.220.114",
      "isBlocked": false,
      "lastConnectionStateChange": "2024-06-23T03:59:52Z",
      "latestBackupTime": "2024-06-22T11:55:10Z",
      "owner": true,
      "registrationTime": "2024-04-17T07:27:14Z",
      "reportedState": {
        "controllerStatus": "READY",
        "deviceState": "connected",
        "timezone": "Europe/Riga"
      },
      "type": "console"
    },
    "httpStatusCode": 200
  }
  ```

- `404 Not Found`

  ```json
  {
    "code": "NOT_FOUND",
    "httpStatusCode": 404,
    "message": "thing not found"
  }
  ```

---

### List Sites

#### GET `/ea/sites`

Retrieve a list of all sites associated with the UI account.

**Parameters:**

- `X-API-KEY` *(string, required)*: API key

**Example:**

```bash
curl -X GET 'https://api.ui.com/ea/sites' \
  -H 'Accept: application/json' \
  -H 'X-API-KEY: YOUR_API_KEY'
```

**Responses:**

- `200 OK`

  ```json
  {
    "data": [
      {
        "hostId": "900A6F00301100000000074A6BA90000000007A3387E0000000063EC9853:123456789",
        "isOwner": true,
        "meta": {
          "desc": "Default",
          "gatewayMac": "f4:e2:c6:c2:3f:13",
          "name": "default",
          "timezone": "Europe/Riga"
        },
        "permission": "admin",
        "siteId": "661900ae6aec8f548d49fd54"
      }
    ],
    "httpStatusCode": 200
  }
  ```

---

### List Devices

#### GET `/ea/devices`

Retrieve a list of UniFi devices managed by hosts where the UI account is an owner or super admin.

**Parameters:**

- `hostIds[]` *(array[string], optional)*: List of host IDs
- `time` *(string, optional)*: Last processed timestamp of devices
- `X-API-KEY` *(string, required)*: API key

**Example:**

```bash
curl -X GET 'https://api.ui.com/ea/devices?hostIds[]=HOST_ID' \
  -H 'Accept: application/json' \
  -H 'X-API-KEY: YOUR_API_KEY'
```

**Responses:**

- `200 OK`

  ```json
  {
    "data": [
      {
        "devices": [
          {
            "adoptionTime": null,
            "firmwareStatus": "upToDate",
            "id": "F4E2C6C23F13",
            "ip": "192.168.1.226",
            "isConsole": true,
            "isManaged": true,
            "mac": "F4E2C6C23F13",
            "model": "UDM SE",
            "name": "unifi.yourdomain.com",
            "status": "online",
            "version": "4.0.6"
          }
        ]
      }
    ],
    "httpStatusCode": 200
  }
  ```

- `400 Invalid Parameter`

  ```json
  {
    "code": "parameter_invalid",
    "httpStatusCode": 400,
    "message": "invalid time format: 2024-04-24"
  }
  ```

---

### ISP Metrics

#### GET `/ea/isp-metrics/{type}`

Retrieve ISP metrics data for all sites linked to the API key.

**Parameters:**

- `type` *(string, required)*: Specify `5m` or `1h` intervals
- `beginTimestamp` *(string, optional)*: Start timestamp
- `endTimestamp` *(string, optional)*: End timestamp
- `duration` *(string, optional)*: Specifies the time range (e.g., `24h`, `7d`, `30d`)
- `X-API-KEY` *(string, required)*: API key

**Example:**

```bash
curl -X GET 'https://api.ui.com/ea/isp-metrics/5m?beginTimestamp=START&endTimestamp=END' \
  -H 'Accept: application/json' \
  -H 'X-API-KEY: YOUR_API_KEY'
```

**Responses:**

- `200 OK`

  ```json
  {
    "data": [
      {
        "metricType": "5m",
        "periods": [
          {
            "data": {
              "wan": {
                "avgLatency": 1,
                "download_kbps": 0,
                "packetLoss": 0,
                "upload_kbps": 0,
                "uptime": 100
              }
            },
            "metricTime": "2024-06-30T13:35:00Z"
          }
        ]
      }
    ],
    "httpStatusCode": 200
  }
  ```

- `400 Invalid Parameter`

  ```json
  {
    "code": "parameter_invalid",
    "httpStatusCode": 400,
    "message": "invalid beginTimestamp format: 2024-06-30"
  }
  ```

---

## Error Codes

- `401 Unauthorized`: Authentication failed.
- `429 Too Many Requests`: Rate limit exceeded.
- `500 Internal Server Error`: Server encountered an error.
- `502 Bad Gateway`: Issue with server communication.

---

For detailed examples and use cases, refer to the [official documentation](https://unifi.ui.com/docs).
