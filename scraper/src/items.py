from dataclasses import dataclass


@dataclass
class PropertyItem:
    id: int
    title: str
    locality: str
    price: str
    image_urls: list
