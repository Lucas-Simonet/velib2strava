from datetime import datetime
import logging
import pathlib
from typing import Iterable
import gpxpy
import gpxpy.gpx
import numpy as np

logger = logging.getLogger("app")


class GpxClient:
    def __init__(self) -> None:
        self.output_dir = pathlib.Path("velib2strava/generated/")
        self._create_directory()

    def _create_directory(self) -> None:
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            logger.error(f"Error creating directory {self.output_dir}: {e}")

    def create_gpx(
        self, id: str, route_coords: list[list[float]], start_time, end_time
    ) -> None:

        augmented_route_coords = self._augment_route_coords(route_coords)

        timestamps = self._get_time_stamps(
            start_time / 1e3, end_time / 1e3, len(augmented_route_coords)
        )

        gpx = gpxpy.gpx.GPX()
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)
        for coord, time in zip(augmented_route_coords, timestamps, strict=True):
            gpx_segment.points.append(
                gpxpy.gpx.GPXTrackPoint(
                    coord[1], coord[0], time=datetime.fromtimestamp(time)
                )
            )
        with open(self.output_dir / f"{id}.gpx", "w") as gpx_file:
            gpx_file.write(gpx.to_xml())

    def _get_time_stamps(
        self, start_time: int, end_time: int, nb_coord_points
    ) -> Iterable[int]:
        time_stamps: Iterable[int] = np.linspace(
            start_time, end_time, nb_coord_points, dtype=int
        )
        return time_stamps

    def _augment_route_coords(
        self, route_coords: list[list[float]]
    ) -> list[list[float]]:
        augmented_route_coords: list[list[float]] = []
        for i in range(len(route_coords) - 1):
            augmented_route_coords.extend(
                np.linspace(route_coords[i], route_coords[i + 1], endpoint=False)
            )
        augmented_route_coords.append(route_coords[-1])
        return augmented_route_coords
