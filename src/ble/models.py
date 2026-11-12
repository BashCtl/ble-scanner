from dataclasses import asdict, dataclass, field

from dataclasses_json import config, dataclass_json


@dataclass_json
@dataclass
class DetailProps:
    address: str = field(metadata=config(field_name="Address"))
    address_type: str = field(metadata=config(field_name="AddressType"))
    alias: str = field(metadata=config(field_name="Alias"))

    paired: bool = field(metadata=config(field_name="Paired"))
    bonded: bool = field(metadata=config(field_name="Bonded"))
    trusted: bool = field(metadata=config(field_name="Trusted"))
    blocked: bool = field(metadata=config(field_name="Blocked"))
    legacy_pairing: bool = field(metadata=config(field_name="LegacyPairing"))
    cable_pairing: bool = field(metadata=config(field_name="CablePairing"))
    connected: bool = field(metadata=config(field_name="Connected"))

    adapter: str = field(metadata=config(field_name="Adapter"))
    services_resolved: bool = field(metadata=config(field_name="ServicesResolved"))
    advertising_flags: bytes = field(metadata=config(field_name="AdvertisingFlags"))

    uuids: list[str] = field(default_factory=list, metadata=config(field_name="UUIDs"))
    manufacturer_data: dict[int, bytes] = field(
        default_factory=dict, metadata=config(field_name="ManufacturerData")
    )

    rssi: int | None = field(default=None, metadata=config(field_name="RSSI"))
    tx_power: int | None = field(default=None, metadata=config(field_name="TxPower"))

    def to_dict(self):
        return asdict(self)


@dataclass_json
@dataclass
class Details:
    path: str
    props: DetailProps


@dataclass
class BaseDevice:
    address: str
    name: str | None

    def to_dict(self):
        return asdict(self)


@dataclass
class DiscoveredDevice(BaseDevice):
    details: Details | None = None


@dataclass
class DiscoveredDeviceWithAdv(BaseDevice):
    rssi: int | None = None
    manufacturer_data: dict[int, bytes] = field(default_factory=dict)
    service_uuids: list[str] = field(default_factory=list)
    service_data: dict[str:bytes] = field(default_factory=dict)
