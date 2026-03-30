import pygame
from lib.jeu import Jeu

LARGEUR = 640
HAUTEUR = 660
FPS = 60

def main():
    pygame.init()

    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Jeu de Dames 🤖")

    clock = pygame.time.Clock()
    jeu = Jeu(fenetre)

    en_cours = True
    while en_cours:
        clock.tick(FPS)

        for event in pygame.event.get():
            # Croix de la fenêtre → quitter
            if event.type == pygame.QUIT:
                en_cours = False

            if event.type == pygame.KEYDOWN:
                # Touche Echap → quitter
                if event.key == pygame.K_ESCAPE:
                    en_cours = False

                # Touche R → recommencer
                if event.key == pygame.K_r:
                    jeu = Jeu(fenetre)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                jeu.gerer_clic(pos)

        if jeu.tour == jeu.ia.couleur and not jeu.partie_terminee:
            jeu.jouer_ia()

        jeu.dessiner()
        pygame.display.flip()

    pygame.quit()

main()