import datetime
import json
import typing

import desertbus
from desertbus import data_types, util


class Event(typing.NamedTuple):
    name: str
    event_id: str
    url: str
    primary: bool
    start_time: datetime.datetime
    logo: data_types.Logo
    total: data_types.Total
    series: "desertbus.Series"

    @classmethod
    def from_json(cls, data: dict) -> "Event":
        return cls(
            name=data["name"],
            event_id=data["id"],
            url=data["url"],
            primary=data["primary"],
            start_time=datetime.datetime.fromisoformat(data["starts_at"]),
            logo=data_types.Logo.from_json(data["logo"]),
            total=data_types.Total.from_json(data["total"]),
            series=desertbus.Series.from_json(data["series"]),
        )

    def fetch_blog_posts(self) -> None:
        raise NotImplementedError

    def fetch_donations(self) -> None:
        raise NotImplementedError

    def fetch_guests(self) -> None:
        raise NotImplementedError

    def fetch_prizes(self) -> None:
        raise NotImplementedError


def get_events(series: "desertbus.Series | str") -> list[Event]:
    if isinstance(series, desertbus.Series):
        series = series.id
    with util.url_opener().open(
        util.build_db_url(path_parts=["events"], parameters={"series": series})
    ) as response:
        if response.status != 200:
            raise RuntimeError(
                "Bad response for API request: {response.status}: {response.reason}"
            )
        events_json = json.load(response)
        return [Event.from_json(event) for event in events_json["events"]]
