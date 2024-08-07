from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.discovery import async_load_platform

from .const import DOMAIN, LOGGER, DEFAULT_SCAN_INTERVAL
from .coodinator import MikanCoordinator

async def async_setup(hass: HomeAssistant, config: ConfigType):
    """Set up the component."""
    LOGGER.info("Ciallo～(∠・ω< )  Mikan-Ani")

    coordinator = MikanCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[0] = coordinator

    await async_load_platform(hass, 'sensor', DOMAIN, {
        "coordinator": coordinator
    }, {})

    async def async_update_data(now):
        await coordinator.async_request_refresh()

    async_track_time_interval(hass, async_update_data, DEFAULT_SCAN_INTERVAL)

    return True
