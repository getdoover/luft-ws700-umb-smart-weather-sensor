import csv
from pathlib import Path
from typing import Dict, Tuple


def to_camel_case(name: str) -> str:
    cleaned = ''.join(ch for ch in name if ch.isalnum() or ch.isspace())
    parts = [p for p in cleaned.strip().split() if p]
    if not parts:
        return ''
    return parts[0][0].lower() + parts[0][1:] + ''.join(p.capitalize() for p in parts[1:])

def get_reg_names(csv_path: Path) -> list[str]:
    reg_names = {}
    with csv_path.open("r", newline="") as f:
        reader = csv.reader(f)
        header_skipped = False
        for row in reader:
            if not header_skipped:
                header_skipped = True
                continue
            if not row:
                continue
            reg_names[to_camel_case(row[3].strip())] = row[3].strip()
    return reg_names


def load_modbus_register_map(csv_path: Path) -> tuple[int, int, Dict[int, Tuple[str, float, bool]]]:
    """Parse weather_registers.csv into a contiguous register span and metadata.

    Returns a tuple of (start_address, register_count, address_to_meta) where
    address_to_meta maps register address -> (tag_key, scale, is_signed).
    """

    address_to_meta: Dict[int, Tuple[str, float, bool]] = {}
    min_addr: int | None = None
    max_addr: int | None = None

    with csv_path.open("r", newline="") as f:
        reader = csv.reader(f)
        header_skipped = False
        for row in reader:
            if not header_skipped:
                header_skipped = True
                continue
            if not row:
                continue
            try:
                register_address_str = row[1].strip()
                value_name_str = row[3].strip()
                scale_str = row[4].strip()
                signed_flag_str = row[5].strip().lower()
            except IndexError:
                continue

            if not register_address_str or not value_name_str or not scale_str or not signed_flag_str:
                continue

            try:
                address = int(register_address_str)
            except ValueError:
                continue
            try:
                scale = float(scale_str)
            except ValueError:
                continue

            is_signed = signed_flag_str.startswith('s')
            tag_key = to_camel_case(value_name_str)
            if not tag_key:
                continue

            address_to_meta[address] = (tag_key, scale, is_signed)

            if min_addr is None or address < min_addr:
                min_addr = address
            if max_addr is None or address > max_addr:
                max_addr = address

    if min_addr is None or max_addr is None:
        return 0, 0, {}

    start_address = min_addr
    register_count = (max_addr - min_addr) + 1
    return start_address, register_count, address_to_meta


