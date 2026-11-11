"""Menus de démarrage : mode de jeu, carte et difficulté."""
from __future__ import annotations

from typing import Optional

import fltk

from . import textes
from .cartes import CARTES, Carte
from .constantes import HAUTEUR_PLATEAU, INTERVALLES, LARGEUR_PLATEAU
from .ui import Bouton, attendre_choix, dessiner_fond_menu, ecrire

CX = LARGEUR_PLATEAU / 2
CY = HAUTEUR_PLATEAU / 2

def _bouton(x1: float, y1: float, x2: float, y2: float, libelle: str) -> Bouton:
    """Bouton défini par rapport au centre (CX, CY)."""
    return Bouton(CX + x1, CY + y1, CX + x2, CY + y2, libelle)

def _rangee_de_trois(y1: float, y2: float, libelles) -> list:
    colonnes = ((-16, -8), (-4, 4), (8, 16))
    return [_bouton(x1, y1, x2, y2, libelle) for (x1, x2), libelle in zip(colonnes, libelles)]

def choisir_nb_joueurs() -> Optional[int]:
    """Retourne 1 (solo) ou 2 (multijoueur)."""
    fltk.efface_tout()
    dessiner_fond_menu()
    ecrire(CX, CY - 8, textes.TITRE, 1.7, "lightgreen")
    ecrire(CX, CY - 5, textes.JOUER, 1.4)
    return attendre_choix([
        (_bouton(-12, -2, -2, 2, textes.SOLO), 1),
        (_bouton(2, -2, 12, 2, textes.MULTIJOUEUR), 2),
    ])

def choisir_carte() -> Optional[Carte]:
    fltk.efface_tout()
    dessiner_fond_menu()
    ecrire(CX, CY - 8, textes.CARTE, 1.5)
    boutons = _rangee_de_trois(8, 12, [carte.nom for carte in CARTES])
    return attendre_choix(list(zip(boutons, CARTES)))

def choisir_difficulte() -> Optional[float]:
    """Retourne l'intervalle (en secondes) entre deux images."""
    fltk.efface_tout()
    dessiner_fond_menu()
    ecrire(CX, CY - 8, textes.DIFFICULTE, 1.5)
    boutons = _rangee_de_trois(5, 9, [textes.FACILE, textes.MOYEN, textes.DIFFICILE])
    return attendre_choix(list(zip(boutons, INTERVALLES)))
