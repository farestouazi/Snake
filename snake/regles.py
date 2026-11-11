"""Règles du jeu : fonctions pures, sans dépendance à l'interface."""
from __future__ import annotations

import random
from typing import Collection, List, Optional

from .constantes import (COMMANDES, LARGEUR_PLATEAU, LIGNE_MAX, LIGNE_MIN, Case)

def direction_opposee(direction: Case) -> Case:
    return -direction[0], -direction[1]

def changer_direction(direction: Case, touche: Optional[str], joueur: int) -> Case:
    """Nouvelle direction après l'appui sur ``touche`` (demi-tour interdit)."""
    nouvelle = COMMANDES[joueur].get(touche)
    if nouvelle is None or nouvelle == direction_opposee(direction):
        return direction
    return nouvelle

def deplacer_serpent(serpent: List[Case], direction: Case) -> List[Case]:
    """Avance le serpent d'une case ; il réapparaît de l'autre côté s'il sort du plateau.

    :param serpent: positions du corps, la tête en premier
    :return: nouvelle liste (l'originale n'est pas modifiée)
    """
    colonne = (serpent[0][0] + direction[0]) % LARGEUR_PLATEAU
    ligne = serpent[0][1] + direction[1]
    if ligne > LIGNE_MAX:
        ligne = LIGNE_MIN
    elif ligne < LIGNE_MIN:
        ligne = LIGNE_MAX
    return [(colonne, ligne)] + serpent[:-1]

def collision_mur(serpent: List[Case], murs: Collection[Case]) -> bool:
    return serpent[0] in murs

def collision_corps(serpent: List[Case]) -> bool:
    """La tête touche son propre corps."""
    return serpent[0] in serpent[1:]

def collision_serpent(serpent: List[Case], autre: List[Case]) -> bool:
    """La tête touche le corps de l'autre serpent (sa tête n'est pas comptée)."""
    return serpent[0] in autre[1:]

def poser_pomme(occupees: Collection[Case]) -> Optional[Case]:
    """Choisit au hasard une case libre pour une pomme (``None`` s'il n'y en a plus).

    Les pommes n'apparaissent pas sur la première ni sur la dernière colonne,
    ni sur la première ligne du plateau.
    """
    libres = [
        (colonne, ligne)
        for colonne in range(1, LARGEUR_PLATEAU - 1)
        for ligne in range(LIGNE_MIN + 1, LIGNE_MAX + 1)
        if (colonne, ligne) not in occupees
    ]
    return random.choice(libres) if libres else None
