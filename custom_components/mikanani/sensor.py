from __future__ import annotations


from homeassistant.components.sensor import (
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    LOGGER,
    ATTRIBUTION,
)
from .coodinator import MikanCoordinator


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    if discovery_info is None:
        return

    coordinator = discovery_info.get("coordinator")
    if coordinator is None:
        return

    async_add_entities([MikanSensor(coordinator)])


class MikanSensor(CoordinatorEntity[MikanCoordinator], SensorEntity):
    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(self, coordinator: MikanCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            name="Mikanani",
        )

    @property
    def name(self):
        return "bangumi map"

    @property
    def state(self):
        data : dict = self.coordinator.data
        return sum([len(data[key]) for key in data.keys()])

    @property
    def unique_id(self):
        return f"{DOMAIN}_bangumi_map_sensor"

    @property
    def device_state_attributes(self):
        return {}

    @property
    def extra_state_attributes(self):
        return self.coordinator.data

    async def async_update(self):
        await self.coordinator.async_request_refresh()
