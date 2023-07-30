import enum
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class Item:
    members: bool
    name: str
    examine: str
    icon: str
    id: int
    value: int
    highalch: int = 0
    lowalch: int = 0
    limit: int = -1


@dataclass
class ItemPrice:
    high: int = 0
    highTime: int = 0
    low: int = 0
    lowTime: int = 0


@dataclass
class ItemPriceAvg:
    avgHighPrice: int = 0
    highPriceVolume: int = 0
    avgLowPrice: int = 0
    lowPriceVolume: int = 0


@dataclass
class ItemPriceSeries:
    timestamp: int = 0
    avgHighPrice: int = 0
    highPriceVolume: int = 0
    avgLowPrice: int = 0
    lowPriceVolume: int = 0


class TimeStep(enum.Enum):
    FIVE_MIN = "5m"
    ONE_HOUR = "1h"
    SIX_HOUR = "6h"
    ONE_DAY = "24f"


def get_latest_price() -> dict[int, ItemPrice]:
    prices = requests.get("https://prices.runescape.wiki/api/v1/osrs/latest").json()[
        "data"
    ]
    prices_parsed = {
        int(item_id): ItemPrice(**price) for item_id, price in prices.items()
    }
    return prices_parsed


def get_5m_price(timestamp: Optional[int] = None) -> dict[int, ItemPriceAvg]:
    if timestamp is None:
        prices = requests.get("https://prices.runescape.wiki/api/v1/osrs/5m").json()[
            "data"
        ]
    else:
        prices = requests.get(
            "https://prices.runescape.wiki/api/v1/osrs/5m",
            params={"timestamp": timestamp},
        ).json()["data"]
    prices_parsed = {
        int(item_id): ItemPriceAvg(**price) for item_id, price in prices.items()
    }
    return prices_parsed


def get_1h_price(timestamp: Optional[int] = None) -> dict[int, ItemPriceAvg]:
    if timestamp is None:
        prices = requests.get("https://prices.runescape.wiki/api/v1/osrs/1h").json()[
            "data"
        ]
    else:
        prices = requests.get(
            "https://prices.runescape.wiki/api/v1/osrs/1h",
            params={"timestamp": timestamp},
        ).json()["data"]
    prices_parsed = {
        int(item_id): ItemPriceAvg(**price) for item_id, price in prices.items()
    }
    return prices_parsed


def get_timeseries(item_id: int, timestep: TimeStep) -> list[ItemPriceSeries]:
    prices = requests.get(
        "https://prices.runescape.wiki/api/v1/osrs/timeseries",
        params={"id": item_id, "timestep": timestep.value},
    ).json()["data"]
    prices_parsed = [ItemPriceSeries(**price) for price in prices]
    return prices_parsed


def get_all_item_info() -> dict[int, Item]:
    items = requests.get("https://prices.runescape.wiki/api/v1/osrs/mapping").json()
    items_parsed = {item["id"]: Item(**item) for item in items}
    return items_parsed


def get_latest_price_for_item(item_id: int) -> Optional[ItemPrice]:
    all_prices = get_latest_price()
    if item_id not in all_prices:
        print("Couldn't find latest price for item, is it tradeable?")
        return None
    else:
        return all_prices[item_id]


def get_latest_5m_price_for_item(item_id: int) -> Optional[ItemPriceAvg]:
    all_prices = get_5m_price()
    if item_id not in all_prices:
        print("Couldn't find latest price for item, is it tradeable?")
        return None
    else:
        return all_prices[item_id]


def get_latest_1h_price_for_item(item_id: int) -> Optional[ItemPriceAvg]:
    all_prices = get_1h_price()
    if item_id not in all_prices:
        print("Couldn't find latest price for item, is it tradeable?")
        return None
    else:
        return all_prices[item_id]
