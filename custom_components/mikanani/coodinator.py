"""Coordinator for mikanani."""

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    MIKAN_HOST,
    LOGGER,
    DEFAULT_SCAN_INTERVAL,
)
from .mikan import MikanBangumi, MikanHTMLParser, MikanParseResult


class MikanCoordinator(DataUpdateCoordinator[MikanParseResult]):
    """Class to manage fetching mikanani data."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize."""
        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )

        self._parser = MikanHTMLParser()

    async def update_token(self):
        pass

    async def _async_request(self):
        async with aiohttp.ClientSession() as session:
            async with session.request("GET", MIKAN_HOST) as response:
                return await response.text(encoding="UTF-8")

    async def _async_update_data(self) -> MikanParseResult:
        parser = MikanHTMLParser()

        try:
            html_text = await self._async_request()
            parser.feed(html_text)
        except Exception as err:
            LOGGER.exception(err)
            raise UpdateFailed(err) from err

        return parser.parse_result
