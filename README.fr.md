# Snake

**Français** | [English](README.md)

Un jeu du serpent en Python pour 1 ou 2 joueurs, avec trois cartes, trois niveaux de difficulté
et une interface graphique basée sur `fltk`.

> Auteur : FARES TOUAZI

## Fonctionnalités

- Mode **solo** ou **deux joueurs** sur le même clavier.
- **3 cartes** avec des murs différents.
- **3 niveaux de difficulté** (le jeu accélère aussi légèrement à chaque pomme mangée).
- Bords traversables : on sort d'un côté du plateau et on réapparaît du côté opposé.
- Possibilité de rejouer directement depuis l'écran de fin.

## Commandes

| Joueur | Haut | Bas | Gauche | Droite |
|---|---|---|---|---|
| 1 | ↑ | ↓ | ← | → |
| 2 | `Z` (ou `W`) | `S` | `Q` (ou `A`) | `D` |

Mangez des pommes pour grandir. Vous perdez si vous heurtez un mur ou un corps de serpent
(le vôtre ou, à deux joueurs, celui de l'adversaire). Si les deux joueurs perdent dans la même
image, la partie est une égalité.

## Installation

Python 3.9 ou supérieur.

```bash
pip install -r requirements.txt
```

Le module graphique **`fltk.py`** n'est pas inclus dans ce dépôt (il appartient à ses propres
auteurs et nous ne pouvons pas le redistribuer). Téléchargez-le depuis la
[source d'origine](https://fltk-b9f35a.frama.io/) et placez-le à la racine du projet, à côté de `main.py`.

## Lancer le jeu

```bash
python main.py
```

## Structure du projet

```
main.py                 point d'entrée
fltk.py                 bibliothèque graphique (fournie séparément, hors dépôt)
assets/                 icône de l'application
snake/
├── app.py              menus de démarrage, puis parties successives
├── jeu.py              boucle de jeu et écran de fin
├── partie.py           état de la partie et application des règles (sans interface)
├── regles.py           fonctions de règles pures (déplacements, collisions, pommes)
├── cartes.py           les trois cartes, dessinées en ASCII
├── constantes.py       taille du plateau, commandes, intervalles de difficulté
├── affichage.py        taille de la fenêtre, conversion case -> pixels
├── dessin.py           dessin d'une image du jeu
├── menus.py            menus de mode / carte / difficulté
├── ui.py               aides pour le texte et les boutons
└── textes.py           tous les textes de l'interface
tests/                  tests unitaires (règles, cartes, partie)
```

`regles.py`, `partie.py` et `cartes.py` ne dépendent pas de `fltk` : ils peuvent être testés sans
écran.

## Tests

```bash
python -m unittest discover -s tests -t . -v
```

## Remerciements

- L'interface graphique repose sur `fltk.py` ([source](https://fltk-b9f35a.frama.io/)), © ses auteurs d'origine.
- Icône *snake* par Mihimihi ([source](https://www.flaticon.com/free-icon/snake_8277654)).

## Licence

Voir le fichier [LICENSE](LICENSE). Elle ne couvre pas `fltk.py` ni l'icône, qui appartiennent à leurs auteurs.
