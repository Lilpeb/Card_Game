import random


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []

        suits = ["spades", "hearts", "diamonds", "clubs"]
        ranks = [
            "2", "3", "4", "5", "6", "7", "8", "9",
            "10", "11", "12", "13", "14"
        ]

        # Create the 52 cards
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, amount=1):
        drawn_cards = []

        for _ in range(amount):
            if len(self.cards) > 0:
                drawn_cards.append(self.cards.pop())

        return drawn_cards

    def cards_left(self):
        return len(self.cards)


class PlayerHand:
    def __init__(self):
        self.cards = []

    def add_cards(self, cards):
        self.cards.extend(cards)

    def remove_cards(self, cards):
        for card in cards:
            if card in self.cards:
                self.cards.remove(card)

    def show(self):
        print("\nYour Hand:")
        for number, card in enumerate(self.cards, start=1):
            print(f"{number}. {card}")
