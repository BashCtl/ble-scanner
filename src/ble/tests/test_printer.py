from io import StringIO

from rich.console import Console

from ble.models import (
    DetailProps,
    Details,
    DiscoveredDevice,
    DiscoveredDeviceWithAdv,
)
from ble.printer import Printer


def make_printer() -> tuple[Printer, StringIO]:
    printer = Printer()
    output = StringIO()
    printer.console = Console(
        file=output, force_terminal=False, color_system=None, width=160
    )
    return printer, output


def make_details() -> Details:
    return Details(
        path="/org/bluez/hci0/dev_AA_BB",
        props=DetailProps(
            address="AA:BB",
            address_type="public",
            alias="Thermometer",
            paired=False,
            bonded=False,
            trusted=False,
            blocked=False,
            legacy_pairing=False,
            cable_pairing=False,
            connected=True,
            adapter="hci0",
            services_resolved=True,
            advertising_flags=b"\x06",
            rssi=-48,
            tx_power=3,
        ),
    )


def test_print_discovered_device_reports_empty_list() -> None:
    printer, output = make_printer()

    printer.print_discovered_device([])

    assert output.getvalue().strip() == "No devices found"


def test_print_discovered_device_shows_name_address_and_details() -> None:
    printer, output = make_printer()
    devices = [
        DiscoveredDevice(
            address="AA:BB",
            name="Thermometer",
            details=make_details(),
        )
    ]

    printer.print_discovered_device(devices)

    rendered = output.getvalue()
    assert "BLE Discovered Devices" in rendered
    assert "Thermometer" in rendered
    assert "AA:BB" in rendered
    assert "/org/bluez/hci0/dev_AA_BB" in rendered
    assert "AdvertisingFlags" in rendered


def test_print_discovered_device_handles_missing_name_and_details() -> None:
    printer, output = make_printer()

    printer.print_discovered_device([DiscoveredDevice(address="CC:DD", name=None)])

    rendered = output.getvalue()
    assert "Unnamed" in rendered
    assert "CC:DD" in rendered
    assert "No details available" in rendered


def test_print_advertisement_device_reports_empty_list() -> None:
    printer, output = make_printer()

    printer.print_descovered_device_with_adv([])

    assert output.getvalue().strip() == "No devices found"


def test_print_advertisement_device_shows_advertisement_data() -> None:
    printer, output = make_printer()
    devices = [
        DiscoveredDeviceWithAdv(
            address="11:22",
            name="Beacon",
            rssi=-67,
            manufacturer_data={76: b"\x01\x02"},
            service_uuids=["battery-service", "device-info"],
            service_data={"battery-service": b"\x0a\xff"},
        )
    ]

    printer.print_descovered_device_with_adv(devices)

    rendered = output.getvalue()
    assert "BLE Discovered Devices With Advertisement On" in rendered
    assert "Beacon" in rendered
    assert "11:22" in rendered
    assert "-67" in rendered
    assert "{76: b'\\x01\\x02'}" in rendered
    assert "battery-service" in rendered
    assert "device-info" in rendered
    assert "0a ff" in rendered
