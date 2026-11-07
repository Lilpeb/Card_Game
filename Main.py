"""Main game loop for the Balatro-like card game."""

from balatro_stackCards import Deck, PlayerHand
from hands import Card as EvaluatedCard
from hands import evaluate_hand
from Score_Psy import calculate_score
from Score_Psy import check_boss, choose_boss


HAND_SIZE = 8
MAX_CARDS_PER_ACTION = 5
BLIND_TARGET = 300
PLAYS_PER_BLIND = 4
DISCARDS_PER_BLIND = 3
BLIND_NUMBER = 1
BLIND_SCORE_INCREMENT_MULTIPLIER = 1


def choose_cards(player, action_name):
	while True:
		selection = input(
			f"Enter 1-{MAX_CARDS_PER_ACTION} hand positions to {action_name}, "
			"separated by commas: "
		).strip()
		positions = [position.strip() for position in selection.split(",")]

		if not positions or any(not position.isdigit() for position in positions):
			print("Enter hand positions as numbers separated by commas.")
			continue
		if len(positions) > MAX_CARDS_PER_ACTION:
			print(f"You can select at most {MAX_CARDS_PER_ACTION} cards.")
			continue

		positions = [int(position) for position in positions]
		if len(set(positions)) != len(positions):
			print("Each hand position can only be selected once.")
			continue
		if any(position < 1 or position > len(player.cards) for position in positions):
			print("One or more positions are outside your hand.")
			continue

		return [player.cards[position - 1] for position in positions]


def refill_hand(deck, player):
	cards_needed = HAND_SIZE - len(player.cards)
	player.add_cards(deck.draw(cards_needed))


def play_game():
	print("=== CARD HAND GAME ===")
	blind_number = BLIND_NUMBER

	# This outer loop starts another blind after every successful clear.
	while True:
		blind_target = BLIND_TARGET * (
			1 + (blind_number - 1) * BLIND_SCORE_INCREMENT_MULTIPLIER
		)
		boss = choose_boss() if blind_number % 3 == 0 else None

		# Each blind gets a fresh deck, hand, score, and action allowance.
		deck = Deck()
		deck.shuffle()
		player = PlayerHand()
		player.add_cards(deck.draw(HAND_SIZE))
		blind_score = 0
		plays_remaining = PLAYS_PER_BLIND
		discards_remaining = DISCARDS_PER_BLIND

		print(f"\n=== {'Boss Blind' if boss else 'Blind'} {blind_number} | Target: {blind_target} ===")

		while blind_score < blind_target and plays_remaining > 0:
			print(
				f"\nBlind score: {blind_score}/{blind_target} | "
				f"Plays: {plays_remaining} | Discards: {discards_remaining}"
			)
			player.show()

			if not player.cards:
				print("You have no cards left to play.")
				break

			action = input(
				"Choose [p]lay, [d]iscard, or [q]uit: "
			).strip().lower()

			if action == "q":
				print("You quit the game.")
				return
			if action not in ("p", "d"):
				print("Choose p to play, d to discard, or q to quit.")
				continue
			if action == "d" and discards_remaining == 0:
				print("You have no discards remaining.")
				continue

			action_name = "play" if action == "p" else "discard"
			selected_cards = choose_cards(player, action_name)

			if action == "p" and not check_boss(selected_cards, boss):
				print(f"{boss} boss blind condition not met.")
				continue

			if action == "p":
				evaluated_cards = [
					EvaluatedCard(int(card.rank), card.suit)
					for card in selected_cards
				]
				hand_type = evaluate_hand(evaluated_cards)
				hand_score = calculate_score(evaluated_cards, hand_type)
				blind_score += hand_score
				plays_remaining -= 1
				print(f"{hand_type}: {hand_score} points")
			else:
				discards_remaining -= 1
				print(f"Discarded {len(selected_cards)} card(s).")

			player.remove_cards(selected_cards)
			refill_hand(deck, player)
			print(f"Cards remaining in deck: {deck.cards_left()}")

		if blind_score >= blind_target:
			print(f"\nBlind {blind_number} cleared! Final score: {blind_score}")
			# Raise the next target by the configured number of base-target steps.
			blind_number += 1

		else:
			print(
				f"\nGame over on blind {blind_number}. "
				f"Final score: {blind_score}/{blind_target}"
			)
			break

	print("Thanks for playing!")


if __name__ == "__main__":
	play_game()
