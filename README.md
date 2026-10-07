# Card Game

A small command-line poker hand game. Each round, you draw five cards from a shuffled standard deck, see the hand type, and get a score.

## Requirements

- Python 3

No external packages are required.

## Run the game

```bash
python Main.py
```

## How to play

- The game deals five cards each round.
- Your hand and score are displayed.
- Press **Enter** to play another hand, or enter **q** to quit.
- The game ends when you quit or there are fewer than five cards left to deal.

## Scoring

A hand's score is calculated as:

**(hand's base chips + card rank values) × hand multiplier**

| Hand | Base chips | Multiplier |
|---|---:|---:|
| High Card | 5 | 1× |
| Pair | 10 | 2× |
| Two Pair | 20 | 2× |
| Three of a Kind | 30 | 3× |
| Straight | 30 | 4× |
| Flush | 35 | 4× |
| Full House | 40 | 4× |
| Four of a Kind | 60 | 7× |
| Straight Flush | 100 | 8× |
| Royal Flush | 100 | 8× |

Card values added to the base chips are their rank for 2–10, 10 for Jack, Queen, and King, and 11 for Ace.

## Project files

- `Main.py` — game loop and command-line interface
- `balatro_stackCards.py` — deck, cards, and player hand
- `hands.py` — poker hand evaluation
- `Score_Psy.py` — hand scoring rules
