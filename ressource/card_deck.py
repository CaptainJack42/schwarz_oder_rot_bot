from dataclasses import dataclass
from enum import IntEnum
from random import randint


class CardColor(IntEnum):
    HEARTS = 0
    DIAMONDS = 1
    SPADES = 2
    CLUBS = 3


class Card(dataclass):
    color: CardColor
    value: int


class CardDeck():
    CARD_VALUE_MAP: dict = {
        2: '2',
        3: '3',
        4: '4',
        5: '5',
        6: '6',
        7: '7',
        8: '8',
        9: '9',
        10: '10',
        11: 'Jack',
        12: 'Queen',
        13: 'King',
        14: 'Ace',
    }

    def __init__(self) -> None:
        self.deck: list[Card]
        for color in CardColor:
            for (key, _) in self.CARD_VALUE_MAP:
                self.deck.append(Card(color, key))

    def draw_card(self) -> Card:
        rand: int = randint(0, len(self.deck) - 1)
        return self.deck.pop(rand)
