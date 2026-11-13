# BLE Scanner

A command-line Bluetooth Low Energy (BLE) scanner built with [Bleak](https://bleak.readthedocs.io/) and [Rich](https://rich.readthedocs.io/). It discovers nearby devices, displays their details in a terminal table, and can save results as JSON.

## Requirements

- Python 3.13 or newer
- A Bluetooth adapter enabled on the computer
- Bluetooth permissions required by your operating system
- [uv](https://docs.astral.sh/uv/) for dependency and project management

## Install

Clone the repository and install its dependencies with uv:

```sh
git clone <repository-url>
cd ble-scanner
uv sync
```

`uv sync` creates the project environment and installs the dependencies from `uv.lock`.

## Use

Scan for nearby devices:

```sh
uv run ble-scanner
```

Show advertisement data such as RSSI, manufacturer data, service UUIDs, and service data:

```sh
uv run ble-scanner --adv
```

Save the scan results to JSON. The program appends `.json` to the provided name:

```sh
uv run ble-scanner --write scan-results
uv run ble-scanner --adv --write advertisements
```

See all command-line options:

```sh
uv run ble-scanner --help
```

The scan duration currently uses the scanner's default of five seconds.

## Project structure

```text
src/ble/
├── models.py       # Device and detail data models
├── printer.py      # Rich terminal output
├── scanner.py      # BLE discovery and command-line interface
├── utils.py        # JSON serialization helpers
└── tests/          # Unit tests
```

## Run tests

Install the development dependency group and run the test suite:

```sh
uv sync --group dev
uv run pytest
```
