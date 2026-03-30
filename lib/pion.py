import pygame

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (150, 150, 150)
OR = (255, 215, 0)

TAILLE_CASE = 80
RAYON = 30

class Pion:
    def __init__(self, ligne, colonne, couleur):
        self.ligne = ligne
        self.colonne = colonne
        self.couleur = couleur
        self.est_dame = False
        self.est_selectionne = False

    def deplacer(self, ligne, colonne):
        self.ligne = ligne
        self.colonne = colonne

    def devenir_dame(self):
        self.est_dame = True

    def dessiner(self, fenetre):
        # Centre du pion en pixels
        x = self.colonne * TAILLE_CASE + TAILLE_CASE // 2
        y = self.ligne * TAILLE_CASE + TAILLE_CASE // 2

        # Contour gris
        pygame.draw.circle(fenetre, GRIS, (x, y), RAYON + 3)

        # Corps du pion
        pygame.draw.circle(fenetre, self.couleur, (x, y), RAYON)

        # Si sélectionné → contour doré
        if self.est_selectionne:
            pygame.draw.circle(fenetre, OR, (x, y), RAYON + 3, 4)

        # Si dame → couronne dorée au centre
        if self.est_dame:
            pygame.draw.circle(fenetre, OR, (x, y), RAYON // 2)