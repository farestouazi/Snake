"""Constantes du jeu (aucune dépendance à l'interface)."""
from typing import Dict, Tuple

Case = Tuple[int, int]  # (colonne, ligne)

# --- Plateau ---------------------------------------------------------------
LARGEUR_PLATEAU = 40
HAUTEUR_PLATEAU = 30
LIGNES_ENTETE = 4  # bandeau des scores au-dessus du plateau
LIGNE_MIN = LIGNES_ENTETE
LIGNE_MAX = LIGNES_ENTETE + HAUTEUR_PLATEAU - 1

# --- Règles ----------------------------------------------------------------
LONGUEUR_INITIALE = 4
NOMBRE_POMMES = 3
ACCELERATION_PAR_POMME = 0.9982  # l'intervalle entre deux images est multiplié par ce facteur

# Intervalle (en secondes) entre deux images : facile, moyen, difficile.
INTERVALLES = (0.5, 0.15, 0.04)

# --- Directions et commandes -----------------------------------------------
HAUT, BAS, GAUCHE, DROITE = (0, -1), (0, 1), (-1, 0), (1, 0)

# Joueur 1 : flèches. Joueur 2 : ZQSD (AZERTY) ou WASD (QWERTY).
COMMANDES: Dict[int, Dict[str, Case]] = {
    1: {"Up": HAUT, "Down": BAS, "Left": GAUCHE, "Right": DROITE},
    2: {"z": HAUT, "w": HAUT, "s": BAS, "q": GAUCHE, "a": GAUCHE, "d": DROITE},
}
