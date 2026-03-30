import pygame
import numpy as np

# Paramètres audio
FREQUENCE = 44100  # qualité du son (Hz)
DUREE_COURTE = 0.1  # secondes
DUREE_LONGUE = 0.6  # secondes

class Sons:
    def __init__(self):
        pygame.mixer.init(frequency=FREQUENCE)
        self.son_deplacement = self.generer_son(440, DUREE_COURTE)   # La (440Hz)
        self.son_capture = self.generer_son(200, DUREE_COURTE)        # Son grave
        self.son_victoire = self.generer_fanfare()                     # Mélodie !

    def generer_son(self, frequence, duree):
        # Nombre d'échantillons
        nb_echantillons = int(FREQUENCE * duree)

        # Générer une onde sinusoïdale
        t = np.linspace(0, duree, nb_echantillons)
        onde = np.sin(2 * np.pi * frequence * t)

        # Ajouter un fondu pour éviter les clics
        fondu = np.linspace(1, 0, nb_echantillons)
        onde = onde * fondu

        # Convertir en format pygame (16 bits)
        onde_int = (onde * 32767).astype(np.int16)

        # Créer un son stéréo
        stereo = np.column_stack([onde_int, onde_int])
        son = pygame.sndarray.make_sound(stereo)
        return son

    def generer_fanfare(self):
        # Une petite mélodie de victoire !
        notes = [523, 659, 784, 1047]  # Do Mi Sol Do
        duree_note = 0.15
        nb_total = int(FREQUENCE * duree_note * len(notes))
        onde_totale = np.zeros(nb_total)

        for i, freq in enumerate(notes):
            nb_echantillons = int(FREQUENCE * duree_note)
            t = np.linspace(0, duree_note, nb_echantillons)
            onde = np.sin(2 * np.pi * freq * t)
            fondu = np.linspace(1, 0, nb_echantillons)
            onde = onde * fondu
            debut = i * nb_echantillons
            onde_totale[debut:debut + nb_echantillons] = onde

        onde_int = (onde_totale * 32767).astype(np.int16)
        stereo = np.column_stack([onde_int, onde_int])
        son = pygame.sndarray.make_sound(stereo)
        return son

    def jouer_deplacement(self):
        self.son_deplacement.play()

    def jouer_capture(self):
        self.son_capture.play()

    def jouer_victoire(self):
        self.son_victoire.play()