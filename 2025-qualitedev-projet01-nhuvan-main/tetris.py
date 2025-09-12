#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
[Ce bloc est la documentation du module]
Un Tetris avec Pygame.
Ce code est basee sur le code de Sébastien CHAZALLET, auteur du livre "Python 3, les fondamentaux du language"
"""

__author__ = "guerrier titouan"
__copyright__ = "Copyright 2022"
__credits__ = ["Sébastien CHAZALLET", "Vincent NGUYEN", "guerrier titouan"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "guerrier titouan"
__email__ = "votre email"

# Probleme de l'ordre des imports
from pygame.locals import *
import constantes
import random
import time
import pygame
import sys


for name, rotations in constantes.PIECES.items():
    constantes.PIECES[name] = [[[int(i) for i in p] for p in r.splitlines()]
                    for r in rotations]

# Classe Tetris
class Jeu:

    def __init__(self):  #constructeur
        pygame.init()
        self.clock = pygame.time.Clock()  #horloge
        self.surface = pygame.display.set_mode(
            constantes.TAILLE_FENETRE)  #création de l'aire de jeu
        self.fonts = {
            'defaut': pygame.font.Font('freesansbold.ttf', 18),
            'titre': pygame.font.Font('freesansbold.ttf', 100),
        }
        pygame.display.set_caption('Application Tetris')

    #image d'accueil
    def start(self):
        ''''print("Démarrage du jeu")'''
        self.afficher_texte('Tetris', constantes.CENTRE_FENETRE, font='titre')
        self.afficher_texte('Appuyer sur une touche...', constantes.POS)
        self.attente()

    #image de game over
    def stop(self)->None:
        ''''print("Arrêt du jeu")'''
        self.afficher_texte('Perdu', constantes.CENTRE_FENETRE, font='titre')
        self.attente()
        self.quitter()

    def afficher_texte(self, text, position, couleur=9, font='defaut')->None:
        '''Affiche du texte à l'écran'''
        #		print("Afficher Texte")
        font = self.fonts.get(font, self.fonts['defaut'])
        couleur = constantes.COULEURS.get(couleur, constantes.COULEURS[9])
        rendu = font.render(text, True, couleur)
        rect = rendu.get_rect()
        rect.center = position
        self.surface.blit(rendu, rect)

    #rafraichi l'image
    def get_event(self)->int|None:
        '''Récupère les événements clavier et souris'''
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quitter()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.quitter()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continue
                return event.key

    def quitter(self)->None:
        '''Quitte le jeu proprement'''
        print("Quitter")
        pygame.quit()
        sys.exit()

    def rendre(self)->None:
        '''Rafraîchit l'écran'''
        pygame.display.update()
        self.clock.tick()

    def attente(self)->None:
        '''Attente d'une action de l'utilisateur'''
        print("Attente")
        while self.get_event() == None:
            self.rendre()

    def get_piece(self)->list:
        '''Retourne une pièce aléatoire'''
        return constantes.PIECES.get(random.choice(constantes.PIECES_KEYS))

    def get_current_piece_color(self)->int:
        '''Retourne la couleur de la pièce courante'''
        for l in self.current[0]:
            for c in l:
                if c != 0:
                    return c
        return 0

    #permet de bouger la pice en cours
    def calculer_donnees_piece_courante(self)->None:
        '''Calcule les coordonnées de la pièce courante'''
        m = self.current[self.position[2]]
        coords = []
        for i, l in enumerate(m):
            for j, k in enumerate(l):
                if k != 0:
                    coords.append([i + self.position[0], j + self.position[1]
                                   ])  # récupère les données
        self.coordonnees = coords

    def est_valide(self, x=0, y=0, r=0)->bool:
        '''Teste si la position est valide'''
        max_x, max_y = constantes.DIM_PLATEAU
        if r == 0:
            coordonnees = self.coordonnees
        else:
            m = self.current[(self.position[2] + r) % len(self.current)]
            coords = []
            for i, l in enumerate(m):
                for j, k in enumerate(l):
                    if k != 0:
                        coords.append(
                            [i + self.position[0], j + self.position[1]])
            coordonnees = coords
#			print("Rotation testée: %s" % coordonnees)
        for cx, cy in coordonnees:
            if not 0 <= x + cx < max_x:
                #				print("Non valide en X: cx=%s, x=%s" % (cx, x))
                return False
            elif cy < 0:
                continue
            elif y + cy >= max_y:
                #				print("Non valide en Y: cy=%s, y=%s" % (cy, y))
                return False
            else:
                if self.plateau[cy + y][cx + x] != 0:
                    #					print("Position occupée sur le plateau")
                    return False


#		print("Position testée valide: x=%s, y=%s" % (x, y))
        return True

    def poser_piece(self)->None:
        '''Pose la pièce courante sur le plateau'''
        print("La pièce est posée")
        if self.position[1] <= 0:
            self.perdu = True
        # Ajout de la pièce parmi le plateau
        couleur = self.get_current_piece_color()
        for cx, cy in self.coordonnees:
            self.plateau[cy][cx] = couleur
        completees = []
        # calculer les lignes complétées
        for i, line in enumerate(self.plateau[::-1]):
            for case in line:
                if case == 0:
                    break
            else:
                print(self.plateau)
                print(">>> %s" % (constantes.DIM_PLATEAU[1] - 1 - i))
                completees.append(constantes.DIM_PLATEAU[1] - 1 - i)
        lignes = len(completees)
        for i in completees:
            self.plateau.pop(i)
        for i in range(lignes):
            self.plateau.insert(0, [0] * constantes.DIM_PLATEAU[0])
        # calculer le score et autre
        self.lignes += lignes
        self.score += lignes * self.niveau
        self.niveau = int(self.lignes / 10) + 1
        if lignes >= 4:
            self.tetris += 1
            self.score += self.niveau * self.tetris
        # Travail avec la pièce courante terminé
        self.current = None

    def first(self)->None:
        '''Initialise une nouvelle partie'''
        self.plateau = [[0] * constantes.DIM_PLATEAU[0] for i in range(constantes.DIM_PLATEAU[1])]
        self.score, self.pieces, self.lignes, self.tetris, self.niveau = 0, 0, 0, 0, 1
        self.current, self.suivant, self.perdu = None, self.get_piece(), False

    def next(self)->None:
        '''Passe à la pièce suivante'''
        print("Piece suivante")
        self.current, self.suivant = self.suivant, self.get_piece()
        self.pieces += 1
        self.position = [int(constantes.DIM_PLATEAU[0] / 2) - 2, -4, 0]
        self.calculer_donnees_piece_courante()
        self.dernier_mouvement = self.derniere_chute = time.time()

    def gerer_evenements(self)->None:  #controleur
        '''Gère les événements clavier'''
        event = self.get_event()
        if event == K_p:
            print("Pause")
            self.surface.fill(constantes.COULEURS.get(0))
            self.afficher_texte('Pause', constantes.CENTRE_FENETRE, font='titre')
            self.afficher_texte('Appuyer sur une touche...', constantes.POS)
            self.attente()
        elif event == K_LEFT:
            print("Mouvement vers la gauche")
            if self.est_valide(x=-1):
                self.position[0] -= 1
        elif event == K_RIGHT:
            print("Mouvement vers la droite")
            if self.est_valide(x=1):
                self.position[0] += 1
        elif event == K_DOWN:
            print("Mouvement vers le bas")
            if self.est_valide(y=1):
                self.position[1] += 1
        elif event == K_UP:
            print("Mouvement de rotation")
            if self.est_valide(r=1):
                self.position[2] = (self.position[2] + 1) % len(self.current)
        elif event == K_SPACE:
            print("Mouvement de chute %s / %s" %
                  (self.position, self.coordonnees))
            if self.position[1] <= 0:
                self.position[1] = 1
                self.calculer_donnees_piece_courante()
            a = 0
            while self.est_valide(y=a):
                a += 1
            self.position[1] += a - 1
        self.calculer_donnees_piece_courante()

    def gerer_gravite(self)->None:  #permet de faire tomber la pièce
        '''Gère la gravité de la pièce courante'''
        if time.time() - self.derniere_chute > 0.35:
            self.derniere_chute = time .time()
            if not self.est_valide():
                print("On est dans une position invalide")
                self.position[1] -= 1
                self.calculer_donnees_piece_courante()
                self.poser_piece()
            elif self.est_valide() and not self.est_valide(y=1):
                self.calculer_donnees_piece_courante()
                self.poser_piece()
            else:
                print("On déplace vers le bas")
                self.position[1] += 1
                self.calculer_donnees_piece_courante()

    def dessiner_plateau(self)->None:
        '''Dessine le plateau de jeu'''
        self.surface.fill(constantes.COULEURS.get(0))
        pygame.draw.rect(self.surface, constantes.COULEURS[8],
                         constantes.START_PLABORD + constantes.TAILLE_PLABORD, constantes.BORDURE_PLATEAU)
        for i, ligne in enumerate(self.plateau):
            for j, case in enumerate(ligne):
                couleur = constantes.COULEURS[case]
                position = j, i
                coordonnees = tuple([
                    constantes.START_PLATEAU[k] + position[k] * constantes.TAILLE_BLOC[k]
                    for k in range(2)
                ])
                pygame.draw.rect(self.surface, couleur,
                                 coordonnees + constantes.TAILLE_BLOC)
        if self.current is not None:
            for position in self.coordonnees:
                couleur = constantes.COULEURS.get(self.get_current_piece_color())
                coordonnees = tuple([
                    constantes.START_PLATEAU[k] + position[k] * constantes.TAILLE_BLOC[k]
                    for k in range(2)
                ])
                pygame.draw.rect(self.surface, couleur,
                                 coordonnees + constantes.TAILLE_BLOC)
        self.score, self.pieces, self.lignes, self.tetris, self.niveau  #TODO
        self.afficher_texte('Score: >%s' % self.score, constantes.POSITION_SCORE)
        self.afficher_texte('Pièces: %s' % self.pieces, constantes.POSITION_PIECES)
        self.afficher_texte('Lignes: %s' % self.lignes, constantes.POSITION_LIGNES)
        self.afficher_texte('Tetris: %s' % self.tetris, constantes.POSITION_TETRIS)
        self.afficher_texte('Niveau: %s' % self.niveau, constantes.POSITION_NIVEAU)

        self.rendre()

    def play(self)->None:
        '''Lance une partie de Tetris'''
        print("Jouer")
        self.surface.fill(constantes.COULEURS.get(0))
        self.first()
        while not self.perdu:
            if self.current is None:
                self.next()
            self.gerer_evenements()
            self.gerer_gravite()
            self.dessiner_plateau()

if __name__ == '__main__':
    j = Jeu()
    print("Jeu prêt")
    j.start()
    print("Partie démarée")
    j.play()
    print("Partie terminée")
    j.stop()
    print("Arrêt du programme")
