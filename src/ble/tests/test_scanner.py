import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

from ble import scanner
from ble.models import DiscoveredDevice, DiscoveredDeviceWithAdv


def test_scan_converts_regular_devices(monkeypatch) -> None:
    bleak_device = SimpleNamespace(
        address="AA:BB",
        name="Sensor",
        details={
            "path": "/org/bluez/hci0/dev_AA_BB",
            "props": {
                "Address": "AA:BB",
                "AddressType": "public",
                "Alias": "Sensor",
                "Paired": False,
                "Bonded": False,
                "Trusted": False,
                "Blocked": False,
                "LegacyPairing": False,
                "CablePairing": False,
                "Connected": True,
                "Adapter": "hci0",
                "ServicesResolved": True,
                "AdvertisingFlags": [6],
                "UUIDs": [],
                "ManufacturerData": {},
                "RSSI": -50,
                "TxPower": 2,
            },
        },
    )
    discover = AsyncMock(return_value=[bleak_device])
    monkeypatch.setattr(scanner.BleakScanner, "discover", discover)

    devices = asyncio.run(scanner.scan(timeout=8))

    discover.assert_awaited_once_with(timeout=8, return_adv=False)
    assert devices == [
        DiscoveredDevice(
            address="AA:BB",
            name="Sensor",
            details=scanner.Details.from_dict(bleak_device.details),
        )
    ]
    assert devices[0].details.props.rssi == -50


def test_scan_converts_advertisement_data_and_prefers_local_name(monkeypatch) -> None:
    device = SimpleNamespace(address="CC:DD", name="Device name")
    advertisement = SimpleNamespace(
        local_name="Advertised name",
        rssi=-63,
        manufacturer_data={76: b"\x01\x02"},
        service_uuids=["battery-service"],
        service_data={"battery-service": b"\x04"},
    )
    discover = AsyncMock(return_value={"CC:DD": (device, advertisement)})
    monkeypatch.setattr(scanner.BleakScanner, "discover", discover)

    devices = asyncio.run(scanner.scan(timeout=3, is_adv=True))

    discover.assert_awaited_once_with(timeout=3, return_adv=True)
    assert devices == [
        DiscoveredDeviceWithAdv(
            address="CC:DD",
            name="Advertised name",
            rssi=-63,
            manufacturer_data={76: b"\x01\x02"},
            service_uuids=["battery-service"],
            service_data={"battery-service": b"\x04"},
        )
    ]


def test_scan_falls_back_to_device_name_when_local_name_missing(monkeypatch) -> None:
    device = SimpleNamespace(address="CC:DD", name="Device name")
    advertisement = SimpleNamespace(
        local_name=None,
        rssi=-63,
        manufacturer_data={},
        service_uuids=[],
        service_data={},
    )
    monkeypatch.setattr(
        scanner.BleakScanner,
        "discover",
        AsyncMock(return_value={"CC:DD": (device, advertisement)}),
    )

    devices = asyncio.run(scanner.scan(is_adv=True))

    assert devices[0].name == "Device name"


def test_main_prints_regular_scan_and_writes_when_requested(monkeypatch) -> None:
    device = DiscoveredDevice(address="AA:BB", name="Sensor")
    printed = []
    written = []
    monkeypatch.setattr(
        scanner.argparse.ArgumentParser,
        "parse_args",
        lambda self: SimpleNamespace(adv=False, write="out"),
    )

    def run_scan(coroutine):
        coroutine.close()
        return [device]

    monkeypatch.setattr(scanner.asyncio, "run", run_scan)
    monkeypatch.setattr(scanner.Printer, "print_discovered_device", lambda self, devices: printed.extend(devices))
    monkeypatch.setattr(scanner, "write_to_json", lambda filename, devices: written.append((filename, devices)))

    scanner.main()

    assert printed == [device]
    assert written == [("out", [device])]


def test_main_converts_scan_value_error_to_argument_error(monkeypatch) -> None:
    errors = []
    monkeypatch.setattr(
        scanner.argparse.ArgumentParser,
        "parse_args",
        lambda self: SimpleNamespace(adv=False, write=None),
    )

    def fail_scan(coroutine):
        coroutine.close()
        raise ValueError("scan failed")

    monkeypatch.setattr(scanner.asyncio, "run", fail_scan)
    monkeypatch.setattr(
        scanner.argparse.ArgumentParser,
        "error",
        lambda self, message: errors.append(message),
    )

    scanner.main()

    assert errors == ["scan failed"]
