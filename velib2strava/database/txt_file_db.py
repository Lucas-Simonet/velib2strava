DB_PATH = "velib2strava/database/processed_ids.txt"


class TxtFileDb:
    def write_processed_run(self, run_id: str) -> None:
        with open(DB_PATH, "a") as f:
            f.write(f"{run_id}\n")

    def read_processed_runs(self) -> list[int]:
        try:
            with open(DB_PATH, "r") as f:
                return [int(line.strip()) for line in f.readlines()]
        except FileNotFoundError:
            raise FileNotFoundError("Could not load the Database")
