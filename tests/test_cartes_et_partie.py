import unittest

from snake.cartes import CARTES, lire_carte
from snake.constantes import (HAUT, HAUTEUR_PLATEAU, LARGEUR_PLATEAU, LIGNE_MAX, LIGNE_MIN,
                              LONGUEUR_INITIALE, NOMBRE_POMMES)
from snake.partie import Partie

class TestCartes(unittest.TestCase):
    def test_trois_cartes(self):
        self.assertEqual([c.nom for c in CARTES], ["Map 1", "Map 2", "Map 3"])

    def test_murs_dans_le_plateau(self):
        for carte in CARTES:
            for colonne, ligne in carte.murs:
                self.assertTrue(0 <= colonne < LARGEUR_PLATEAU)
                self.assertTrue(LIGNE_MIN <= ligne <= LIGNE_MAX)

    def test_la_carte_1_a_des_murs_en_haut_et_en_bas_et_des_passages_sur_les_cotes(self):
        murs = CARTES[0].murs
        for colonne in range(LARGEUR_PLATEAU):
            self.assertIn((colonne, LIGNE_MIN), murs)
            self.assertIn((colonne, LIGNE_MAX), murs)
        for ligne in range(LIGNE_MIN + 1, 29):
            self.assertIn((0, ligne), murs)
            self.assertIn((LARGEUR_PLATEAU - 1, ligne), murs)
        for ligne in range(29, LIGNE_MAX):  # ouvertures latérales
            self.assertNotIn((0, ligne), murs)
            self.assertNotIn((LARGEUR_PLATEAU - 1, ligne), murs)

    def test_serpents_de_depart_valides(self):
        for carte in CARTES:
            self.assertEqual(len(carte.serpents), 2)
            for serpent in carte.serpents:
                self.assertEqual(len(serpent), LONGUEUR_INITIALE)
                self.assertFalse(set(serpent) & carte.murs)
                # tête en haut, corps en dessous (le serpent démarre vers le haut)
                for (c1, l1), (c2, l2) in zip(serpent, serpent[1:]):
                    self.assertEqual((c2, l2), (c1, l1 + 1))

    def test_dessin_de_mauvaise_taille_refuse(self):
        with self.assertRaises(ValueError):
            lire_carte("x", ["#" * LARGEUR_PLATEAU] * (HAUTEUR_PLATEAU - 1), [])

class TestPartie(unittest.TestCase):
    def setUp(self):
        self.carte = CARTES[0]

    def test_depart_solo(self):
        partie = Partie(self.carte, 1, 0.1)
        self.assertEqual(len(partie.serpents), 1)
        self.assertEqual(partie.scores, [0])
        self.assertEqual(len(partie.pommes), NOMBRE_POMMES)
        self.assertEqual(len(set(partie.pommes)), NOMBRE_POMMES)
        self.assertFalse(partie.perdants())

    def test_depart_deux_joueurs(self):
        partie = Partie(self.carte, 2, 0.1)
        self.assertEqual(len(partie.serpents), 2)
        self.assertEqual(partie.scores, [0, 0])

    def test_les_pommes_ne_sont_pas_sur_les_murs_ni_les_serpents(self):
        for _ in range(30):
            partie = Partie(self.carte, 2, 0.1)
            for pomme in partie.pommes:
                self.assertNotIn(pomme, self.carte.murs)
                self.assertFalse(any(pomme in s for s in partie.serpents))

    def test_manger_une_pomme(self):
        partie = Partie(self.carte, 1, 0.1)
        tete = partie.serpents[0][0]
        partie.pommes = [(tete[0], tete[1] - 1)]  # juste devant la tête
        partie.avancer()
        self.assertEqual(partie.scores, [1])
        self.assertEqual(len(partie.serpents[0]), LONGUEUR_INITIALE + 1)
        self.assertEqual(len(partie.pommes), 1)   # remplacée par une nouvelle pomme
        self.assertLess(partie.intervalle, 0.1)   # le jeu accélère
        partie.avancer()
        self.assertEqual(partie.scores, [1])      # la longueur ne change plus sans pomme

    def test_les_deux_serpents_peuvent_manger_dans_la_meme_image(self):
        partie = Partie(self.carte, 2, 0.1)
        devant = [(s[0][0], s[0][1] - 1) for s in partie.serpents]
        partie.pommes = list(devant)
        partie.avancer()
        self.assertEqual([len(s) for s in partie.serpents], [LONGUEUR_INITIALE + 1] * 2)

    def test_collision_avec_un_mur(self):
        partie = Partie(self.carte, 1, 0.1)
        for _ in range(60):
            partie.avancer()
            if partie.perdants():
                break
        self.assertEqual(partie.perdants(), [0])

    def test_collision_avec_l_autre_serpent(self):
        partie = Partie(self.carte, 2, 0.1)
        partie.serpents = [[(10, 10), (10, 11)], [(11, 10), (10, 9), (10, 10)]]
        # la tête du serpent 0 est sur le corps du serpent 1
        self.assertEqual(partie.perdants(), [0])

    def test_egalite_quand_les_deux_perdent(self):
        partie = Partie(self.carte, 2, 0.1)
        mur = next(iter(self.carte.murs))
        partie.serpents = [[mur, (mur[0], mur[1] + 1)], [mur, (mur[0] + 1, mur[1])]]
        self.assertEqual(partie.perdants(), [0, 1])

    def test_les_touches_changent_les_directions(self):
        partie = Partie(self.carte, 2, 0.1)
        partie.changer_directions("Right")
        partie.changer_directions("a")
        self.assertEqual(partie.directions, [(1, 0), (-1, 0)])

    def test_en_solo_les_touches_du_joueur_2_sont_ignorees(self):
        partie = Partie(self.carte, 1, 0.1)
        partie.changer_directions("d")
        self.assertEqual(partie.directions, [HAUT])

if __name__ == "__main__":
    unittest.main()
