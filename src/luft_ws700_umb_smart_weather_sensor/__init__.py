from pydoover.docker import run_app

from .application import LuftWs700UmbSmartWeatherSensorApplication
from .app_config import LuftWs700UmbSmartWeatherSensorConfig

def main():
    """
    Run the application.
    """
    run_app(LuftWs700UmbSmartWeatherSensorApplication(config=LuftWs700UmbSmartWeatherSensorConfig()))
