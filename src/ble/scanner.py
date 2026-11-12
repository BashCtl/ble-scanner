import argparse
import asyncio

from bleak import BleakScanner

from ble.models import Details, DiscoveredDevice, DiscoveredDeviceWithAdv
from ble.printer import Printer
from ble.utils import write_to_json


async def scan(
    timeout: int = 5, is_adv: bool = False
) -> list[DiscoveredDevice] | list[DiscoveredDeviceWithAdv]:
    result = await BleakScanner.discover(timeout=timeout, return_adv=is_adv)
    devices = []
    if is_adv:
        for address, (device, advertisment) in result.items():
            devices.append(
                DiscoveredDeviceWithAdv(
                    address=address,
                    name=advertisment.local_name or device.name,
                    rssi=advertisment.rssi,
                    manufacturer_data=advertisment.manufacturer_data,
                    service_uuids=advertisment.service_uuids,
                    service_data=advertisment.service_data,
                )
            )
    else:
        for device in result:
            devices.append(
                DiscoveredDevice(
                    address=device.address,
                    name=device.name,
                    details=Details.from_dict(device.details),
                )
            )
    return devices


def main():
    printer = Printer()

    parser = argparse.ArgumentParser(description="BLE devices scanner")
    parser.add_argument(
        "-a", "--adv", action="store_true", help="Advertisement data on."
    )
    parser.add_argument(
        "-w", "--write", type=str, help="Name of json file to store device in."
    )

    args = parser.parse_args()
    try:
        devices = asyncio.run(scan(is_adv=args.adv))
        if args.adv:
            printer.print_descovered_device_with_adv(devices)
        else:
            printer.print_discovered_device(devices)

        if args.write is not None:
            write_to_json(args.write, devices)

    except ValueError as e:
        parser.error(str(e))


if __name__ == "__main__":
    main()
