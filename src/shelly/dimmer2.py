"""
Dimmer2 Control Module.

This module provides classes and methods to control a Dimmer2 device,
including managing the light state, fetching status, and controlling
brightness levels. The module also handles logging and threading to
periodically update the device status.
"""

from __future__ import annotations
from pathlib import Path
import threading
import time
from typing import Optional

import httpx
from loguru import logger
from paho.mqtt.client import Client
from paho.mqtt.enums import CallbackAPIVersion  # type: ignore

from models import LightStatus, Status

log_dir = Path(__file__).parents[2] / "logs"
logger.level("STATUS", no=15, color="<blue>")
logger.add(
    log_dir / "dimmer2.log",
    rotation="10MB",
    level="DEBUG",
)
logger.level("POWER", no=25, color="<yellow>")
logger.add(
    sink=log_dir / "dimmer_power.log",
    rotation="20MB",
    retention=20,
    level="POWER",
)


def time_ms() -> float:
    """
    Returns the current time in milliseconds.

    Returns
    -------
    float
        The current time in milliseconds since the epoch.
    """
    return time.time() * 1000


class LightControl:
    """
    Controls the light settings of a Dimmer2 device.

    Attributes
    ----------
    brightness_increment : int
        The amount by which to increment or decrement the brightness.
    dimmer : Dimmer2
        The Dimmer2 device associated with this light control.
    ip : str
        The IP address of the Dimmer2 device.
    url : str
        The URL for sending commands to the light control of the Dimmer2
        device.
    """

    brightness_increment = 10

    def __init__(self, dimmer: Dimmer2) -> None:
        """
        Initializes the LightControl instance.

        Parameters
        ----------
        dimmer : Dimmer2
            The Dimmer2 device to control.
        """
        self.ip: str = dimmer.ip
        self.url: str = f"http://{self.ip}/light/0"
        self.dimmer: Dimmer2 = dimmer

    def __bool__(self) -> bool:
        """
        Returns the current state of the light (on or off).

        Returns
        -------
        bool
            True if the light is on, False otherwise.
        """
        if self.dimmer.light_status is None:
            return False
        return self.dimmer.light_status.is_on

    @property
    def brightness(self) -> int:
        """
        Gets the current brightness level.

        Returns
        -------
        int
            The current brightness level (0-100).
        """
        if self.dimmer.light_status is None:
            return 0
        return self.dimmer.light_status.brightness

    def set_brightness(self, value: int) -> None:
        """
        Sets the brightness to the specified value.

        Parameters
        ----------
        value : int
            The brightness level to set (0-100).
        """
        brightness = max(0, min(100, value))
        self.change_state(brightness=brightness)

    def brightness_up(self) -> None:
        """
        Increases the brightness by the predefined increment.
        """
        brightness = self.brightness + self.brightness_increment
        brightness = max(0, min(100, brightness))
        self.change_state(brightness=brightness)

    def brightness_down(self) -> None:
        """
        Decreases the brightness by the predefined increment.
        """
        brightness = self.brightness - self.brightness_increment
        brightness = max(0, min(100, brightness))
        self.change_state(brightness=brightness)

    def toggle(
        self, brightness: Optional[int] = None, transition: Optional[int] = None
    ) -> None:
        """
        Toggles the light on or off.

        Parameters
        ----------
        brightness : Optional[int], optional
            The brightness level to set, by default None.
        transition : Optional[int], optional
            The transition time, by default None.
        """
        turn = "toggle"
        self.change_state(turn=turn, brightness=brightness, transition=transition)

    def on(
        self, brightness: Optional[int] = None, transition: Optional[int] = None
    ) -> None:
        """
        Turns the light on.

        Parameters
        ----------
        brightness : Optional[int], optional
            The brightness level to set, by default None.
        transition : Optional[int], optional
            The transition time, by default None.
        """
        turn = "on"
        self.change_state(turn=turn, brightness=brightness, transition=transition)

    def off(
        self, brightness: Optional[int] = None, transition: Optional[int] = None
    ) -> None:
        """
        Turns the light off.

        Parameters
        ----------
        brightness : Optional[int], optional
            The brightness level to set, by default None.
        transition : Optional[int], optional
            The transition time, by default None.
        """
        turn = "off"
        self.change_state(turn=turn, brightness=brightness, transition=transition)

    def change_state(
        self,
        turn: Optional[str] = None,
        brightness: Optional[int] = None,
        transition: Optional[int] = None,
    ) -> None:
        """
        Changes the state of the light.

        Parameters
        ----------
        turn : Optional[str], optional
            The action to perform ("on", "off", "toggle"), by default None.
        brightness : Optional[int], optional
            The brightness level to set, by default None.
        transition : Optional[int], optional
            The transition time, by default None.
        """
        payload = {"turn": turn, "transition": transition, "brightness": brightness}
        logger.log("STATUS", f"Changing state: {payload}")

        payload = {k: v for k, v in payload.items() if v is not None}
        httpx.put(
            url=self.url,
            params=payload,
        )


class Dimmer2:
    """
    Represents a Dimmer2 device, providing methods to control and monitor it.

    Attributes
    ----------
    ip : str
        The IP address of the Dimmer2 device.
    url : str
        The base URL for accessing the Dimmer2 device.
    mqtt : Client
        The MQTT client for communication.
    http_refresh : int
        The interval in milliseconds for refreshing the device status.
    _status : Optional[Status]
        The current status of the device.

    Methods
    -------
    get_status()
        Fetches and updates the status of the device from the network.
    get(endpoint: str) -> str
        Fetches data from a specific endpoint of the device.
    stop_status_loop()
        Stops the background status update loop.


    """

    _status: Optional[Status] = None
    http_refresh: int = 1000  # in milliseconds

    def __init__(self, device_ip: str = "192.168.1.99") -> None:
        """
        Initializes the Dimmer2 instance.

        Parameters
        ----------
        device_ip : str, optional
            The IP address of the device, by default "192.168.1.99".
        """
        self.ip = device_ip
        self.url = f"http://{device_ip}/"
        self._light_control = LightControl(self)
        self.mqtt = Client(CallbackAPIVersion.VERSION1)
        self._stop_event = threading.Event()
        self._status_thread = threading.Thread(target=self._status_loop, daemon=True)
        self._status_thread.start()

    @property
    def device_id(self) -> str:
        """
        Returns the MAC address of the device as its ID.

        Returns
        -------
        str
            The MAC address of the device. If the status has not been
            fetched yet, returns a placeholder string.
        """
        if self._status is None:
            return "Dimmer2(ID not fetched yet)"  # Placeholder
        return self._status.mac

    @property
    def status(self) -> Optional[Status]:
        """
        Gets the current status of the device.

        Returns
        -------
        Optional[Status]
            The current status of the device.
        """
        self.get_status()
        return self._status

    def get_status(self) -> None:
        """
        Fetches and updates the status of the device from the network.
        """
        logger.debug(f"Refreshing status for {self.device_id}")
        try:
            response = httpx.get(f"{self.url}status")
            logger.debug(f"Response: {response.json()}")
            self._status = Status(**response.json())
            logger.log("POWER", f"Watts: {self._status.meters[0].power}")
        except httpx.HTTPError as e:
            logger.error(f"Failed to get status: {e}")

    def get(self, endpoint: str) -> str:
        """
        Fetches data from a specific endpoint of the device.

        Parameters
        ----------
        endpoint : str
            The endpoint to query.

        Returns
        -------
        str
            The response from the device as a string.
        """
        response = httpx.get(self.url + endpoint)
        return response.text

    @property
    def light_status(self) -> Optional[LightStatus]:
        """
        Gets the status of the light.

        Returns
        -------
        Optional[LightStatus]
            The status of the light if available, otherwise None.
        """
        if self._status is not None:
            return self._status.lights[0]
        return None

    def _status_loop(self) -> None:
        """
        Runs a loop in a separate thread to periodically update the device
        status.
        """
        while not self._stop_event.is_set():
            self.get_status()
            time.sleep(self.http_refresh / 1000.0)

    def stop_status_loop(self) -> None:
        """
        Stops the background status update loop.
        """
        self._stop_event.set()
        self._status_thread.join()

    @property
    def brightness(self) -> int:
        """
        Gets the current brightness level.

        Returns
        -------
        int
            The current brightness level (0-100).
        """
        return self._light_control.brightness

    def __getattr__(self, item):
        """
        Dynamically accesses methods of the LightControl class.

        Parameters
        ----------
        item : str
            The name of the method or attribute to access.

        Returns
        -------
        Any
            The method or attribute of the LightControl class, or raises an
            AttributeError if not found.
        """
        if item in [
            "toggle",
            "brightness_up",
            "brightness_down",
            "set_brightness",
            "on",
            "off",
        ]:
            return getattr(self._light_control, item)

        return self.__dict__[item](self)


if __name__ == "__main__":
    dimmer_control = Dimmer2()
    dimmer_control.toggle()
