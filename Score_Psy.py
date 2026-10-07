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


def value_of_cards(rank):
    if rank <= 10:
        return rank

    elif rank == 14:
        return 11

    else:
        return 10


def calculate_score(scoring_cards, hand_type):
    chips = hands_scores[hand_type][0]
    mult = hands_scores[hand_type][1]

    for card in scoring_cards:
        chips = chips + value_of_cards(card.rank)

    score = chips * mult

    return score


def check_boss(played_cards, boss):
    if boss == "Psychic":
        if len(played_cards) != 5:
            return False

    return True