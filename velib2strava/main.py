import json
import logging.config
import os
import pathlib
from velib2strava.client.gpx_client import GpxClient
from velib2strava.client.router_client import RouterClient
from velib2strava.client.strava_client import StravaClient
from velib2strava.client.velib_client import VelibClient

from velib2strava.database.txt_file_db import TxtFileDb

logger = logging.getLogger("app")


def setup_logging():
    config_file = pathlib.Path("velib2strava/resource/log_config.json")
    with open(config_file) as file:
        config = json.load(file)
    logging.config.dictConfig(config)


def main():
    setup_logging()
    strava_token_path = os.getenv("STRAVA_ACCESS_TOKEN_PATH")
    strava_client_id = os.getenv("STRAVA_CLIENT_ID")
    strava_client_secret = os.getenv("STRAVA_CLIENT_SECRET")
    velib_client = VelibClient()
    strava_client = StravaClient(
        strava_token_path, strava_client_id, strava_client_secret
    )
    router_client = RouterClient()
    gpx_client = GpxClient()
    file_db = TxtFileDb()
    processed_ids = file_db.read_processed_runs()

    ride_list = velib_client.get_rides()
    for ride in ride_list:
        if ride.id in processed_ids:
            logger.info((f"already proccessed run {ride.id}"))
        else:
            route_coords = router_client.get_points_from_velib_run(ride)
            gpx_client.create_gpx(
                ride.id,
                route_coords,
                start_time=ride.start_time,
                end_time=ride.end_time,
            )
            strava_client.upload_ride(ride)
            file_db.write_processed_run(ride.id)


if __name__ == "__main__":
    main()
