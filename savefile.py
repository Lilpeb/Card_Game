import json
from balatro_stackCards import Card

SAVE_FILE = "balatro_save.json"

def save_game(deck, player, game_state):
    """Save the current blind, deck, and player's hand."""

    game_data = {
        "deck": [
            {"rank": card.rank, "suit": card.suit}
            for card in deck.cards
        ],

        "player_hand": [
            {"rank": card.rank, "suit": card.suit}
            for card in player.cards
        ],
        "game_state": game_state,
    }

    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        json.dump(game_data, file, indent=4)

    print("\nGame saved successfully!")

def load_game(deck, player):
    """Restore a saved deck and hand, returning the saved blind state."""

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            game_data = json.load(file)

        if not isinstance(game_data, dict):
            raise ValueError("Saved game must be an object.")
        saved_deck = [
            Card(card["rank"], card["suit"])
            for card in game_data["deck"]
        ]
        saved_hand = [
            Card(card["rank"], card["suit"])
            for card in game_data["player_hand"]
        ]
        game_state = game_data["game_state"]
        required_state = (
            "blind_number",
            "blind_score",
            "plays_remaining",
            "discards_remaining",
            "boss",
        )
        if not isinstance(game_state, dict) or any(
            key not in game_state for key in required_state
        ):
            raise ValueError("Saved blind state is incomplete.")
        numeric_state = required_state[:-1]
        if any(type(game_state[key]) is not int for key in numeric_state):
            raise ValueError("Saved blind values must be integers.")
        if (
            game_state["blind_number"] < 1
            or game_state["blind_score"] < 0
            or game_state["plays_remaining"] < 0
            or game_state["discards_remaining"] < 0
            or game_state["boss"] not in (None, "Psychic")
        ):
            raise ValueError("Saved blind values are outside the allowed range.")

        deck.cards = saved_deck
        player.cards = saved_hand

        print("\nGame loaded successfully!")
        return game_state

    except FileNotFoundError:
        print("\nNo save file found. Starting a new game.")
        return False

    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        print("\nSave file is damaged or invalid. Starting a new game.")
        return False