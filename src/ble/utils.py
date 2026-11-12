import json

from ble.models import DiscoveredDevice, DiscoveredDeviceWithAdv


def encoder(obj):
    if isinstance(obj, bytes):
        return obj.hex()
    raise TypeError(f"Cannot serialize {type(obj)}")


def write_to_json(
    filename: str,
    devices: list[DiscoveredDeviceWithAdv] | list[DiscoveredDevice],
) -> None:
    with open(f"{filename}.json", "w", encoding="utf-8") as file:
        json.dump(
            [device.to_dict() for device in devices],
            file,
            indent=2,
            default=encoder,
        )
