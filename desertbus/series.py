import json
import typing

import desertbus
from desertbus import util


class Series(typing.NamedTuple):
    name: str
    id: str

    @classmethod
    def from_json(cls, data: dict) -> "Series":
        return cls(name=data["name"], id=data["id"])

    def fetch_events(self) -> list[desertbus.Event]:
        return desertbus.get_events(self)


def get_series() -> list[Series]:
    with util.url_opener().open(util.build_db_url(path_parts=["series"])) as response:
        if response.status != 200:
            raise RuntimeError(
                "Bad response for API request: {response.status}: {response.reason}"
            )
        series_json = json.load(response)
        return [Series.from_json(s) for s in series_json["series"]]
