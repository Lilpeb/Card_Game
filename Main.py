"""Main game loop for the Balatro-like card game."""

from balatro_stackCards import Deck, PlayerHand
from hands import Card as EvaluatedCard
from hands import evaluate_hand
from Score_Psy import calculate_score



def play_game():
	deck = Deck()
	deck.shuffle()
	round_number = 1

	print("=== CARD HAND GAME ===")

	while deck.cards_left() >= 5:
		player = PlayerHand()
		player.add_cards(deck.draw(5))

		print(f"\nRound {round_number}")
		player.show()

		evaluator_cards = [
			EvaluatedCard(int(card.rank), card.suit) for card in player.cards
		]
		hand_type = evaluate_hand(evaluator_cards)
		print(f"Hand: {hand_type}")
		print(f"Score: {calculate_score(evaluator_cards, hand_type)}")
		print(f"Cards remaining in deck: {deck.cards_left()}")
		round_number += 1

		if deck.cards_left() < 5:
			break
		if input("\nPress Enter to play another hand, or q to quit: ").strip().lower() == "q":
			break

	print("\nThanks for playing!")


if __name__ == "__main__":
	play_game()
