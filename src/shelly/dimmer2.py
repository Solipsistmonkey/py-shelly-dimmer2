from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional

import httpx

from loguru import logger
from orjson import OPT_INDENT_2, loads as orloads, dumps as ordumps
from pathlib import Path

import paho.mqtt.client as mqtt
from paho.mqtt.client import Client
from paho.mqtt.enums import CallbackAPIVersion  # type: ignore

from models.light import LightStatus
from models.status import Status

log_dir = Path(__file__).parents[2] / "logs"
# logger.add()
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
    return time.time() * 1000


class LightControl:
    brightness_increment = 10

    def __init__(self, dimmer: Dimmer2) -> None:
        self.ip: str = dimmer.ip
        self.url: str = f"http://{self.ip}/light/0"
        self.dimmer: Dimmer2 = dimmer

    def __bool__(self):
        return self.dimmer.light_status.is_on

    @property
    def brightness(self) -> int:

        return self.dimmer.light_status.brightness

    @brightness.setter
    def brightness(self, value: int) -> None:
        brightness = max(0, min(100, value))
        self.change_state(brightness=brightness)

    def brightness_up(self) -> None:
        brightness = self.brightness + self.brightness_increment
        brightness = max(0, min(100, brightness))
        self.change_state(brightness=brightness)

    def brightness_down(self) -> None:
        brightness = self.brightness - self.brightness_increment
        brightness = max(0, min(100, brightness))
        self.change_state(brightness=brightness)

    def toggle(
        self, brightness: Optional[int] = None, transition: Optional[int] = None
    ) -> None:
        turn = "toggle"
        self.change_state(turn=turn, brightness=brightness, transition=transition)

    def on(
        self, brightness: Optional[int] = None, transition: Optional[int] = None
    ) -> None:
        turn = "on"
        self.change_state(turn=turn, brightness=brightness, transition=transition)

    def off(
        self, brightness: Optional[int] = None, transition: Optional[int] = None
    ) -> None:
        turn = "off"
        self.change_state(turn=turn, brightness=brightness, transition=transition)

    def change_state(
        self,
        turn: Optional[str] = None,
        brightness: Optional[int] = None,
        transition: Optional[int] = None,
    ) -> None:
        payload = {"turn": turn, "transition": transition, "brightness": brightness}
        logger.log("STATUS", f"Changing state: {payload}")

        payload = {k: v for k, v in payload.items() if v is not None}
        httpx.put(
            url=self.url,
            params=payload,
        )


class Dimmer2:
    _status: Optional[Status] = None
    http_refresh: int = 1000  # in milliseconds

    def __init__(self, device_ip: str = "192.168.1.99") -> None:
        self.ip = device_ip
        self.url = f"http://{device_ip}/"
        self.get_status()
        self._light_control = LightControl(self)
        self.mqtt = Client(CallbackAPIVersion.VERSION1)
        self._stop_event = threading.Event()
        self._status_thread = threading.Thread(target=self._status_loop, daemon=True)
        self._status_thread.start()

    @property
    def device_id(self) -> str:
        if self._status is None:
            return "Dimmer2(ID not fetched yet)"  # Placeholder
        return self.status.mac

    @property
    def status(self) -> Status:
        self.get_status()
        return self._status


    def get_status(self) -> None:


        logger.debug(f"Refreshing status for {self.device_id}")
        response = httpx.get(f"{self.url}status")
        logger.debug(f"Response: {response.json()}")
        self._status = Status(**response.json())
        logger.log("POWER", f"Watts: {self._status.meters[0].power}")
        self.last_refresh = time_ms()

    def get(self, endpoint: str) -> str:
        response = httpx.get(self.url + endpoint)
        return response.text

    @property
    def light_status(self) -> LightStatus:
        return self.status.lights[0]

    def _status_loop(self):
        while not self._stop_event.is_set():
            self.get_status()
            time.sleep(self.http_refresh / 1000.0)

    def stop_status_loop(self):
        self._stop_event.set()
        self._status_thread.join()

    def __getattr__(self, item):
        if item in [
            "toggle",
            "brightness_up",
            "brightness_down",
            "on",
            "off",
            "brightness",
        ]:
            return getattr(self._light_control, item)
        else:
            return self.__dict__[item](
                self,
            )



if __name__ == "__main__":
    dimmer = Dimmer2()
    dimmer.toggle()
