import json
import logging
from pydantic import BaseModel, field_validator
from requests import request

STATION_INFO_PATH = "velib2strava/resource/station_information.json"

logger = logging.getLogger("app")

velib_station_dict: dict[int, dict[str, str | float | int]] = {}


def _load_station_info(velib_station_dict, STATION_INFO_PATH):
    with open(STATION_INFO_PATH, "r") as file:
        station_json = json.load(file)
        for station in station_json["data"]["stations"]:
            velib_station_dict[station["station_id"]] = station


try:
    _load_station_info(velib_station_dict, STATION_INFO_PATH)
except FileNotFoundError:
    station_data = request(
        "get",
        "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json",
    )
    with open(STATION_INFO_PATH, "w") as file:
        file.write(json.dumps(station_data.json()))

    _load_station_info(velib_station_dict, STATION_INFO_PATH)


class VelibStation(BaseModel):
    station_id: int
    station_name: str
    lat: float
    lon: float


def get_velib_station_from_id(id: int) -> VelibStation:
    dict_entry = velib_station_dict[id]
    if dict_entry:
        station = VelibStation(
            station_id=id,
            station_name=str(dict_entry["name"]),
            lat=float(dict_entry["lat"]),
            lon=float(dict_entry["lon"]),
        )
        return station
    raise ValueError("Could not find station based on station id")


class VelibRun(BaseModel):
    id: int
    start_point: VelibStation
    end_point: VelibStation
    distance: float
    # bike_type: Literal["mechanical", "electrical"]
    average_speed: float
    start_time: int
    end_time: int

    @field_validator("distance")
    def check_distance(cls, value):
        if value < 150:
            raise ValueError("False run, unusable bike")
        return value

    @field_validator("start_point", "end_point", mode="before")
    def check_station_coord(cls, value):
        try:
            station = get_velib_station_from_id(int(value))
        except Exception as e:
            logger.info(e)
        return station
