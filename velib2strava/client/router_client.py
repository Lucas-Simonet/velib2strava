from requests import request
from velib2strava.model.run import VelibRun


class RouterClient:
    def __init__(self) -> None:
        pass

    def get_points_from_velib_run(
        self, velib_run: VelibRun
    ) -> list[list[float]] | None:
        coord = f"{velib_run.start_point.lon},{velib_run.start_point.lat};{velib_run.end_point.lon},{velib_run.end_point.lat}"
        response = request(
            "get",
            f"http://router.project-osrm.org/route/v1/bike/{coord}?steps=true&geometries=geojson&alternatives=true",
        )
        real_distance = velib_run.distance
        data = response.json()
        if "routes" in data:
            best_route = self._choose_most_representative_route(real_distance, data)
            return best_route
        else:
            return None

    def _choose_most_representative_route(
        self, real_distance: float, data: dict
    ) -> list[list[float]]:
        best_distance_diff = real_distance
        route_index: int = 0
        for index, route in enumerate(data["routes"]):
            if abs(real_distance - route["distance"]) < best_distance_diff:
                best_distance_diff = abs(real_distance - route["distance"])
                route_index = index
        return data["routes"][route_index]["geometry"]["coordinates"]
