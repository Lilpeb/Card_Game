# Card Game

A small command-line poker hand game. Each blind, you draw eight cards from a shuffled standard deck and play selected hands to reach a score target. Every third blind adds a boss condition.

## Requirements

- Python 3

No external packages are required.

## Run the game

```bash
python Main.py
```

To load a saved game directly without the startup prompt:

```bash
python Main.py --load
```

## How to play

- At startup, enter **y** to resume a saved game, or press **Enter** to start a new one.
- Choose **p** to play up to five selected cards, **d** to discard them and draw replacements, or **h** to get a hint for the highest-scoring legal play.
- Enter hand positions separated by commas when prompted.
- Choose **s** to save and quit, or **q** to quit without saving.
- Hints do not use a play or discard. Boss conditions are applied when finding a hint.
- Each blind allows four plays and three discards. Reach its target score to advance.

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
