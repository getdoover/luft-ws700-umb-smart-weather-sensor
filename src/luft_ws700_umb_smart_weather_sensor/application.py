import logging
import time
from pathlib import Path
from typing import Dict, Tuple

from pydoover.docker import Application
from pydoover import ui

from .app_config import LuftWs700UmbSmartWeatherSensorConfig
from .app_ui import LuftWs700UmbSmartWeatherSensorUI
from .utils import load_modbus_register_map

log = logging.getLogger()

class LuftWs700UmbSmartWeatherSensorApplication(Application):
    config: LuftWs700UmbSmartWeatherSensorConfig  # not necessary, but helps your IDE provide autocomplete!

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.started: float = time.time()
        self._register_start_address: int | None = None
        self._register_count: int | None = None
        # address -> (tag_key, scale, is_signed)
        self._address_to_meta: Dict[int, Tuple[str, float, bool]] = {}

    async def setup(self):
        self.ui = LuftWs700UmbSmartWeatherSensorUI(self.config)
        self.ui_manager.add_children(*self.ui.fetch())

        # Load register map from CSV via utils
        csv_path = Path(__file__).with_name("weather_registers.csv")
        start_address, register_count, address_to_meta = load_modbus_register_map(csv_path)
        if register_count == 0:
            log.warning("No Modbus registers loaded from weather_registers.csv")
        self._register_start_address = start_address
        self._register_count = register_count
        self._address_to_meta = address_to_meta

    async def main_loop(self):
        # If no registers configured, idle briefly
        if not self._register_count:
            await self.wait_for_interval(2)
            return

        # Single read across the full address span
        values = await self.modbus_iface.read_registers(
            bus_id="default",
            modbus_id=1,
            start_address=self._register_start_address,
            num_registers=self._register_count,
            register_type=4,
            configure_bus=True,
        )
        tags: Dict[str, float] = {}
        
        if isinstance(values, list):
            for address, (tag_key, scale, is_signed) in self._address_to_meta.items():
                idx = address - int(self._register_start_address)
                if 0 <= idx < len(values):
                    raw = int(values[idx])
                    if is_signed:
                        raw = raw - 0x10000 if raw & 0x8000 else raw
                    try:
                        converted = raw / scale if scale else float(raw)
                    except ZeroDivisionError:
                        converted = float(raw)
                    tags[tag_key] = converted
        elif isinstance(values, int):
            # Degenerate case: only one register requested
            address = int(self._register_start_address)
            meta = self._address_to_meta.get(address)
            if meta:
                tag_key, scale, is_signed = meta
                raw = int(values)
                if is_signed:
                    raw = raw - 0x10000 if raw & 0x8000 else raw
                converted = raw / scale if scale else float(raw)
                tags[tag_key] = converted

        if tags:
            self.set_tags(tags)

        self.ui.update()
        await self.wait_for_interval(2)
