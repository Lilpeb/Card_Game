"""Main game loop for the Balatro-like card game."""

import argparse

from balatro_stackCards import Deck, PlayerHand
from hands import Card as EvaluatedCard
from hands import Hand
from Score_Psy import calculate_score
from Score_Psy import check_boss, choose_boss
from savefile import load_game, save_game
from hints import best_play_hint


# Tunable gameplay values for the round flow.
HAND_SIZE = 8
MAX_CARDS_PER_ACTION = 5
BLIND_TARGET = 300
PLAYS_PER_BLIND = 4
DISCARDS_PER_BLIND = 3
BLIND_NUMBER = 1
BLIND_SCORE_INCREMENT_MULTIPLIER = 1
# Fixed for combatability
SUIT_NAMES = {"♠": "spades", "♥": "hearts", "♦": "diamonds", "♣": "clubs"}
# Convert the deck's face-card labels to the numeric ranks used by Hand.
FACE_CARD_RANKS = {"J": 11, "Q": 12, "K": 13, "A": 14}


def choose_cards(player, action_name):
	# Validate a comma-separated list of card positions and return the matching card objects.
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
	# Keep the player's hand at a consistent size after discards or plays.
	cards_needed = HAND_SIZE - len(player.cards)
	player.add_cards(deck.draw(cards_needed))


def play_game(load_saved=False):
	# Main loop: each blind has its own target, deck, and action limits.
	print("=== CARD HAND GAME ===")
	blind_number = BLIND_NUMBER
	deck = Deck()
	player = PlayerHand()
	resume_state = None

	if load_saved or input("Load saved game? [y/N]: ").strip().lower() == "y":
		resume_state = load_game(deck, player)

	# This outer loop starts another blind after every successful clear.
	while True:
		if resume_state is not None:
			blind_number = resume_state["blind_number"]
		blind_target = BLIND_TARGET * (
			1 + (blind_number - 1) * BLIND_SCORE_INCREMENT_MULTIPLIER
		)
		if resume_state is not None:
			blind_score = resume_state["blind_score"]
			plays_remaining = resume_state["plays_remaining"]
			discards_remaining = resume_state["discards_remaining"]
			boss = resume_state["boss"]
			resume_state = None
		else:
			# Each blind gets a fresh deck, hand, score, and action allowance.
			deck = Deck()
			deck.shuffle()
			player = PlayerHand()
			player.add_cards(deck.draw(HAND_SIZE))
			blind_score = 0
			plays_remaining = PLAYS_PER_BLIND
			discards_remaining = DISCARDS_PER_BLIND
			boss = choose_boss() if blind_number % 3 == 0 else None

		print(f"\n=== {'Boss Blind' if boss else 'Blind'} {blind_number} | Target: {blind_target} ===")

		while blind_score < blind_target and plays_remaining > 0:
			# Report the current round state before each action choice.
			print(
				f"\nBlind score: {blind_score}/{blind_target} | "
				f"Plays: {plays_remaining} | Discards: {discards_remaining}"
			)
			player.show()

			if not player.cards:
				print("You have no cards left to play.")
				break

			action = input(
				"Choose [p]lay, [d]iscard, [h]int, [s]ave and quit, or [q]uit: "
			).strip().lower()

			if action == "h":
				# Show a useful legal play without using a play or discard.
				hint = best_play_hint(player.cards, boss)
				if hint is None:
					print("No legal hand is available for this boss blind.")
				else:
					positions, hand_type, score = hint
					print(
						f"Hint: play positions {', '.join(map(str, positions))} "
						f"({hand_type}, {score} points)."
					)
				continue
			if action == "q":
				print("You quit the game.")
				return
			if action == "s":
				save_game(deck, player, {
					"blind_number": blind_number,
					"blind_score": blind_score,
					"plays_remaining": plays_remaining,
					"discards_remaining": discards_remaining,
					"boss": boss,
				})
				return
			if action not in ("p", "d"):
				print("Choose p to play, d to discard, h for a hint, s to save, or q to quit.")
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
				# Score the selected cards as a poker-like hand and advance the blind timer.
				evaluated_cards = [
					EvaluatedCard(
						int(card.rank) if card.rank.isdigit() else FACE_CARD_RANKS[card.rank],
						SUIT_NAMES[card.suit],
					)
					for card in selected_cards
				]
				# Let the selected cards' Hand object determine their poker category.
				hand_type = Hand(evaluated_cards).evaluate()
				hand_score = calculate_score(evaluated_cards, hand_type)
				blind_score += hand_score
				plays_remaining -= 1
				print(f"{hand_type}: {hand_score} points")
			else:
				discards_remaining -= 1
				print(f"Discarded {len(selected_cards)} card(s).")

			# Replace played/discarded cards so the hand stays full for the next turn.
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
	# --load resumes a save directly; without it, play_game prompts as usual.
	parser = argparse.ArgumentParser(description="Play the Balatro-like card game.")
	parser.add_argument(
		"--load",
		action="store_true",
		help="load the saved game without prompting",
	)
	play_game(load_saved=parser.parse_args().load)
