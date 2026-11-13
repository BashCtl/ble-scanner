from ble.models import (
    DetailProps,
    Details,
    DiscoveredDevice,
    DiscoveredDeviceWithAdv,
)


def make_detail_props(**overrides) -> DetailProps:
    values = {
        "address": "AA:BB:CC:DD:EE:FF",
        "address_type": "public",
        "alias": "Sensor",
        "paired": False,
        "bonded": False,
        "trusted": False,
        "blocked": False,
        "legacy_pairing": False,
        "cable_pairing": False,
        "connected": True,
        "adapter": "hci0",
        "services_resolved": True,
        "advertising_flags": b"\x06",
    }
    values.update(overrides)
    return DetailProps(**values)


def test_detail_props_optional_fields_and_collections_default_independently() -> None:
    first = make_detail_props()
    second = make_detail_props()

    assert first.uuids == []
    assert first.manufacturer_data == {}
    assert first.rssi is None
    assert first.tx_power is None

    first.uuids.append("battery-service")
    first.manufacturer_data[76] = b"data"
    assert second.uuids == []
    assert second.manufacturer_data == {}


def test_detail_props_to_dict_contains_all_values() -> None:
    props = make_detail_props(
        uuids=["battery-service"],
        manufacturer_data={76: b"\x01\x02"},
        rssi=-55,
        tx_power=4,
    )

    assert props.to_dict() == {
        "Address": "AA:BB:CC:DD:EE:FF",
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
        "AdvertisingFlags": b"\x06",
        "UUIDs": ["battery-service"],
        "ManufacturerData": {76: b"\x01\x02"},
        "RSSI": -55,
        "TxPower": 4,
    }


def test_details_to_dict_includes_nested_props() -> None:
    props = make_detail_props(rssi=-70)
    details = Details(path="/org/bluez/hci0/dev_AA_BB", props=props)

    result = details.to_dict()

    assert result["path"] == "/org/bluez/hci0/dev_AA_BB"
    assert result["props"]["Address"] == "AA:BB:CC:DD:EE:FF"
    assert result["props"]["RSSI"] == -70


def test_discovered_device_to_dict_includes_optional_details() -> None:
    device = DiscoveredDevice(address="AA:BB", name=None)

    assert device.to_dict() == {"address": "AA:BB", "name": None, "details": None}

    device.details = Details(path="/device", props=make_detail_props())
    assert device.to_dict()["details"]["path"] == "/device"


def test_discovered_device_with_adv_defaults_and_to_dict() -> None:
    device = DiscoveredDeviceWithAdv(address="CC:DD", name="Beacon")

    assert device.rssi is None
    assert device.manufacturer_data == {}
    assert device.service_uuids == []
    assert device.service_data == {}
    assert device.to_dict() == {
        "address": "CC:DD",
        "name": "Beacon",
        "rssi": None,
        "manufacturer_data": {},
        "service_uuids": [],
        "service_data": {},
    }
