from dataclasses import dataclass


@dataclass
class Property:
    id: int
    title: str
    locality: str
    price: str
    image_urls: list
