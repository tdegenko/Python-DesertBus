import datetime
import typing


class Logo(typing.NamedTuple):
    url: str
    alt: str
    width: int
    height: int

    @classmethod
    def from_json(cls, data: dict) -> "Logo":
        return cls(
            url=data["url"],
            alt=data["alt"],
            width=data["width"],
            height=data["height"],
        )


class Auction:
    def __init__(self):
        raise NotImplementedError

    @classmethod
    def from_json(cls, data: dict) -> "Auction":
        return cls()


class Blog:
    def __init__(self):
        raise NotImplementedError

    @classmethod
    def from_json(cls, data: dict) -> "Blog":
        return cls()


class Donation:
    def __init__(self):
        raise NotImplementedError

    @classmethod
    def from_json(cls, data: dict) -> "Donation":
        return cls()


class Prize:
    def __init__(self):
        raise NotImplementedError

    @classmethod
    def from_json(cls, data: dict) -> "Prize":
        return cls()


class Total(typing.NamedTuple):
    currency: str
    amount: float
    updated_at: datetime.datetime

    @classmethod
    def from_json(cls, data: dict) -> "Total":
        return cls(
            currency=data["currency"],
            amount=data["amount"],
            updated_at=datetime.datetime.fromisoformat(data["updated_at"]),
        )
