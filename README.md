## Python - Net2Grid Client

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
[![Typing Status][typing-shield]][typing-url]

Asynchronous Python client for Net2Grid devices.

## About

A python package with which you can read the data from a [NET2GRID][net2grid] device via a local api. Net2Grid supplies energy hardware to brands, that can market it as a white label product.

## Supported SmartBridges

- SBWF3102 ([Pure Energie][pure-energie])

## Installation

```bash
pip install gridnet
```

## Usage

```py
import asyncio

from gridnet import GridNet

async def main():
    """Show example on getting data from your device."""
    async with GridNet(
        host="example.com",
    ) as client:
        device = await client.device()
        smartbridge = await client.smartbridge()
        print(device)
        print(smartbridge)

if __name__ == "__main__":
    asyncio.run(main())
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

### SmartBridge

- Power Flow (W)
- Energy Consumption (kWh)
- Energy Production (kWh)

## Contributing

This is an active open-source project. We are always open to people who want to
use the code or contribute to it.

We've set up a separate document for our
[contribution guidelines](CONTRIBUTING.md).

Thank you for being involved! :heart_eyes:

## Setting up development environment

This Python project is fully managed using the [Poetry][poetry] dependency
manager.

You need at least:

- Python 3.9+
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

## Trademark Legal Notices

All product names, trademarks and registered trademarks in this repository, are property of their respective owners, and are used by the author for identification purposes only. The use of these names, trademarks and brands, do not imply endorsement or affiliation.

## License

MIT License

Copyright (c) 2021-2022 Klaas Schoute

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
[build-shield]: https://github.com/klaasnicolaas/python-gridnet/actions/workflows/tests.yaml/badge.svg
[build-url]: https://github.com/klaasnicolaas/python-gridnet/actions/workflows/tests.yaml
[code-quality-shield]: https://img.shields.io/lgtm/grade/python/g/klaasnicolaas/python-gridnet.svg?logo=lgtm&logoWidth=18
[code-quality]: https://lgtm.com/projects/g/klaasnicolaas/python-gridnet/context:python
[commits-shield]: https://img.shields.io/github/commit-activity/y/klaasnicolaas/python-gridnet.svg
[commits-url]: https://github.com/klaasnicolaas/python-gridnet/commits/main
[codecov-shield]: https://codecov.io/gh/klaasnicolaas/python-gridnet/branch/main/graph/badge.svg?token=CXCSJBsRPE
[codecov-url]: https://codecov.io/gh/klaasnicolaas/python-gridnet
[forks-shield]: https://img.shields.io/github/forks/klaasnicolaas/python-gridnet.svg
[forks-url]: https://github.com/klaasnicolaas/python-gridnet/network/members
[issues-shield]: https://img.shields.io/github/issues/klaasnicolaas/python-gridnet.svg
[issues-url]: https://github.com/klaasnicolaas/python-gridnet/issues
[license-shield]: https://img.shields.io/github/license/klaasnicolaas/python-gridnet.svg
[last-commit-shield]: https://img.shields.io/github/last-commit/klaasnicolaas/python-gridnet.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2022.svg
[maintainability-shield]: https://api.codeclimate.com/v1/badges/0b3297077cbc525a837e/maintainability
[maintainability-url]: https://codeclimate.com/github/klaasnicolaas/python-gridnet/maintainability
[project-stage-shield]: https://img.shields.io/badge/project%20stage-experimental-yellow.svg
[pypi]: https://pypi.org/project/gridnet/
[python-versions-shield]: https://img.shields.io/pypi/pyversions/gridnet
[typing-shield]: https://github.com/klaasnicolaas/python-gridnet/actions/workflows/typing.yaml/badge.svg
[typing-url]: https://github.com/klaasnicolaas/python-gridnet/actions/workflows/typing.yaml
[releases-shield]: https://img.shields.io/github/release/klaasnicolaas/python-gridnet.svg
[releases]: https://github.com/klaasnicolaas/python-gridnet/releases
[stars-shield]: https://img.shields.io/github/stars/klaasnicolaas/python-gridnet.svg
[stars-url]: https://github.com/klaasnicolaas/python-gridnet/stargazers
