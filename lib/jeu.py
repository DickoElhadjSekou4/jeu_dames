import pygame
import time
from lib.plateau import Plateau
from lib.ia import IA
from lib.sons import Sons

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
TAILLE_CASE = 80

class Jeu:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.plateau = Plateau()
        self.tour = BLANC
        self.partie_terminee = False
        self.gagnant = None
        self.ia = IA(BLANC)
        self.joueur_couleur = NOIR
        self.sons = Sons()

    def gerer_clic(self, pos):
        if self.tour == self.ia.couleur:
            return
        if self.partie_terminee:
            return

        colonne = pos[0] // TAILLE_CASE
        ligne = pos[1] // TAILLE_CASE

        pion_clique = self.plateau.obtenir_pion(ligne, colonne)

        if self.plateau.pion_selectionne:
            self.tenter_deplacement(ligne, colonne)
        elif pion_clique and pion_clique.couleur == self.tour:
            self.selectionner_pion(pion_clique)

    def jouer_ia(self):
        if self.partie_terminee:
            return
        if self.tour != self.ia.couleur:
            return

        time.sleep(0.5)

        resultat = self.ia.choisir_mouvement(self.plateau)

        if resultat:
            pion, mouvement = resultat
            self.plateau.deplacer_pion(pion, mouvement[0], mouvement[1])

            if mouvement[2] is not None:
                self.plateau.capturer_pion(mouvement[2], mouvement[3])
                self.sons.jouer_capture()
            else:
                self.sons.jouer_deplacement()

            self.verifier_fin_partie()

            if not self.partie_terminee:
                self.changer_tour()
        else:
            self.partie_terminee = True
            self.gagnant = "Noir"

    def selectionner_pion(self, pion):
        if self.plateau.pion_selectionne:
            self.plateau.pion_selectionne.est_selectionne = False

        pion.est_selectionne = True
        self.plateau.pion_selectionne = pion
        self.plateau.mouvements_possibles = self.plateau.calculer_mouvements(pion)

    def tenter_deplacement(self, ligne, colonne):
        pion = self.plateau.pion_selectionne
        mouvements = self.plateau.mouvements_possibles

        mouvement_valide = None
        for mouvement in mouvements:
            if mouvement[0] == ligne and mouvement[1] == colonne:
                mouvement_valide = mouvement
                break

        if mouvement_valide:
            self.plateau.deplacer_pion(pion, ligne, colonne)

            if mouvement_valide[2] is not None:
                self.plateau.capturer_pion(mouvement_valide[2], mouvement_valide[3])
                self.sons.jouer_capture()
            else:
                self.sons.jouer_deplacement()

            pion.est_selectionne = False
            self.plateau.pion_selectionne = None
            self.plateau.mouvements_possibles = []

            self.verifier_fin_partie()

            if not self.partie_terminee:
                self.changer_tour()
        else:
            pion.est_selectionne = False
            self.plateau.pion_selectionne = None
            self.plateau.mouvements_possibles = []

            nouveau_pion = self.plateau.obtenir_pion(ligne, colonne)
            if nouveau_pion and nouveau_pion.couleur == self.tour:
                self.selectionner_pion(nouveau_pion)

    def changer_tour(self):
        if self.tour == BLANC:
            self.tour = NOIR
        else:
            self.tour = BLANC

    def verifier_fin_partie(self):
        blancs = 0
        noirs = 0

        for pion in self.plateau.grille.values():
            if pion.couleur == BLANC:
                blancs += 1
            else:
                noirs += 1

        if blancs == 0:
            self.partie_terminee = True
            self.gagnant = "Noir"
            self.sons.jouer_victoire()
        elif noirs == 0:
            self.partie_terminee = True
            self.gagnant = "Blanc"
            self.sons.jouer_victoire()
    
    def dessiner(self):
        self.plateau.dessiner(self.fenetre)
        self.afficher_tour()
        self.afficher_instructions()

        if self.partie_terminee:
            self.afficher_gagnant()

    def afficher_instructions(self):
       font = pygame.font.SysFont("arial", 15)
       texte1 = font.render("R = Nouvelle partie", True, (255, 255, 255))
       texte2 = font.render("Echap = Quitter", True, (255, 255, 255))
       self.fenetre.blit(texte1, (10, 610))
       self.fenetre.blit(texte2, (10, 628))

    def afficher_tour(self):
        font = pygame.font.SysFont("arial", 20, bold=True)
        if self.tour == self.ia.couleur:
            texte = font.render("Tour : IA 🤖", True, (255, 255, 255))
        else:
            texte = font.render("Tour : Joueur ⚫", True, (255, 255, 255))
        self.fenetre.blit(texte, (10, 10))

    def afficher_gagnant(self):
        font = pygame.font.SysFont("arial", 60, bold=True)
        texte = font.render(
            f"{self.gagnant} a gagne !",
            True,
            (255, 215, 0)
        )
        rect = texte.get_rect(center=(320, 320))
        self.fenetre.blit(texte, rect)