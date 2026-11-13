import json

import pytest

from ble.models import DiscoveredDevice, DiscoveredDeviceWithAdv
from ble.utils import encoder, write_to_json


def test_encoder_serializes_bytes_as_hex() -> None:
    assert encoder(b"\x00\xab\xff") == "00abff"


def test_encoder_rejects_unsupported_types() -> None:
    with pytest.raises(TypeError, match=r"Cannot serialize <class 'object'>"):
        encoder(object())


def test_write_to_json_serializes_discovered_devices(tmp_path) -> None:
    devices = [DiscoveredDevice(address="AA:BB", name="Sensor")]
    output = tmp_path / "devices"

    write_to_json(str(output), devices)

    assert json.loads((tmp_path / "devices.json").read_text(encoding="utf-8")) == [
        {"address": "AA:BB", "name": "Sensor", "details": None}
    ]


def test_write_to_json_serializes_advertisement_bytes(tmp_path) -> None:
    devices = [
        DiscoveredDeviceWithAdv(
            address="CC:DD",
            name="Beacon",
            rssi=-62,
            manufacturer_data={76: b"\x01\x02"},
            service_uuids=["0000180f-0000-1000-8000-00805f9b34fb"],
            service_data={"service": b"\xfe"},
        )
    ]
    output = tmp_path / "advertisements"

    write_to_json(str(output), devices)

    assert json.loads(
        (tmp_path / "advertisements.json").read_text(encoding="utf-8")
    ) == [
        {
            "address": "CC:DD",
            "name": "Beacon",
            "rssi": -62,
            "manufacturer_data": {"76": "0102"},
            "service_uuids": ["0000180f-0000-1000-8000-00805f9b34fb"],
            "service_data": {"service": "fe"},
        }
    ]
