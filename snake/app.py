"""Point d'entrée : menus de démarrage puis parties successives."""
import fltk

from . import textes
from .affichage import HAUTEUR_FENETRE, LARGEUR_FENETRE
from .jeu import jouer_partie
from .menus import choisir_carte, choisir_difficulte, choisir_nb_joueurs

def main() -> None:
    fltk.cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)

    nb_joueurs = choisir_nb_joueurs()
    carte = choisir_carte() if nb_joueurs is not None else None
    intervalle = choisir_difficulte() if carte is not None else None

    if intervalle is not None:
        while jouer_partie(nb_joueurs, carte, intervalle):
            pass

    fltk.ferme_fenetre()
    print(textes.MERCI)
