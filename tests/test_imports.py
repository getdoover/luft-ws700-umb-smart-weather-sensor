"""
Basic tests for an application.

This ensures all modules are importable and that the config is valid.
"""

def test_import_app():
    from luft_ws700_umb_smart_weather_sensor.application import LuftWs700UmbSmartWeatherSensorApplication
    assert LuftWs700UmbSmartWeatherSensorApplication

def test_config():
    from luft_ws700_umb_smart_weather_sensor.app_config import LuftWs700UmbSmartWeatherSensorConfig

    config = LuftWs700UmbSmartWeatherSensorConfig()
    assert isinstance(config.to_dict(), dict)

def test_ui():
    from luft_ws700_umb_smart_weather_sensor.app_ui import LuftWs700UmbSmartWeatherSensorUI
    assert LuftWs700UmbSmartWeatherSensorUI

def test_state():
    from luft_ws700_umb_smart_weather_sensor.app_state import LuftWs700UmbSmartWeatherSensorState
    assert LuftWs700UmbSmartWeatherSensorState