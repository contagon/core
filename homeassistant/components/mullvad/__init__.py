"""The Mullvad VPN integration."""
from datetime import timedelta
import logging

from mullvad_async import Mullvad

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import update_coordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN

PLATFORMS = [Platform.BINARY_SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Mullvad VPN integration."""

    mullvad_client = Mullvad(async_get_clientsession(hass))

    coordinator: update_coordinator.DataUpdateCoordinator = (
        update_coordinator.DataUpdateCoordinator(
            hass,
            logging.getLogger(__name__),
            name=DOMAIN,
            update_method=mullvad_client.is_connected,
            update_interval=timedelta(minutes=1),
        )
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        del hass.data[DOMAIN]

    return unload_ok
