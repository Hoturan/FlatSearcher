from dataclasses import dataclass


@dataclass
class Flat:
    """Class representing the attributes of a Flat"""

    name: str
    price: float
    price_currency: str
    number_of_rooms: int
    square_meters: str
    summary: str
    link: str
    description: str
