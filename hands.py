from collections import Counter
from dataclasses import dataclass
from typing import Sequence


VALID_SUITS = {"clubs", "diamonds", "hearts", "spades"}


@dataclass(frozen=True)
class Card:
	"""A playing card. Ranks run from 2 to 14, where 11-14 are J-Q-K-A."""

	rank: int
	suit: str


def evaluate_hand(cards: Sequence[Card]) -> str:
	"""Return the strongest poker hand made from one to five selected cards."""
	if not 1 <= len(cards) <= 5:
		raise ValueError("A hand must contain between 1 and 5 cards.")

	for card in cards:
		if not 2 <= card.rank <= 14:
			raise ValueError("Card ranks must be between 2 and 14.")
		if card.suit not in VALID_SUITS:
			raise ValueError(f"Unknown card suit: {card.suit}")

	if len({(card.rank, card.suit) for card in cards}) != len(cards):
		raise ValueError("A hand cannot contain the same card more than once.")

	ranks = [card.rank for card in cards]
	rank_counts = sorted(Counter(ranks).values(), reverse=True)
	is_five_cards = len(cards) == 5
	is_flush = is_five_cards and len({card.suit for card in cards}) == 1
	unique_ranks = set(ranks)
	is_straight = is_five_cards and (
		len(unique_ranks) == 5
		and (
			max(unique_ranks) - min(unique_ranks) == 4
			or unique_ranks == {14, 2, 3, 4, 5}
		)
	)

	if is_straight and is_flush:
		if max(ranks) == 14 and min(ranks) == 10:
			return "Royal Flush"
		return "Straight Flush"
	if rank_counts[0] == 4:
		return "Four of a Kind"
	if rank_counts == [3, 2]:
		return "Full House"
	if is_flush:
		return "Flush"
	if is_straight:
		return "Straight"
	if rank_counts[0] == 3:
		return "Three of a Kind"
	if rank_counts.count(2) == 2:
		return "Two Pair"
	if rank_counts[0] == 2:
		return "Pair"
	return "High Card"
