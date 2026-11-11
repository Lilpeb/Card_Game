"""Find a highest-scoring legal play for the game's hint option."""

from hands import Card as EvaluatedCard
from hands import Hand
from Score_Psy import Scorer, check_boss

# Convert the deck's display labels to the ranks and suits used by the evaluator.
SUIT_NAMES = {"♠": "spades", "♥": "hearts", "♦": "diamonds", "♣": "clubs"}
FACE_CARD_RANKS = {"J": 11, "Q": 12, "K": 13, "A": 14}


def best_play_hint(cards, boss):
	"""Return the best legal play as (positions, hand type, score), or None."""
	# Load the scoring configuration once for the full recursive search.
	scorer = Scorer()
	best = None

	def search(start, selected):
		# Score each nonempty selection that satisfies the current boss condition.
		nonlocal best
		if selected and check_boss(selected, boss):
			converted = [
				EvaluatedCard(
					int(card.rank) if card.rank.isdigit() else FACE_CARD_RANKS[card.rank],
					SUIT_NAMES[card.suit],
				)
				for card in selected
			]
			hand_type = Hand(converted).evaluate()
			score = scorer.calculate_score(converted, hand_type)
			if best is None or score > best[2]:
				best = (
					tuple(cards.index(card) + 1 for card in selected),
					hand_type,
					score,
				)

		# Recursively choose remaining cards, stopping at the five-card play limit.
		if len(selected) < 5:
			for index in range(start, len(cards)):
				selected.append(cards[index])
				search(index + 1, selected)
				selected.pop()

	# Start the recursive search with an empty selection.
	search(0, [])
	return best
