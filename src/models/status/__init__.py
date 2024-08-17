from typing import List
from pydantic import BaseModel, Field

from models import status
from models.light import LightStatus
from models.status.inputs import InputStatus
from models.status.meter import MeterStatus
from models.status.mqtt import MQTTStatus
from models.status.temperature import TempStatus
from models.status.update import UpdateStatus
from models.status.wifi_status import WifiStatus
from models.status.cloud import CloudStatus


class Status(BaseModel):
    wifi_status: WifiStatus = Field(
        ...,
        description="The current WiFi connection status",
        alias="wifi_sta",
        repr=False,
    )
    cloud: CloudStatus = Field(
        ...,
        description="The current cloud connection status",
        repr=False,
    )
    mqtt: MQTTStatus = Field(
        ...,
        description="The current MQTT connection status",
        repr=False,
    )
    time: str = Field(
        ...,
        description="The current time",
        repr=False,
    )
    unix_time: int = Field(
        ...,
        description="The current time in unixtime",
        alias="unixtime",
        repr=False,
    )
    serial: int = Field(
        ...,
        description="The cloud serial number of the device",
        repr=False,
    )
    has_update: bool = Field(
        ...,
        description="Whether the device has an update available",
        repr=False,
    )
    mac: str = Field(
        ...,
        description="The MAC address of the device",
        repr=False,
    )
    config_change_count: int = Field(
        ...,
        description="The number of configuration changes",
        alias="cfg_changed_cnt",
        repr=False,
    )
    actions_stats: dict = Field(
        ...,
        description="The statistics of actions",
        repr=False,
    )
    lights: List[LightStatus] = Field(
        ...,
        description="The status of the lights",
        repr=True,
    )
    meters: List[MeterStatus] = Field(
        ...,
        description="The status of the meters",
        repr=False,
    )
    inputs: List[InputStatus] = Field(
        ...,
        description="The status of the inputs",
        repr=False,
    )
    temperature: TempStatus = Field(
        ...,
        description="The temperature status",
        alias="tmp"
    )
    calibrated: bool = Field(
        ...,
        description="Whether the calibration is done",
        repr=False,
    )
    calibration_progress: int = Field(
        ...,
        description="The calibration progress in percent",
        alias="calib_progress",
        repr=False,
    )
    calibration_running: bool = Field(
        ...,
        description="Whether the calibration is running",
        alias="calib_running",
        repr=False,
    )
    wire_mode: int = Field(
        ...,
        description="0:LO mode, 1: LN mode",
        repr=False,
    )
    forced_neutral: bool = Field(
        ...,
        description="Forced neutral flag",
        repr=False,
    )
    over_temperature: bool = Field(
        ...,
        description="Whether an overtemperature condition has occurred",
        alias="overtemperature"
    )
    load_error: int = Field(
        ...,
        description="The load error",
        alias="loaderror"
    )
    over_power: bool = Field(
        ...,
        description="Whether an over power condition has occurred",
        alias="overpower"
    )
    debug: int = Field(
        ...,
        description="Whether debug mode is enabled",
        repr=False,
    )
    update: UpdateStatus = Field(
        ...,
        description="The update status",
        repr=False,
    )
    ram_total: int = Field(
        ...,
        description="The total RAM",
        repr=False,
    )
    ram_free: int = Field(
        ...,
        description="The free RAM",
        repr=False,
    )
    fs_size: int = Field(
        ...,
        description="The filesystem size",
        repr=False,
    )
    fs_free: int = Field(
        ...,
        description="The free filesystem space",
        repr=False,
    )
    uptime: int = Field(
        ...,
        description="The uptime in seconds",
        repr=False,
    )

if __name__ == '__main__':

    status_json = {
      "wifi_sta": {
        "connected": True,
        "ssid": "13 Claps",
        "ip": "192.168.1.99",
        "rssi": -51
      },
      "cloud": {
        "enabled": False,
        "connected": False
      },
      "mqtt": {
        "connected": True
      },
      "time": "14:16",
      "unixtime": 1723929401,
      "serial": 124,
      "has_update": False,
      "mac": "EC64C9C2EFE2",
      "cfg_changed_cnt": 0,
      "actions_stats": {
        "skipped": 0
      },
      "lights": [
        {
          "ison": False,
          "source": "http",
          "has_timer": False,
          "timer_started": 0,
          "timer_duration": 0,
          "timer_remaining": 0,
          "mode": "white",
          "brightness": 100,
          "transition": 0
        }
      ],
      "meters": [
        {
          "power": 0.0,
          "overpower": 0.0,
          "is_valid": True,
          "timestamp": 1723904201,
          "counters": [
            0.0,
            0.0,
            0.0
          ],
          "total": 244
        }
      ],
      "inputs": [
        {
          "input": 0,
          "event": "",
          "event_cnt": 0
        },
        {
          "input": 0,
          "event": "",
          "event_cnt": 0
        }
      ],
      "tmp": {
        "tC": 36.65,
        "tF": 97.98,
        "is_valid": True
      },
      "calibrated": False,
      "calib_progress": 0,
      "calib_status": 0,
      "calib_running": 0,
      "wire_mode": 1,
      "forced_neutral": False,
      "overtemperature": False,
      "loaderror": 0,
      "overpower": False,
      "debug": 0,
      "update": {
        "status": "idle",
        "has_update": False,
        "new_version": "20230913-114008/v1.14.0-gcb84623",
        "old_version": "20230913-114008/v1.14.0-gcb84623",
        "beta_version": "20231107-164738/v1.14.1-rc1-g0617c15"
      },
      "ram_total": 49672,
      "ram_free": 36320,
      "fs_size": 233681,
      "fs_free": 112197,
      "uptime": 7400
    }
    status = Status(**status_json)
    print(status)
    print(status.model_dump_json())
    print(status.model_dump())
