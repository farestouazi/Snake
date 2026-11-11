"""Briques d'interface : texte, boutons et attente d'un choix.

Toutes les coordonnées et tailles sont exprimées en *cases* ; ``px`` les convertit.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence, Tuple

import fltk

from .affichage import LARGEUR_FENETRE, px
from .constantes import HAUTEUR_PLATEAU, LIGNES_ENTETE

COULEUR_FOND_MENU = "#151515"

def ecrire(x: float, y: float, texte: str, taille: float, couleur: str = "white"):
    """Écrit un texte centré en (x, y)."""
    return fltk.texte(px(x), px(y), texte, couleur=couleur, ancrage="center", taille=int(px(taille)))


def dessiner_fond_menu() -> None:
    fltk.rectangle(0, 0, LARGEUR_FENETRE, px(LIGNES_ENTETE + HAUTEUR_PLATEAU),
                   COULEUR_FOND_MENU, COULEUR_FOND_MENU)

@dataclass(frozen=True)
class Bouton:
    x1: float
    y1: float
    x2: float
    y2: float
    libelle: str
    taille_texte: float = 1.1

    def dessiner(self) -> None:
        fltk.rectangle(px(self.x1), px(self.y1), px(self.x2), px(self.y2), "#FFFFFF", "#000000")
        ecrire((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2, self.libelle, self.taille_texte)

    def contient(self, x: float, y: float) -> bool:
        """``x`` et ``y`` sont en pixels."""
        return px(self.x1) < x < px(self.x2) and px(self.y1) < y < px(self.y2)

def attendre_choix(choix: Sequence[Tuple[Bouton, Any]]) -> Any:
    """Dessine les boutons puis attend un clic sur l'un d'eux.

    Retourne la valeur associée au bouton cliqué, ou ``None`` si la fenêtre est fermée.
    """
    for bouton, _ in choix:
        bouton.dessiner()
    while True:
        evenement = fltk.attend_ev()
        type_evenement = fltk.type_ev(evenement)
        if type_evenement == "Quitte":
            return None
        if type_evenement == "ClicGauche":
            x, y = fltk.abscisse_souris(), fltk.ordonnee_souris()
            for bouton, valeur in choix:
                if bouton.contient(x, y):
                    return valeur
