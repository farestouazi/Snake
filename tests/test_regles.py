import unittest

from snake import regles
from snake.constantes import BAS, DROITE, GAUCHE, HAUT, LARGEUR_PLATEAU, LIGNE_MAX, LIGNE_MIN

class TestDirection(unittest.TestCase):
    def test_changement_de_direction_joueur_1(self):
        self.assertEqual(regles.changer_direction(HAUT, "Right", 1), DROITE)
        self.assertEqual(regles.changer_direction(DROITE, "Down", 1), BAS)

    def test_demi_tour_interdit(self):
        self.assertEqual(regles.changer_direction(HAUT, "Down", 1), HAUT)
        self.assertEqual(regles.changer_direction(GAUCHE, "Right", 1), GAUCHE)

    def test_touche_inconnue_ou_absente(self):
        self.assertEqual(regles.changer_direction(HAUT, "x", 1), HAUT)
        self.assertEqual(regles.changer_direction(HAUT, None, 2), HAUT)

    def test_joueur_2_accepte_zqsd_et_wasd(self):
        for touche in ("z", "w"):
            self.assertEqual(regles.changer_direction(DROITE, touche, 2), HAUT)
        for touche in ("q", "a"):
            self.assertEqual(regles.changer_direction(HAUT, touche, 2), GAUCHE)
        self.assertEqual(regles.changer_direction(DROITE, "s", 2), BAS)

    def test_les_touches_d_un_joueur_n_agissent_pas_sur_l_autre(self):
        self.assertEqual(regles.changer_direction(HAUT, "Right", 2), HAUT)
        self.assertEqual(regles.changer_direction(HAUT, "d", 1), HAUT)

class TestDeplacement(unittest.TestCase):
    def test_avance_et_conserve_la_longueur(self):
        serpent = [(5, 10), (5, 11), (5, 12)]
        self.assertEqual(regles.deplacer_serpent(serpent, HAUT), [(5, 9), (5, 10), (5, 11)])
        self.assertEqual(serpent, [(5, 10), (5, 11), (5, 12)])  # non modifié

    def test_traverse_les_bords_horizontaux(self):
        self.assertEqual(regles.deplacer_serpent([(LARGEUR_PLATEAU - 1, 10)], DROITE), [(0, 10)])
        self.assertEqual(regles.deplacer_serpent([(0, 10)], GAUCHE), [(LARGEUR_PLATEAU - 1, 10)])

    def test_traverse_le_bord_superieur(self):
        self.assertEqual(regles.deplacer_serpent([(7, LIGNE_MIN)], HAUT), [(7, LIGNE_MAX)])

    def test_traverse_le_bord_inferieur(self):
        # Régression : le serpent réapparaissait dans le bandeau des scores (ligne 0).
        self.assertEqual(regles.deplacer_serpent([(7, LIGNE_MAX)], BAS), [(7, LIGNE_MIN)])

class TestCollisions(unittest.TestCase):
    def test_collision_mur(self):
        self.assertTrue(regles.collision_mur([(3, 3), (3, 4)], {(3, 3)}))
        self.assertFalse(regles.collision_mur([(3, 3), (3, 4)], {(3, 4)}))

    def test_collision_corps(self):
        self.assertTrue(regles.collision_corps([(1, 1), (2, 1), (1, 1)]))
        self.assertFalse(regles.collision_corps([(1, 1), (2, 1), (3, 1)]))

    def test_collision_avec_l_autre_serpent_ignore_sa_tete(self):
        autre = [(5, 5), (5, 6), (5, 7)]
        self.assertTrue(regles.collision_serpent([(5, 6)], autre))
        self.assertFalse(regles.collision_serpent([(5, 5)], autre))

class TestPommes(unittest.TestCase):
    def test_pomme_toujours_sur_une_case_libre_du_plateau(self):
        occupees = {(x, y) for x in range(1, 20) for y in range(LIGNE_MIN + 1, LIGNE_MAX + 1)}
        for _ in range(200):
            colonne, ligne = regles.poser_pomme(occupees)
            self.assertNotIn((colonne, ligne), occupees)
            self.assertTrue(1 <= colonne <= LARGEUR_PLATEAU - 2)
            self.assertTrue(LIGNE_MIN + 1 <= ligne <= LIGNE_MAX)

    def test_aucune_case_libre(self):
        occupees = {(x, y) for x in range(LARGEUR_PLATEAU) for y in range(LIGNE_MAX + 1)}
        self.assertIsNone(regles.poser_pomme(occupees))

if __name__ == "__main__":
    unittest.main()
