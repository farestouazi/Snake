"""Dessin d'une image de la partie : bandeau des scores, pommes, serpents et murs."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Tuple

import fltk

from . import textes
from .affichage import LARGEUR_FENETRE, TAILLE_CASE, case_vers_pixel, px
from .constantes import HAUTEUR_PLATEAU, LARGEUR_PLATEAU, LIGNES_ENTETE
from .partie import Partie
from .ui import ecrire

COULEUR_BANDEAU = "black"
COULEUR_PLATEAU = "#121212"
COULEUR_MUR = "#ABABAB"

@dataclass(frozen=True)
class StyleJoueur:
    couleur: str
    couleur_corps: str
    x_titre: float
    x_score: float
    pave: Tuple[float, float]
    touches: Sequence[Tuple[str, float, float]]

STYLES = (
    StyleJoueur("blue", "darkblue", LARGEUR_PLATEAU / 2 + 2, LARGEUR_PLATEAU / 2 + 5, (2, 8),
                (("Left", 3, 2.5), ("Down", 5, 2.5), ("Right", 7, 2.5), ("Up", 5, 1.5))),
    StyleJoueur("orange", "purple", LARGEUR_PLATEAU / 2 + 10, LARGEUR_PLATEAU / 2 + 13, (10, 16),
                (("Q", 11, 2.5), ("S", 13, 2.5), ("D", 15, 2.5), ("Z", 13, 1.5))),
)

def _dessiner_fond() -> None:
    fltk.rectangle(0, 0, LARGEUR_FENETRE, px(LIGNES_ENTETE), COULEUR_BANDEAU, COULEUR_BANDEAU)
    fltk.rectangle(0, px(LIGNES_ENTETE), LARGEUR_FENETRE, px(LIGNES_ENTETE + HAUTEUR_PLATEAU),
                   COULEUR_BANDEAU, COULEUR_PLATEAU)

def _dessiner_bandeau(partie: Partie) -> None:
    for i, (style, score) in enumerate(zip(STYLES, partie.scores)):
        gauche, droite = style.pave
        ecrire(style.x_titre, 2, textes.SCORE.format(numero=i + 1), 0.75, style.couleur)
        ecrire(style.x_score, 2, str(score), 0.75, style.couleur)
        fltk.rectangle(px(gauche), px(2), px(droite), px(3), couleur=style.couleur)
        fltk.rectangle(px(gauche + 2), px(1), px(droite - 2), px(3), couleur=style.couleur)
        for libelle, x, y in style.touches:
            ecrire(x, y, libelle, 1 / 3, style.couleur)

def _dessiner_pommes(partie: Partie) -> None:
    for pomme in partie.pommes:
        x, y = case_vers_pixel(pomme)
        fltk.cercle(x, y, TAILLE_CASE / 2, couleur="darkred", remplissage="red")
        fltk.rectangle(x - 2, y - TAILLE_CASE * 0.4, x + 2, y - TAILLE_CASE * 0.7,
                       couleur="darkgreen", remplissage="darkgreen")

def _dessiner_serpents(partie: Partie) -> None:
    for serpent, style in zip(partie.serpents, STYLES):
        for rang, case in enumerate(serpent):
            x, y = case_vers_pixel(case)
            couleur = style.couleur if rang == 0 else style.couleur_corps
            fltk.cercle(x, y, TAILLE_CASE / 2 + 1, couleur=couleur, remplissage=couleur)

def _dessiner_murs(partie: Partie) -> None:
    demi = TAILLE_CASE / 2
    for mur in partie.murs:
        x, y = case_vers_pixel(mur)
        fltk.rectangle(x - demi, y - demi, x + demi, y + demi, COULEUR_MUR, COULEUR_MUR)

def dessiner_partie(partie: Partie) -> None:
    """Efface l'écran puis dessine l'état courant de la partie."""
    fltk.efface_tout()
    _dessiner_fond()
    _dessiner_bandeau(partie)
    _dessiner_pommes(partie)
    _dessiner_serpents(partie)
    _dessiner_murs(partie)
    fltk.mise_a_jour()
