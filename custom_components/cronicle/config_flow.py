import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, CONF_API_URL, CONF_API_KEY, CONF_INSTANCE_NAME


class CronicleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            api_url = user_input[CONF_API_URL]

            if not api_url.startswith("http://") and not api_url.startswith("https://"):
                errors["base"] = "invalid_url"

            if not errors:
                return self.async_create_entry(title=user_input[CONF_INSTANCE_NAME], data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_INSTANCE_NAME, default="Cronicle"): str,
                vol.Required(CONF_API_URL): str,
                vol.Required(CONF_API_KEY): str
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)