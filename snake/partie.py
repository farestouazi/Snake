"""État et déroulement d'une partie (logique pure, testable sans écran)."""
from __future__ import annotations

from typing import List

from . import regles
from .cartes import Carte
from .constantes import (ACCELERATION_PAR_POMME, HAUT, LONGUEUR_INITIALE,
                         NOMBRE_POMMES, Case)

class Partie:
    """Une partie solo (``nb_joueurs=1``) ou à deux (``nb_joueurs=2``)."""

    def __init__(self, carte: Carte, nb_joueurs: int, intervalle: float) -> None:
        self.carte = carte
        self.nb_joueurs = nb_joueurs
        self.intervalle = intervalle  # secondes entre deux images
        self.serpents: List[List[Case]] = [list(s) for s in carte.serpents[:nb_joueurs]]
        self.directions: List[Case] = [HAUT] * nb_joueurs
        self.pommes: List[Case] = []
        for _ in range(NOMBRE_POMMES):
            self._ajouter_pomme()

    @property
    def murs(self):
        return self.carte.murs

    @property
    def scores(self) -> List[int]:
        return [len(serpent) - LONGUEUR_INITIALE for serpent in self.serpents]

    def changer_directions(self, touche: str) -> None:
        """Applique une touche pressée aux directions de chaque joueur."""
        for i, direction in enumerate(self.directions):
            self.directions[i] = regles.changer_direction(direction, touche, joueur=i + 1)

    def avancer(self) -> None:
        """Déplace les serpents, puis gère les pommes mangées."""
        for i, serpent in enumerate(self.serpents):
            self.serpents[i] = regles.deplacer_serpent(serpent, self.directions[i])
        self._manger_pommes()

    def perdants(self) -> List[int]:
        """Indices des serpents en collision (liste vide : la partie continue)."""
        perdants = []
        for i, serpent in enumerate(self.serpents):
            perdu = regles.collision_mur(serpent, self.murs) or regles.collision_corps(serpent)
            if self.nb_joueurs == 2:
                perdu = perdu or regles.collision_serpent(serpent, self.serpents[1 - i])
            if perdu:
                perdants.append(i)
        return perdants

    # --- Interne -----------------------------------------------------------
    def _cases_occupees(self):
        occupees = set(self.murs) | set(self.pommes)
        for serpent in self.serpents:
            occupees.update(serpent)
        return occupees

    def _ajouter_pomme(self) -> None:
        pomme = regles.poser_pomme(self._cases_occupees())
        if pomme is not None:
            self.pommes.append(pomme)

    def _manger_pommes(self) -> None:
        for serpent in self.serpents:
            if serpent[0] in self.pommes:
                self.pommes.remove(serpent[0])
                serpent.append(serpent[-1])  # le serpent grandit au prochain pas
                self._ajouter_pomme()
                self.intervalle *= ACCELERATION_PAR_POMME
