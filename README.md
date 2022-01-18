## Python - NET2GRID Client

<!-- PROJECT SHIELDS -->
[![GitHub Release][releases-shield]][releases]
[![Python Versions][python-versions-shield]][pypi]
![Project Stage][project-stage-shield]
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE)

[![GitHub Activity][commits-shield]][commits-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GitHub Last Commit][last-commit-shield]][commits-url]

[![Code Quality][code-quality-shield]][code-quality]
[![Maintainability][maintainability-shield]][maintainability-url]
[![Code Coverage][codecov-shield]][codecov-url]
[![Build Status][build-shield]][build-url]

Asynchronous Python client for NET2GRID devices.

## About

A python package with which you can read the data from a [NET2GRID][net2grid] device via a local API. NET2GRID supplies energy hardware to brands, that can market it as a white label product.

## Supported SmartBridges

- SBWF3102 ([Pure Energie][pure-energie])

## Installation

```bash
pip install net2grid
```

## Usage

```py
import asyncio

from net2grid import Net2Grid

async def main():
    """Show example on getting data from your NET2GRID device."""
    async with Net2Grid(
        host="example.com",
    ) as client:
        device = await client.device()
        smartmeter = await client.smartmeter()
        print(device)
        print(smartmeter)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

## Data

You can read the following data with this package, the `power flow` entity can also give a negative value. The `energy` entities are total values of both low and high tariff together.

### Device

- ID
- Model
- Batch
- Firmware version
- Hardware version
- Manufacturer

### SmartMeter

- Power Flow (W)
- Energy Consumption (kWh)
- Energy Production (kWh)

## Setting up development environment

This Python project is fully managed using the [Poetry][poetry] dependency
manager.

You need at least:

- Python 3.8+
- [Poetry][poetry-install]

Install all packages, including all development requirements:

```bash
poetry install
```

Poetry creates by default an virtual environment where it installs all
necessary pip packages, to enter or exit the venv run the following commands:

```bash
poetry shell
exit
```

Setup the pre-commit check, you must run this inside the virtual environment:

```bash
pre-commit install
```

*Now you're all set to get started!*

As this repository uses the [pre-commit][pre-commit] framework, all changes
are linted and tested with each commit. You can run all checks and tests
manually, using the following command:

```bash
poetry run pre-commit run --all-files
```

To run just the Python tests:

```bash
poetry run pytest
```

## License

MIT License

Copyright (c) 2021 Klaas Schoute

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[pure-energie]: https://pure-energie.nl
[net2grid]: https://www.net2grid.com
[poetry-install]: https://python-poetry.org/docs/#installation
[poetry]: https://python-poetry.org
[pre-commit]: https://pre-commit.com

<!-- MARKDOWN LINKS & IMAGES -->
[build-shield]: https://github.com/klaasnicolaas/python-net2grid/actions/workflows/tests.yaml/badge.svg
[build-url]: https://github.com/klaasnicolaas/python-net2grid/actions/workflows/tests.yaml
[code-quality-shield]: https://img.shields.io/lgtm/grade/python/g/klaasnicolaas/python-net2grid.svg?logo=lgtm&logoWidth=18
[code-quality]: https://lgtm.com/projects/g/klaasnicolaas/python-net2grid/context:python
[commits-shield]: https://img.shields.io/github/commit-activity/y/klaasnicolaas/python-net2grid.svg
[commits-url]: https://github.com/klaasnicolaas/python-net2grid/commits/main
[codecov-shield]: https://codecov.io/gh/klaasnicolaas/python-net2grid/branch/main/graph/badge.svg?token=VQTR24YFQ9
[codecov-url]: https://codecov.io/gh/klaasnicolaas/python-net2grid
[forks-shield]: https://img.shields.io/github/forks/klaasnicolaas/python-net2grid.svg
[forks-url]: https://github.com/klaasnicolaas/python-net2grid/network/members
[issues-shield]: https://img.shields.io/github/issues/klaasnicolaas/python-net2grid.svg
[issues-url]: https://github.com/klaasnicolaas/python-net2grid/issues
[license-shield]: https://img.shields.io/github/license/klaasnicolaas/python-net2grid.svg
[last-commit-shield]: https://img.shields.io/github/last-commit/klaasnicolaas/python-net2grid.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2021.svg
[maintainability-shield]: https://api.codeclimate.com/v1/badges/0b3297077cbc525a837e/maintainability
[maintainability-url]: https://codeclimate.com/github/klaasnicolaas/python-net2grid/maintainability
[project-stage-shield]: https://img.shields.io/badge/project%20stage-experimental-yellow.svg
[pypi]: https://pypi.org/project/net2grid/
[python-versions-shield]: https://img.shields.io/pypi/pyversions/net2grid
[releases-shield]: https://img.shields.io/github/release/klaasnicolaas/python-net2grid.svg
[releases]: https://github.com/klaasnicolaas/python-net2grid/releases
[stars-shield]: https://img.shields.io/github/stars/klaasnicolaas/python-net2grid.svg
[stars-url]: https://github.com/klaasnicolaas/python-net2grid/stargazers
