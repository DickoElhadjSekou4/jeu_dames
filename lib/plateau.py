import pygame
from lib.pion import Pion

# Couleurs
BEIGE = (240, 217, 181)
MARRON = (181, 136, 99)
VERT = (0, 255, 0)
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

TAILLE_CASE = 80
NB_CASES = 8

class Plateau:
    def __init__(self):
        self.grille = {}
        self.pion_selectionne = None
        self.mouvements_possibles = []
        self.creer_pions()

    def creer_pions(self):
        for ligne in range(NB_CASES):
            for colonne in range(NB_CASES):
                if (ligne + colonne) % 2 != 0:
                    if ligne < 3:
                        self.grille[(ligne, colonne)] = Pion(ligne, colonne, BLANC)
                    elif ligne > 4:
                        self.grille[(ligne, colonne)] = Pion(ligne, colonne, NOIR)

    def obtenir_pion(self, ligne, colonne):
        return self.grille.get((ligne, colonne), None)

    def deplacer_pion(self, pion, ligne, colonne):
        # On supprime l'ancienne position
        del self.grille[(pion.ligne, pion.colonne)]

        # On déplace le pion
        pion.deplacer(ligne, colonne)

        # On met à jour la grille
        self.grille[(ligne, colonne)] = pion

        # Vérifier si le pion devient dame
        if pion.couleur == BLANC and ligne == NB_CASES - 1:
            pion.devenir_dame()
        elif pion.couleur == NOIR and ligne == 0:
            pion.devenir_dame()

    def capturer_pion(self, ligne, colonne):
        if (ligne, colonne) in self.grille:
            del self.grille[(ligne, colonne)]

    def calculer_mouvements(self, pion):
        mouvements = []

        if pion.couleur == BLANC:
            directions = [1]
        else:
            directions = [-1]

        if pion.est_dame:
            directions = [1, -1]

        for direction in directions:
            for delta_col in [-1, 1]:
                nouvelle_ligne = pion.ligne + direction
                nouvelle_col = pion.colonne + delta_col

                if 0 <= nouvelle_ligne < NB_CASES and 0 <= nouvelle_col < NB_CASES:
                    # Case vide → mouvement simple
                    if self.obtenir_pion(nouvelle_ligne, nouvelle_col) is None:
                        mouvements.append((nouvelle_ligne, nouvelle_col, None, None))
                    else:
                        # Case occupée → vérifier si on peut capturer
                        pion_adverse = self.obtenir_pion(nouvelle_ligne, nouvelle_col)
                        if pion_adverse.couleur != pion.couleur:
                            saut_ligne = nouvelle_ligne + direction
                            saut_col = nouvelle_col + delta_col
                            if 0 <= saut_ligne < NB_CASES and 0 <= saut_col < NB_CASES:
                                if self.obtenir_pion(saut_ligne, saut_col) is None:
                                    mouvements.append((saut_ligne, saut_col, nouvelle_ligne, nouvelle_col))

        return mouvements

    def dessiner(self, fenetre):
        # Dessiner les cases
        for ligne in range(NB_CASES):
            for colonne in range(NB_CASES):
                if (ligne + colonne) % 2 == 0:
                    couleur = BEIGE
                else:
                    couleur = MARRON
                pygame.draw.rect(
                    fenetre,
                    couleur,
                    (colonne * TAILLE_CASE, ligne * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
                )

        # Dessiner les mouvements possibles
        for mouvement in self.mouvements_possibles:
            ligne, colonne = mouvement[0], mouvement[1]
            pygame.draw.rect(
                fenetre,
                VERT,
                (colonne * TAILLE_CASE, ligne * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE),
                4
            )

        # Dessiner les pions
        for pion in self.grille.values():
            pion.dessiner(fenetre)