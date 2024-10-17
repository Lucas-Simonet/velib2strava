import json
import logging
import time
from stravalib import Client
from velib2strava.model.run import VelibRun

logger = logging.getLogger("app")


class StravaClient:
    def __init__(
        self, access_token_path: str, client_id: int, client_secret: str
    ) -> None:
        self.client = Client()
        try:
            with open(access_token_path, "r") as f:
                access_token = json.load(f)

        except FileNotFoundError:
            self._handle_access_token_retrieval(
                access_token_path, client_id, client_secret
            )

        finally:
            with open(access_token_path, "r") as f:
                access_token = json.load(f)

        self._handle_access_token_refresh(
            access_token_path, client_id, client_secret, access_token
        )

    def _handle_access_token_refresh(
        self, access_token_path, client_id, client_secret, access_token
    ):
        if time.time() > access_token["expires_at"]:
            logger.warning("Token has expired, will refresh")
            refresh_response = self.client.refresh_access_token(
                client_id=client_id,
                client_secret=client_secret,
                refresh_token=access_token["refresh_token"],
            )
            access_token = refresh_response
            with open(access_token_path, "w") as f:
                json.dump(refresh_response, f)
            logger.info("Refreshed token saved to file")
            self.client.access_token = refresh_response["access_token"]
        else:
            logger.info("Access token still valid")
            self.client.access_token = access_token["access_token"]

    def _handle_access_token_retrieval(
        self, access_token_path, client_id, client_secret
    ):
        logger.warning(
            "no token file found, generating url to get one. Please log in at : "
        )
        url = self.client.authorization_url(
            client_id=client_id,
            redirect_uri="http://127.0.0.1:5000/authorization",
            scope=[
                "read",
                "read_all",
                "profile:read_all",
                "profile:write",
                "activity:read",
                "activity:read_all",
                "activity:write",
            ],
        )
        logger.warning("\n", url, "\n")
        logger.warning("And copy paste the code in the redirected url")
        code = input()
        access_token = self.client.exchange_code_for_token(
            client_id=client_id, client_secret=client_secret, code=code
        )
        with open(access_token_path, "w") as f:
            json.dump(access_token, f)

    def upload_ride(self, ride: VelibRun) -> None:
        activity_name = f"My Vélib Ride {ride.start_point.station_name} / {ride.end_point.station_name}"
        with open(f"velib2strava/generated/{ride.id}.gpx", "rb") as gpx_file:
            activity = self.client.upload_activity(
                activity_file=gpx_file,
                data_type="gpx",
                name=activity_name,
                activity_type="ride",
            )
        try:
            detailed_activty = activity.wait()
        except Exception:
            logger.error(detailed_activty)

        if detailed_activty and detailed_activty.id:
            self.client.update_activity(
                activity_id=detailed_activty.id,
                name=activity_name,
                sport_type="Ride",
                hide_from_home=True,
            )
        logger.info(f"processed run : {activity_name}")
