from pathlib import Path

from pydoover import config
from pydoover.docker import ModbusConfig

from .utils import get_reg_names

class LuftWs700UmbSmartWeatherSensorConfig(config.Schema):
    def __init__(self):
        self.modbus_config = ModbusConfig("Modbus Config")
        
        reg_names = get_reg_names(Path(__file__).with_name("weather_registers.csv"))
        print("reg_names:", reg_names)
        for reg_name, label in reg_names.items():
            setattr(self, f"show_{reg_name}", config.Boolean(f"Show {label}", default=True))

def export():
    LuftWs700UmbSmartWeatherSensorConfig().export(Path(__file__).parents[2] / "doover_config.json", "luft_ws700_umb_smart_weather_sensor")

if __name__ == "__main__":
    export()
