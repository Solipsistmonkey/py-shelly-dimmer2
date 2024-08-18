# Shelly Device Control

This repository contains Python modules and scripts for controlling and monitoring Shelly devices, particularly focusing on the Shelly Dimmer2. It includes models for various device statuses and a threaded control loop for periodic status updates.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Models Overview](#models-overview)
  - [Running the Dimmer2 Controller](#running-the-dimmer2-controller)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project is designed to interact with Shelly devices, enabling you to control and monitor various aspects of the device's functionality, such as lighting, power usage, temperature, and more. The repository provides Pydantic models for data validation and serialization, making it easy to parse and work with the JSON data returned by the device.

## Features

- **Device Status Models:** Pydantic models for various statuses including light, meter, WiFi, temperature, and more.
- **Threaded Control Loop:** Background thread for continuously updating the device status.
- **Comprehensive Logging:** Utilizes Loguru for detailed logging of device interactions and status updates.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/shelly-device-control.git
   cd shelly-device-control
    ```
2. **Set up a virtual environment (optional but recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```
## Usage

### Models Overview

The `models` package contains various Pydantic models that represent the status of different aspects of a Shelly device:

- `LightStatus`: Represents the status of the light, including whether it's on, brightness, mode, etc.
- `MeterStatus`: Represents the power metering status, including current power usage, total usage, and more.
- `TempStatus`: Represents the temperature status, providing readings in Celsius and Fahrenheit.
- `WifiStatus`, `CloudStatus`, etc., each representing their respective statuses.

### Running the Dimmer2 Controller

The `Dimmer2` class in `models/dimmer.py` is designed to manage a Shelly Dimmer2 device, including controlling the light, updating its status, and interacting with it over HTTP.

To control a Dimmer2 device, you can use the following example:

```python
from shelly import Dimmer2

dimmer = Dimmer2(device_ip="192.168.1.99")
dimmer.toggle()  # Toggles the light on or off
```
This will also start a background thread that continuously updates the device status.


### Configuration

- `Logging`: Logs are saved to the logs directory. The logging setup can be customized in the Dimmer2 class.

### License

This project is licensed under the MIT License. See the LICENSE file for more details.