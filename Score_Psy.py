import random


hands_scores = {
    "High Card": [5, 1],
    "Pair": [10, 2],
    "Two Pair": [20, 2],
    "Three of a Kind": [30, 3],
    "Straight": [30, 4],
    "Flush": [35, 4],
    "Full House": [40, 4],
    "Four of a Kind": [60, 7],
    "Straight Flush": [100, 8],
    "Royal Flush": [100, 8]
}

class Scorer:
    def __init__(self):
        self.hands_scores = hands_scores

    def value_of_cards(self, rank):
        if rank <= 10:
            return rank
        elif rank == 14:
            return 11
        else:
            return 10

    def _sum_card_values(self, scoring_cards, index=0):
        # Stop once every selected card's value has been added.
        if index == len(scoring_cards):
            return 0
        # Add this card, then recurse with the next position.
        return (
            self.value_of_cards(scoring_cards[index].rank)
            + self._sum_card_values(scoring_cards, index + 1)
        )

    def calculate_score(self, scoring_cards, hand_type):
        chips = self.hands_scores[hand_type][0]
        mult = self.hands_scores[hand_type][1]
        chips += self._sum_card_values(scoring_cards)
        return chips * mult

def value_of_cards(rank):
    if rank <= 10:
        return rank

    elif rank == 14:
        return 11

    else:
        return 10


def calculate_score(scoring_cards, hand_type):
    scorer = Scorer()
    return scorer.calculate_score(scoring_cards, hand_type)


boss_blinds = {
    "Psychic": lambda played_cards: len(played_cards) == 5,
}


def choose_boss():
    return random.choice(tuple(boss_blinds))


def check_boss(played_cards, boss):
    return boss is None or boss_blinds[boss](played_cards)
