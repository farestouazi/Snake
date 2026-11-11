"""Boucle de jeu et écran de fin de partie."""
from __future__ import annotations

import time
from typing import Tuple

import fltk

from . import textes
from .cartes import Carte
from .constantes import HAUTEUR_PLATEAU, LARGEUR_PLATEAU
from .dessin import dessiner_partie
from .partie import Partie
from .affichage import px
from .ui import Bouton, attendre_choix, ecrire

CX = LARGEUR_PLATEAU / 2
CY = HAUTEUR_PLATEAU / 2

def jouer_partie(nb_joueurs: int, carte: Carte, intervalle: float) -> bool:
    """Joue une partie. Retourne True pour rejouer, False pour quitter."""
    partie = Partie(carte, nb_joueurs, intervalle)

    while not partie.perdants():
        dessiner_partie(partie)

        evenement = fltk.donne_ev()
        type_evenement = fltk.type_ev(evenement)
        if type_evenement == "Quitte":
            return False
        if type_evenement == "Touche":
            partie.changer_directions(fltk.touche(evenement))

        partie.avancer()
        time.sleep(partie.intervalle)

    dessiner_partie(partie)
    return _ecran_fin(partie)

def _message_fin(partie: Partie) -> Tuple[str, str]:
    """Texte et couleur à afficher selon l'issue de la partie."""
    perdants = partie.perdants()
    if partie.nb_joueurs == 1:
        return textes.DEFAITE, "white"
    if len(perdants) == 2:
        return textes.EGALITE, "white"
    if perdants == [0]:
        return textes.JOUEUR_2_GAGNE, "orange"
    return textes.JOUEUR_1_GAGNE, "blue"

def _ecran_fin(partie: Partie) -> bool:
    """Affiche le résultat et propose de rejouer. Retourne True pour rejouer."""
    fltk.rectangle(px(CX - 7), px(CY - 7), px(CX + 7), px(CY + 7), "#FFFFFF", "#000000")
    message, couleur = _message_fin(partie)
    ecrire(CX, CY - 5.5, message, 30 / 36, couleur)

    choix = attendre_choix([
        (Bouton(CX - 4, CY - 4, CX + 4, CY, textes.REJOUER, 0.75), True),
        (Bouton(CX - 4, CY + 1, CX + 4, CY + 5, textes.QUITTER, 0.75), False),
    ])
    return bool(choix)
