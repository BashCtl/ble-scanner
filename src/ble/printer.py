from rich.console import Console
from rich.table import Table
from rich.text import Text

from ble.models import Details, DiscoveredDevice, DiscoveredDeviceWithAdv


class Printer:
    def __init__(self):
        self.console = Console()

    def print_discovered_device(self, devices: list[DiscoveredDevice]):
        if not devices:
            self.console.print("No devices found")
            return

        table = Table(title="BLE Discovered Devices")

        table.add_column("Name", style="cyan")
        table.add_column("Address", style="magenta")
        table.add_column("Details", style="green")

        for device in devices:
            table.add_row(
                device.name or "Unnamed",
                device.address,
                self.__details_table(device.details),
            )

        self.console.print(table)

    def __details_table(self, details: Details):
        table = Table(header_style="cyan", box=None, padding=(0, 1))
        table.add_column("Property")
        table.add_column("Value")

        table.add_row("path", details.path)

        for name, value in details.props.to_dict().items():
            table.add_row(str(name), str(value))
        return table

    def print_descovered_device_with_adv(self, devices: list[DiscoveredDeviceWithAdv]):
        if not devices:
            self.console.print("No devices found")
            return

        table = Table(title="BLE Discovered Devices With Advertisement On")

        table.add_column("Name", style="cyan")
        table.add_column("Address", style="magenta")
        table.add_column("RSSI", style="green")
        table.add_column("Manufacturer Data", style="blue")
        table.add_column("Sercie UUIDS", style="green")
        table.add_column("Service Data", style="green")

        for device in devices:
            table.add_row(
                device.name or "Unnamed",
                device.address,
                str(device.rssi),
                str(device.manufacturer_data),
                "\n".join(device.service_uuids),
                self.__service_data_table(device.service_data),
            )

        self.console.print(table)

    def __service_data_table(self, service_data: dict):
        table = Table(header_style="cyan", box=None)
        table.add_column("UUID")
        table.add_column("Hex Value")
        for uuid, data in service_data.items():
            table.add_row(uuid, Text(data.hex(" ")))

        return table
