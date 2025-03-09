import logging
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry

from .api import get_last_status, get_jobs
from .const import CONF_API_URL, CONF_API_KEY, ERROR, SUCCESS

_LOGGER = logging.getLogger(__name__)
DOMAIN = "cronicle"
SCAN_INTERVAL = timedelta(seconds=30)


async def async_setup_entry(hass, config_entry: ConfigEntry, async_add_entities):
    api_url = config_entry.data[CONF_API_URL]
    api_token = config_entry.data[CONF_API_KEY]

    jobs = await get_jobs(api_url, api_token)

    sensors = (CronicleJobSensor(api_url, api_token, el['title'], el['id'], config_entry) for el in jobs)
    async_add_entities(sensors,
                       update_before_add=True)


class CronicleJobSensor(SensorEntity):
    def __init__(self, api_url, api_token, name, cronicle_id, config_entry):
        self._state = None
        self._name = name
        self._cronicle_id = cronicle_id
        self._api_url = api_url
        self._api_token = api_token
        self._config_entry = config_entry

    @property
    def name(self):
        return self._name

    @property
    def native_value(self):
        return self._state

    @property
    def device_class(self):
        return SensorDeviceClass.ENUM

    @property
    def options(self):
        return [SUCCESS, ERROR]

    @property
    def icon(self):
        return 'mdi:information-outline'

    async def async_update(self):
        try:
            response = await get_last_status(self._api_url, self._api_token, self._cronicle_id)
            # Extract the sensor value from the response
            self._state = 'Error' if response['code'] > 0 else 'Success'

        except:
            _LOGGER.error("Error fetching data from API", self._cronicle_id, self._api_token, self._api_url)
            self._state = None
