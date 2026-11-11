"""Taille de la fenêtre et conversion cases -> pixels."""
from __future__ import annotations

from typing import Optional, Tuple

from .constantes import HAUTEUR_PLATEAU, LARGEUR_PLATEAU, LIGNES_ENTETE, Case

TAILLES_DISPONIBLES = tuple(range(12, 26))  # taille d'une case, en pixels
TAILLE_PAR_DEFAUT = 20
FACTEUR_LARGEUR = 75
FACTEUR_HAUTEUR = 40

def _dimensions_ecran() -> Optional[Tuple[int, int]]:
    """Retourne (largeur, hauteur) de l'écran, ou None s'il est inconnu."""
    try:
        import pyautogui

        taille = pyautogui.size()
        return int(taille[0]), int(taille[1])
    except Exception:  # bibliothèque absente, pas d'écran, etc.
        return None

def trouver_taille_case(dimensions: Optional[Tuple[int, int]] = None) -> int:
    """Choisit la plus grande taille de case qui tient confortablement à l'écran."""
    if dimensions is None:
        return TAILLE_PAR_DEFAUT
    largeur, hauteur = dimensions
    possibles = [
        t for t in TAILLES_DISPONIBLES
        if t * FACTEUR_LARGEUR < largeur and t * FACTEUR_HAUTEUR < hauteur
    ]
    return max(possibles) if possibles else min(TAILLES_DISPONIBLES)

TAILLE_CASE = trouver_taille_case(_dimensions_ecran())
LARGEUR_FENETRE = TAILLE_CASE * LARGEUR_PLATEAU
HAUTEUR_FENETRE = TAILLE_CASE * (LIGNES_ENTETE + HAUTEUR_PLATEAU)

def px(cases: float) -> float:
    """Convertit une longueur exprimée en cases en pixels."""
    return cases * TAILLE_CASE

def case_vers_pixel(case: Case) -> Tuple[float, float]:
    """Centre (en pixels) de la case (colonne, ligne).

    >>> case_vers_pixel((4, 6)) == (4.5 * TAILLE_CASE, 6.5 * TAILLE_CASE)
    True
    """
    colonne, ligne = case
    return px(colonne + 0.5), px(ligne + 0.5)
