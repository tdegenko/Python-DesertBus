import enum
import json
import typing

import phxsocket

import desertbus
from desertbus import constants, data_types

AuctionCallbackType = typing.Callable[[data_types.Auction], None]
BlogCallbackType = typing.Callable[[data_types.Blog], None]
DonationCallbackType = typing.Callable[[data_types.Donation], None]
PrizeCallbackType = typing.Callable[[data_types.Prize], None]
TotalCallbackType = typing.Callable[[data_types.Total], None]


class ListenTopics(enum.Enum):
    AUCTION = "auctions"
    BLOG = "blog"
    DONATION = "donations"
    PRIZE = "prizes"
    TOTAL = "total"


TOPIC_EVENTS = {
    ListenTopics.AUCTION: "auction",
    ListenTopics.BLOG: "blog",
    ListenTopics.DONATION: "donation",
    ListenTopics.PRIZE: "prize",
    ListenTopics.TOTAL: "total",
}


class PHXClient(phxsocket.Client):
    @property
    def connected(self):
        return self._loop is not None


class PushListener:
    def __init__(self, event: desertbus.Event) -> None:
        self.event = event
        self.phxsocket = None
        self._auction_cbs: set[AuctionCallbackType] = set()
        self._blog_cbs: set[BlogCallbackType] = set()
        self._donation_cbs: set[DonationCallbackType] = set()
        self._prize_cbs: set[PrizeCallbackType] = set()
        self._total_cbs: set[TotalCallbackType] = set()
        self.TOPIC_HANDLER_MAP = {
            ListenTopics.AUCTION.value: self._handle_auction,
            ListenTopics.BLOG.value: self._handle_blog,
            ListenTopics.DONATION.value: self._handle_donation,
            ListenTopics.PRIZE.value: self._handle_prize,
            ListenTopics.TOTAL.value: self._handle_total,
        }

    def setup(
        self,
        topics: set[ListenTopics] = {
            ListenTopics.TOTAL,
        },
    ):
        self.phxsocket = PHXClient(constants.WEBSOCKET_URL)
        if not self.phxsocket.connect():
            raise RuntimeError("Could not connect phoenix channel socket")
        for key, handler in self.TOPIC_HANDLER_MAP.items():
            topic = ListenTopics(key)
            if topic not in topics:
                continue
            channel = self.phxsocket.channel(f"{key}:{self.event.event_id}")
            channel.on(TOPIC_EVENTS[topic], handler)
            response = channel.join()
            if response is not None:
                handler(response)

    def teardown(self):
        self.phxsocket.close()

    @property
    def connected(self):
        if self.phxsocket is None:
            return False
        return self.phxsocket.connected

    def subscribe_auction(self, callback: AuctionCallbackType) -> None:
        self._auction_cbs.add(callback)

    def unsubscribe_auction(self, callback: AuctionCallbackType) -> bool:
        if callback in self._auction_cbs:
            return False
        self._auction_cbs.remove(callback)
        return True

    def get_callbacks_auction(
        self, callback: AuctionCallbackType
    ) -> set[AuctionCallbackType]:
        return self._auction_cbs

    def subscribe_blog(self, callback: BlogCallbackType) -> None:
        self._blog_cbs.add(callback)

    def unsubscribe_blog(self, callback: BlogCallbackType) -> bool:
        if callback in self._blog_cbs:
            return False
        self._blog_cbs.remove(callback)
        return True

    def get_callbacks_blog(self, callback: BlogCallbackType) -> set[BlogCallbackType]:
        return self._blog_cbs

    def subscribe_donation(self, callback: DonationCallbackType) -> None:
        self._donation_cbs.add(callback)

    def unsubscribe_donation(self, callback: DonationCallbackType) -> bool:
        if callback in self._donation_cbs:
            return False
        self._donation_cbs.remove(callback)
        return True

    def get_callbacks_donation(
        self, callback: DonationCallbackType
    ) -> set[DonationCallbackType]:
        return self._donation_cbs

    def subscribe_prize(self, callback: PrizeCallbackType) -> None:
        self._prize_cbs.add(callback)

    def unsubscribe_prize(self, callback: PrizeCallbackType) -> bool:
        if callback in self._prize_cbs:
            return False
        self._prize_cbs.remove(callback)
        return True

    def get_callbacks_prize(
        self, callback: PrizeCallbackType
    ) -> set[PrizeCallbackType]:
        return self._prize_cbs

    def subscribe_total(self, callback: TotalCallbackType) -> None:
        self._total_cbs.add(callback)

    def unsubscribe_total(self, callback: TotalCallbackType) -> bool:
        if callback in self._total_cbs:
            return False
        self._total_cbs.remove(callback)
        return True

    def get_callbacks_total(
        self, callback: TotalCallbackType
    ) -> set[TotalCallbackType]:
        return self._total_cbs

    def _handle_auction(self, message: phxsocket.Message) -> None:
        if not self._auction_cbs:
            return
        auction = data_types.Auction.from_json(json.loads(message.payload))
        for cb in self._auction_cbs:
            cb(auction)

    def _handle_blog(self, message: phxsocket.Message) -> None:
        if not self._blog_cbs:
            return
        blog = data_types.Blog.from_json(json.loads(message.payload))
        for cb in self._blog_cbs:
            cb(blog)

    def _handle_donation(self, message: phxsocket.Message) -> None:
        if not self._donation_cbs:
            return
        donation = data_types.Donation.from_json(json.loads(message.payload))
        for cb in self._donation_cbs:
            cb(donation)

    def _handle_prize(self, message: phxsocket.Message) -> None:
        if not self._prize_cbs:
            return
        prize = data_types.Prize.from_json(json.loads(message.payload))
        for cb in self._prize_cbs:
            cb(prize)

    def _handle_total(self, message: phxsocket.Message) -> None:
        if not self._total_cbs:
            return
        total = data_types.Total.from_json(message)
        for cb in self._total_cbs:
            cb(total)
