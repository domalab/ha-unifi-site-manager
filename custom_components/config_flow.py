"""Config flow for UniFi Site Manager integration."""
from __future__ import annotations

import logging
import re
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .api import (
    UnifiSiteManagerAPI,
    UnifiSiteManagerAuthError,
    UnifiSiteManagerConnectionError,
)
from .const import DEFAULT_API_HOST, DOMAIN, ERROR_AUTH_INVALID, ERROR_CANNOT_CONNECT

_LOGGER = logging.getLogger(__name__)

API_KEY_PATTERN = re.compile(r"^[a-zA-Z0-9]{32,}$")

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): vol.All(
            str,
            vol.Length(min=32),
            vol.Match(API_KEY_PATTERN, msg="Invalid API key format"),
        ),
    }
)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    api = UnifiSiteManagerAPI(
        hass=hass,
        api_key=data[CONF_API_KEY],
        host=DEFAULT_API_HOST,
    )

    # Try to get the sites to validate the API key
    await api.async_validate_api_key()

    # Return info to store in the config entry.
    return {"title": "UniFi Site Manager"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for UniFi Site Manager."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except UnifiSiteManagerAuthError:
                errors["base"] = ERROR_AUTH_INVALID
            except UnifiSiteManagerConnectionError:
                errors["base"] = ERROR_CANNOT_CONNECT
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(user_input[CONF_API_KEY])
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )


    async def async_step_reauth(self, entry_data: dict[str, Any]) -> FlowResult:
        """Handle reauthorization request."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle reauthorization confirmation."""
        errors = {}

        if user_input is not None:
            try:
                await validate_input(self.hass, user_input)
            except UnifiSiteManagerAuthError:
                errors["base"] = ERROR_AUTH_INVALID
            except UnifiSiteManagerConnectionError:
                errors["base"] = ERROR_CANNOT_CONNECT
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Get the existing entry
                existing_entry = await self.async_set_unique_id(user_input[CONF_API_KEY])
                if existing_entry:
                    self.hass.config_entries.async_update_entry(
                        existing_entry,
                        data=user_input,
                    )
                    await self.hass.config_entries.async_reload(existing_entry.entry_id)
                    return self.async_abort(reason="reauth_successful")

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )