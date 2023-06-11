from dataclasses import dataclass

ID = "id"
NAME = "name"
PRICE = "price"
PRICE_CURRENCY = "price_currency"
NUMBER_OF_ROOMS = "number_of_rooms"
SPACE = "space"
LINK = "link"
DESCRIPTION = "description"
SUMMARY = "summary"
LOCATION = "location"

@dataclass
class Flat:
    """Class representing the attributes of a Flat"""
    id: int
    name: str
    price: float
    price_currency: str
    number_of_rooms: int
    space: str
    summary: str
    link: str
    description: str
    location: str = "Unknown"

    def to_json(self):
        return {
            ID: self.id,
            NAME: self.name,
            PRICE: self.price,
            PRICE_CURRENCY: self.price_currency,
            NUMBER_OF_ROOMS: self.number_of_rooms,
            SPACE: self.space,
            LINK: self.link,
            DESCRIPTION: self.description,
            SUMMARY: self.summary,
            LOCATION: self.location
        }
