<picture>
         <source media="(prefers-color-scheme: dark)" srcset="./dark.png">
        <img alt="Texas Tech Computer Science - Whitacre College of Engineering" src="https://raw.githubusercontent.com/jaxcksn/jaxcksn/main/files/Lockup_Github.svg" width="200" align="right">
</picture>

# FSMD

<div align="center">

### <u>F</u>inite <u>S</u>tate <u>M</u>achine <u>D</u>iagram Tool

![Python Version >= 3.7](https://flat.badgen.net/pypi/python/FSMD)

</div>

> A python command line tool for creating finite state machine diagrams from a file. Make deterministic and non-deterministic automata easily!

<div align="center">

![Version 1.0.0](https://flat.badgen.net/badge/pypi/1.0.0/cyan?icon=pypi) ![MIT License](https://flat.badgen.net/badge/license/GPLv3/blue) ![Python >3.7](https://flat.badgen.net/pypi/dd/FSMD/?label=downloads&color=purple) ![Last Commit](https://flat.badgen.net/github/last-commit/jaxcksn/FSMD)

![Made by Jaxcksn](https://flat.badgen.net/badge/Made%20with%20%E2%99%A5%20by/Jaxcksn/red)

</div>

<div align="center">

[Features](#features) **·** [Installation](#installation) **·** [Usage](#using-fsmd) **·** [Support](#support)

</div>

## Features

### Current

- Allows easy creation of an FSM diagram anywhere from a YAML file
- Quickly create non-deterministic automata with epsilon transition support.
- Included installer for Graphviz for Windows and MacOS.
- Easy to install and use
- Diagrams are automatically optimized to be the ideal size.

### Planned

- [ ] Allow changing output format
- [ ] Improve input file capabilities
- [ ] Add CLI options for sizing output
- [ ] Add more rigorous input file checking
- [ ] Linux support for installer
- [ ] Improve reliability of installer

## Installation

### Pre-requisites

To use FSMD, **Python 3.7 or greater** is required to be installed. You must also have pip as well.

### Install FSMD

To install FSMD you can run:

```
pip install FSDM
```

If you want to run the project directly, you can run the main.py file in the source folder, and Typer should take care of the rest.

### Install Graphviz

The Graphviz library is required for FSDM to work properly, there are a few two ways (unless you are on Linux) to do this.

### Automatic Install (Windows & MacOS Only)

FSDM includes an automatic installer for Graphviz. Each platform has different steps.

The automatic installer is experimental and **not guaranteed** to work, it's recommended to [install Graphviz yourself](#manual-install-all-platforms) if the automatic installer does not work for you.

---

<details>
    <summary>Windows</summary>

#### Usage

To install on Windows, run the following command:

    FSDM install

_Note:_ The windows installer does not add the Graphviz executables to your system path. It instead installs to a location in `%LOCALAPPDATA`, which is added to the PATH only when running FSDM. If you don't know what this means, don't worry about it.

</details>

---

<details>
    <summary>MacOS</summary>

#### Requirements

Automatic installation on MacOS **requires Homebrew** to be installed. You can install it by following the steps on [this page](https://brew.sh/).

#### Usage

Once you meet all the requirements, run the following command:

    FSDM install

</details>

---

### Manual Install (All Platforms)

Visit the [Graphviz Download Page](https://graphviz.org/download/) and follow the steps to install Graphviz for your platform.

Once downloaded and installed, make sure Graphviz is in your path by running:

    dot --version

If the command runs with no issues, then you are ready to start using FSMD.

## Using FSMD

Once you have the tool installed, you will need to create a file for FSMD to create a diagram of. Please see the [FSM File Documentation](./docs/fsmfile.md) for details.

To create the diagram, run the following command:

    FSMD create FORMAT INPUT_FILE OUTPUT_FOLDER

Where FORMAT is `png` or `svg`
To view all the options and arguments for the create command you can run:

    FSMD create --help

## Support

I am an active college student, so I stay pretty busy, but feel free to open an issue if you run into any problems, and I will look into it as soon as I can.
