import random

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

class IA:
    def __init__(self, couleur):
        self.couleur = couleur

    def choisir_mouvement(self, plateau):
        # Récupérer tous les pions de l'IA
        mes_pions = []
        for pion in plateau.grille.values():
            if pion.couleur == self.couleur:
                mes_pions.append(pion)

        # Chercher d'abord les captures possibles
        captures = []
        mouvements_simples = []

        for pion in mes_pions:
            mouvements = plateau.calculer_mouvements(pion)
            for mouvement in mouvements:
                # Si le mouvement capture un pion (case 2 et 3 != None)
                if mouvement[2] is not None:
                    captures.append((pion, mouvement))
                else:
                    mouvements_simples.append((pion, mouvement))

        # Priorité aux captures !
        if captures:
            return random.choice(captures)

        # Sinon mouvement simple aléatoire
        if mouvements_simples:
            return random.choice(mouvements_simples)

        # Aucun mouvement possible
        return None