"""Config flow for Mullvad VPN integration."""
from mullvad_async import Mullvad, MullvadAPIError

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Mullvad VPN."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        self._async_abort_entries_match()

        errors = {}
        if user_input is not None:
            try:
                mullvad_client = Mullvad(async_get_clientsession(self.hass))
                await self.hass.async_add_executor_job(mullvad_client.is_connected)
            except MullvadAPIError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title="Mullvad VPN", data=user_input)

        return self.async_show_form(step_id="user", errors=errors)
