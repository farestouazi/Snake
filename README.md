# Snake

[Français](README.fr.md) | **English**

A Snake game in Python for 1 or 2 players, with three maps, three difficulty levels and a
graphical interface built on `fltk`.

> Author: FARES TOUAZI

## Features

- **Solo** or **two-player** mode on the same keyboard.
- **3 maps** with different wall layouts.
- **3 difficulty levels** (the game also speeds up slightly with every apple eaten).
- Screen wrap-around: leave the board on one side and come back on the opposite one.
- Replay straight from the end screen.

## Controls

| Player | Up | Down | Left | Right |
|---|---|---|---|---|
| 1 | ↑ | ↓ | ← | → |
| 2 | `Z` (or `W`) | `S` | `Q` (or `A`) | `D` |

Eat apples to grow. You lose if you hit a wall or a snake body (your own or, in two-player
mode, your opponent's). If both players crash in the same frame, the game is a draw.

## Installation

Python 3.9 or later.

```bash
pip install -r requirements.txt
```

The graphical module **`fltk.py`** is not included in this repository (it belongs to its own
authors and is not ours to redistribute). Download it from the [original source](https://fltk-b9f35a.frama.io/) and
put it at the project root, next to `main.py`.

## Run

```bash
python main.py
```

## Project structure

```
main.py                 entry point
fltk.py                 graphics library (provided separately, not in the repo)
assets/                 application icon
snake/
├── app.py              start-up menus, then successive games
├── jeu.py              game loop and end screen
├── partie.py           game state and rules in action (no GUI)
├── regles.py           pure rule functions (moves, collisions, apples)
├── cartes.py           the three maps, drawn in ASCII
├── constantes.py       board size, controls, difficulty intervals
├── affichage.py        window size, cell -> pixel conversion
├── dessin.py           drawing of one frame
├── menus.py            mode / map / difficulty menus
├── ui.py               text and button helpers
└── textes.py           all interface texts
tests/                  unit tests (rules, maps, game)
```

`regles.py`, `partie.py` and `cartes.py` do not depend on `fltk`, so they can be tested without a
display. (Module and identifier names are in French, as in the original project.)

## Tests

```bash
python -m unittest discover -s tests -t . -v
```

## Credits

- Graphics are powered by `fltk.py` ([source](https://fltk-b9f35a.frama.io/)), © its original authors.
- Icon *snake* by Mihimihi ([source](https://www.flaticon.com/free-icon/snake_8277654)).

## License

See the [LICENSE](LICENSE) file. It does not cover `fltk.py` or the icon, which belong to their own authors.
