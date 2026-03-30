import pygame

pygame.init()

# Constantes
TAILLE_CASE = 80
NB_CASES = 8
LARGEUR = TAILLE_CASE * NB_CASES
HAUTEUR = TAILLE_CASE * NB_CASES
RAYON = 30  # rayon du cercle du pion

# Couleurs
BEIGE = (240, 217, 181)
MARRON = (181, 136, 99)
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (150, 150, 150)

# Création de la fenêtre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu de Dames")


def dessiner_plateau(fenetre):
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


def dessiner_pion(fenetre, ligne, colonne, couleur):
    # Centre du cercle en pixels
    x = colonne * TAILLE_CASE + TAILLE_CASE // 2
    y = ligne * TAILLE_CASE + TAILLE_CASE // 2

    # On dessine d'abord un contour gris
    pygame.draw.circle(fenetre, GRIS, (x, y), RAYON + 3)

    # Puis le pion avec sa couleur
    pygame.draw.circle(fenetre, couleur, (x, y), RAYON)


def dessiner_pions_initiaux(fenetre):
    for ligne in range(NB_CASES):
        for colonne in range(NB_CASES):

            # Cases marron uniquement
            if (ligne + colonne) % 2 != 0:

                # Pions blancs sur les 3 premières lignes
                if ligne < 3:
                    dessiner_pion(fenetre, ligne, colonne, BLANC)

                # Pions noirs sur les 3 dernières lignes
                elif ligne > 4:
                    dessiner_pion(fenetre, ligne, colonne, NOIR)


# Boucle principale
en_cours = True
while en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

    dessiner_plateau(fenetre)
    dessiner_pions_initiaux(fenetre)
    pygame.display.flip()

pygame.quit()