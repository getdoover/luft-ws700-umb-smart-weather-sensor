from pathlib import Path

from pydoover import config
from pydoover.docker import ModbusConfig

class LuftWs700UmbSmartWeatherSensorConfig(config.Schema):
    def __init__(self):
        self.modbus_config = ModbusConfig("Modbus Config")
        
        self.show_rel_humidity_average = config.Boolean("Show Relative Humidity Average", default=False)
        self.show_rel_air_pressure = config.Boolean("Show Relative Air Pressure", default=False)
        self.show_wind_direction_min = config.Boolean("Show Wind Direction Min", default=False)
        self.show_wind_direction_max = config.Boolean("Show Wind Direction Max", default=False)
        self.show_compass = config.Boolean("Show Compass", default=False)
        self.show_precipitation_type = config.Boolean("Show Precipitation Type", default=False)
        self.show_wind_measurement_quality = config.Boolean("Show Wind Measurement Quality", default=False)
        self.show_global_radiation_average = config.Boolean("Show Global Radiation Average", default=False)
        self.show_air_temperature_average = config.Boolean("Show Air Temperature Average", default=False)
        self.show_wind_chill_temperature = config.Boolean("Show Wind Chill Temperature", default=False)
        self.show_heating_temperature_wind = config.Boolean("Show Heating Temperature Wind", default=False)
        self.show_heating_temperature_r2s = config.Boolean("Show Heating Temperature R2S", default=False)
        self.show_wind_speed_min = config.Boolean("Show Wind Speed Min", default=False)
        self.show_wind_speed_max = config.Boolean("Show Wind Speed Max", default=False)
        self.show_wind_speed_average = config.Boolean("Show Wind Speed Average", default=False)
        self.show_precipitation_absolute = config.Boolean("Show Precipitation Absolute", default=False)
        self.show_precipitation_different = config.Boolean("Show Precipitation Different", default=False)
        self.show_precipitation_intensive = config.Boolean("Show Precipitation Intensive", default=False)
        self.show_absolute_humidity_average = config.Boolean("Show Absolute Humidity Average", default=False)
        self.show_mixing_ratio_average = config.Boolean("Show Mixing Ratio Average", default=False)
        self.show_absolute_air_pressure_average = config.Boolean("Show Absolute Air Pressure Average", default=False)
        self.show_wind_speed_kmh_average = config.Boolean("Show Wind Speed km/h Average", default=False)
        self.show_wind_speed_kts_min = config.Boolean("Show Wind Speed kts Min", default=False)
        self.show_wind_speed_kts_max = config.Boolean("Show Wind Speed kts Max", default=False)
        self.show_wind_speed_kts_average = config.Boolean("Show Wind Speed kts Average", default=False)
        self.show_wind_speed_std_dev_ms = config.Boolean("Show Wind Speed Standard Deviation (m/s)", default=False)
        self.show_wind_speed_std_dev_mph = config.Boolean("Show Wind Speed Standard Deviation (mph)", default=False)
        self.show_wind_direction_std_dev = config.Boolean("Show Wind Direction Standard Deviation", default=False)
        self.show_wet_bulb_temperature_c_actual = config.Boolean("Show Wet Bulb Temperature °C Actual", default=False)
        self.show_wet_bulb_temperature_f_actual = config.Boolean("Show Wet Bulb Temperature °F Actual", default=False)
        self.show_specific_enthalpy_actual = config.Boolean("Show Specific Enthalpy Actual", default=False)
        self.show_air_density_actual = config.Boolean("Show Air Density Actual", default=False)
        self.show_external_temperature_c_actual = config.Boolean("Show External Temperature °C Actual", default=False)
        self.show_external_temperature_f_actual = config.Boolean("Show External Temperature °F Actual", default=False)
        self.show_wind_value_quality_fast = config.Boolean("Show Wind Value Quality Fast", default=False)
        self.show_lightning_events_minute = config.Boolean("Show Lightning Events Minute", default=False)
        self.show_lightning_events_interval = config.Boolean("Show Lightning Events Interval", default=False)

def export():
    LuftWs700UmbSmartWeatherSensorConfig().export(Path(__file__).parents[2] / "doover_config.json", "luft_ws700_umb_smart_weather_sensor")

if __name__ == "__main__":
    export()
