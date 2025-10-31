from pydoover import ui

from .app_config import LuftWs700UmbSmartWeatherSensorConfig
from .utils import to_camel_case, get_reg_names
from pathlib import Path


class LuftWs700UmbSmartWeatherSensorUI:
    def __init__(self, config):
        # Build NumericVariables for all weather values that are enabled in config
        self._config = config
        self._reg_names = get_reg_names(Path(__file__).with_name("weather_registers.csv"))
        
        for flag_name, label in self._reg_names.items():
            print(f"flag_name: {flag_name}, label: {label}")
            if not hasattr(self._config, f"show_{flag_name}"):
                print(f"no show_{flag_name} attribute found")
                continue
            var = ui.NumericVariable(flag_name, label, precision=2, hidden=(not getattr(self._config, f"show_{flag_name}").value))
            setattr(self, flag_name, var)

    def fetch(self):
        ui_vars = []
        for name in self._reg_names.keys():
            var = getattr(self, name, None)
            if var is not None:
                ui_vars.append(var)
        return tuple(ui_vars)

    def update(self, values: dict | None = None, **kwargs):
        # Update variables using provided mapping or keyword args. Unknown keys are ignored.
        payload = {}
        if isinstance(values, dict):
            payload.update(values)
        if kwargs:
            payload.update(kwargs)
        
        for key, value in payload.items():
            var = getattr(self, str(key), None)
            if var is None:
                continue
            else:
                var.update(float(value))
        return None
