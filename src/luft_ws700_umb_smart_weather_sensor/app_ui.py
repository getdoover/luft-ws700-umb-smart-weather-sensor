from pydoover import ui

from .app_config import LuftWs700UmbSmartWeatherSensorConfig
from .utils import to_camel_case


class LuftWs700UmbSmartWeatherSensorUI:
    def __init__(self):
        # Build NumericVariables for all weather values that are enabled in config
        self._config = LuftWs700UmbSmartWeatherSensorConfig()
        # Mapping of config flag -> human-friendly label (matches CSV value_name)
        self._flag_to_label = {
            "show_rel_humidity_average": "Avg Relative humidity",
            "show_rel_air_pressure": "Avg Relative air pressure",
            "show_wind_direction_min": "Min Wind direction",
            "show_wind_direction_max": "Max Wind direction",
            "show_compass": "Compass",
            "show_precipitation_type": "Precipitation type",
            "show_wind_measurement_quality": "Wind measurement quality",
            "show_global_radiation_average": "AvgGlobal radiation",
            "show_air_temperature_average": "Air temperature (°C)",
            "show_wind_chill_temperature": "Wind chill-temperature (°C)",
            "show_heating_temperature_wind": "Heating temperature Wind (°C)",
            "show_heating_temperature_r2s": "Heating temperature R2S (°C)",
            "show_wind_speed_min": "Min Wind speed (m/s)",
            "show_wind_speed_max": "Max Wind speed (m/s)",
            "show_wind_speed_average": "Avg Wind speed (m/s)",
            "show_precipitation_absolute": "Precipitation absolute (mm)",
            "show_precipitation_different": "Precipitation different (mm)",
            "show_precipitation_intensive": "Precipitation intensive (mm/h)",
            "show_absolute_humidity_average": "Avg Absolute humidity",
            "show_mixing_ratio_average": "Avg Mixing ratio",
            "show_absolute_air_pressure_average": "Avg Absolute air pressure",
            "show_wind_speed_kmh_average": "Avg Wind speed (km/h)",
            "show_wind_speed_kts_min": "Min Wind speed (kts)",
            "show_wind_speed_kts_max": "Max Wind speed (kts)",
            "show_wind_speed_kts_average": "Avg Wind speed (kts)",
            "show_wind_speed_std_dev_ms": "Std Dev Wind speed (m/s)",
            "show_wind_speed_std_dev_mph": "Std Dev Wind speed (mph)",
            "show_wind_direction_std_dev": "Wind direction standard deviation",
            "show_wet_bulb_temperature_c_actual": "Wet bulb temperature (°C)",
            "show_wet_bulb_temperature_f_actual": "Wet bulb temperature (°F)",
            "show_specific_enthalpy_actual": "Specific enthalpy",
            "show_air_density_actual": "Air density (act)",
            "show_external_temperature_c_actual": "External temperature (°C)",
            "show_external_temperature_f_actual": "External temperature (°F)",
            "show_wind_value_quality_fast": "Wind value quality",
            "show_lightning_events_minute": "Lightning events (min)",
            "show_lightning_events_interval": "Lightning events (int.)",
        }

        self._variables: list[ui.NumericVariable] = []
        self._key_to_var: dict[str, ui.NumericVariable] = {}

        for flag_name, label in self._flag_to_label.items():
            # Resolve flag value; default to True if not present
            try:
                flag_obj = getattr(self._config, flag_name)
                flag_value = getattr(flag_obj, "value", None)
                is_enabled = bool(flag_value) if flag_value is not None else bool(flag_obj)
            except Exception:
                is_enabled = True

            if is_enabled:
                key = to_camel_case(label)
                # Default precision to 2; UI can adjust ranges later if desired
                var = ui.NumericVariable(key, label, precision=2)
                self._variables.append(var)
                self._key_to_var[key] = var

    def fetch(self):
        # Return all enabled weather variables so they can be added to the UI manager
        return tuple(self._variables)

    def update(self, values: dict | None = None, **kwargs):
        # Update variables using provided mapping or keyword args. Unknown keys are ignored.
        payload = {}
        if isinstance(values, dict):
            payload.update(values)
        if kwargs:
            payload.update(kwargs)

        for key, value in payload.items():
            var = self._key_to_var.get(str(key))
            if var is not None and value is not None:
                try:
                    var.update(float(value))
                except (TypeError, ValueError):
                    # Ignore non-numeric updates
                    continue
        return None
