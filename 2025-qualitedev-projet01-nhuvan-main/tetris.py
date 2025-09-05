#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
[Ce bloc est la documentation du module]
Un Tetris avec Pygame.
Ce code est basee sur le code de Sébastien CHAZALLET, auteur du livre "Python 3, les fondamentaux du language"
"""

__author__ = "votre nom"
__copyright__ = "Copyright 2022"
__credits__ = ["Sébastien CHAZALLET", "Vincent NGUYEN", "votre nom"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "votre nom"
__email__ = "votre email"

# Probleme de l'ordre des imports
from pygame.locals import *
import random
import time
import pygame
import sys


TAILLE_FENETRE = 640, 480
DIM_PLATEAU = 10, 20
BORDURE_PLATEAU = 4
TAILLE_BLOC = 20, 20

TAILLE_PLATEAU = tuple([DIM_PLATEAU[i]*TAILLE_BLOC[i] for i in range(2)])
TAILLE_PLABORD = tuple([DIM_PLATEAU[i]*TAILLE_BLOC[i]+BORDURE_PLATEAU*2 for i in range(2)])

MARGE = tuple([TAILLE_FENETRE[i]-TAILLE_PLATEAU[i]- BORDURE_PLATEAU*2 for i in range(2)])
START_PLATEAU = int(MARGE[0]/2), MARGE[1]+2*BORDURE_PLATEAU
START_PLABORD = int(MARGE[0]/2)-BORDURE_PLATEAU, MARGE[1]+BORDURE_PLATEAU

CENTRE_FENETRE = tuple([TAILLE_FENETRE[i]/2 for i in range(2)])
POS = CENTRE_FENETRE[0], CENTRE_FENETRE[1]+100
POSITION_SCORE = TAILLE_FENETRE[0] - START_PLABORD[0] / 2, 120
POSITION_PIECES = POSITION_SCORE[0], 150
POSITION_LIGNES = POSITION_SCORE[0], 180
POSITION_TETRIS = POSITION_SCORE[0], 210
POSITION_NIVEAU = POSITION_SCORE[0], 240

PIECES = {
	'O': [
		'0000\n0110\n0110\n0000',
	],
	'S': [
		'0000\n0022\n0220\n0000',
		'0000\n0200\n0220\n0020',
	],
	'Z': [
		'0000\n3300\n0330\n0000',
		'0000\n0030\n0330\n0300',
	],
	'I': [
		'0400\n0400\n0400\n0400',
		'0000\n4444\n0000\n0000',
	],
	'J': [
		'0000\n5000\n5550\n0000',
		'0000\n0550\n0500\n0500',
		'0000\n0000\n5550\n0050',
		'0000\n0050\n0050\n0550',
	],
	'L': [
		'0000\n0060\n6660\n0000',
		'0000\n0060\n0060\n0660',
		'0000\n0000\n6660\n6000',
		'0000\n0660\n0060\n0060',
	],
	'T': [
		'0000\n0700\n7770\n0000',
		'0000\n0700\n0770\n0700',
		'0000\n0000\n7770\n0700',
		'0000\n0070\n0770\n0070',
	]}

for name, rotations in PIECES.items():
	PIECES[name] = [[[int(i) for i in p] for p in r.splitlines()] for r in rotations]

COULEURS = {
	0: (0, 0, 0),
	1: (255, 255, 0),
	2: (0, 255, 0),
	3: (255, 0, 0),
	4: (0, 255, 255),
	5: (0, 0, 255),
	6: (255, 127, 0),
	7: (255, 0, 255),
	8: (127, 255, 0),
	9: (255, 255, 255),
}

PIECES_KEYS = list(PIECES.keys())

# Classe Tetris
class Jeu:
	"""
	[Il manque la documentation de la classe]
	"""
	def __init__(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.surface = pygame.display.set_mode(TAILLE_FENETRE)
		self.fonts = {
			'defaut': pygame.font.Font('freesansbold.ttf', 18),
			'titre': pygame.font.Font('freesansbold.ttf', 100),
		}
		pygame.display.set_caption('Application Tetris')

	def start(self):
		self._afficherTexte('Tetris', CENTRE_FENETRE, font = 'titre')
		self._afficherTexte('Appuyer sur une touche...', POS)
		self._attente()

	def stop(self):
		self._afficherTexte('Perdu', CENTRE_FENETRE, font='titre')
		self._attente()
		self._quitter()

	def _afficherTexte(self, text, position, couleur=9, font='defaut'):
#		print("Afficher Texte")
		font = self.fonts.get(font, self.fonts['defaut'])
		couleur=COULEURS.get(couleur, COULEURS[9])
		rendu = font.render(text, True, couleur)
		rect = rendu.get_rect()
		rect.center = position
		self.surface.blit(rendu, rect)
	def _getEvent(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self._quitter()
			if event.type == KEYUP:
				if event.key == K_ESCAPE:
					self._quitter()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					continue
				return event.key
				
	def _quitter(self):
		print("Quitter")
		pygame.quit()
		sys.exit()
	def _rendre(self):
		pygame.display.update()
		self.clock.tick()
	def _attente(self):
		print("Attente")
		while self._getEvent() == None:
			self._rendre()
	def _getPiece(self):
		return PIECES.get(random.choice(PIECES_KEYS))
	def _getCurrentPieceColor(self):
		for l in self.current[0]:
			for c in l:
				if c != 0:
					return c
		return 0
	def _calculerDonneesPieceCourante(self):
		m=self.current[self.position[2]]
		coords = []
		for i, l in enumerate(m):
			for j, k in enumerate(l):
				if k != 0:
					coords.append([i+self.position[0], j+self.position[1]])
		self.coordonnees = coords
	def _estValide(self, x=0, y=0, r=0):
		max_x, max_y = DIM_PLATEAU
		if r == 0:
			coordonnees = self.coordonnees
		else:
			m=self.current[(self.position[2]+r)%len(self.current)]
			coords = []
			for i, l in enumerate(m):
				for j, k in enumerate(l):
					if k != 0:
						coords.append([i+self.position[0], j+self.position[1]])
			coordonnees = coords
#			print("Rotation testée: %s" % coordonnees)
		for cx, cy in coordonnees:
			if not 0 <= x + cx < max_x:
#				print("Non valide en X: cx=%s, x=%s" % (cx, x))
				return False
			elif cy <0:
				continue
			elif y + cy >= max_y:
#				print("Non valide en Y: cy=%s, y=%s" % (cy, y))
				return False
			else:
				if self.plateau[cy+y][cx+x] != 0:
#					print("Position occupée sur le plateau")
					return False
#		print("Position testée valide: x=%s, y=%s" % (x, y))
		return True
	def _poserPiece(self):
		print("La pièce est posée")
		if self.position[1] <= 0:
			self.perdu = True
		# Ajout de la pièce parmi le plateau
		couleur = self._getCurrentPieceColor()
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
				print(">>> %s" % (DIM_PLATEAU[1]-1-i))
				completees.append(DIM_PLATEAU[1]-1-i)
		lignes = len(completees)
		for i in completees:
			self.plateau.pop(i)
		for i in range(lignes):
			self.plateau.insert(0, [0] * DIM_PLATEAU[0])
		# calculer le score et autre
		self.lignes += lignes
		self.score += lignes * self.niveau
		self.niveau = int(self.lignes / 10) + 1
		if lignes >= 4:
			self.tetris +=1
			self.score += self.niveau * self.tetris
		# Travail avec la pièce courante terminé
		self.current = None
	def _first(self):
		self.plateau = [[0] * DIM_PLATEAU[0] for i in range(DIM_PLATEAU[1])]
		self.score, self.pieces, self.lignes, self.tetris, self.niveau = 0, 0, 0, 0, 1
		self.current, self.next, self.perdu = None, self._getPiece(), False
	def _next(self):
		print("Piece suivante")
		self.current, self.next = self.next, self._getPiece()
		self.pieces += 1
		self.position = [int(DIM_PLATEAU[0] / 2)-2, -4, 0]
		self._calculerDonneesPieceCourante()
		self.dernier_mouvement = self.derniere_chute = time.time()
	def _gererEvenements(self):
		event = self._getEvent()
		if event == K_p:
			print("Pause")
			self.surface.fill(COULEURS.get(0))
			self._afficherTexte('Pause', CENTRE_FENETRE, font='titre')
			self._afficherTexte('Appuyer sur une touche...', POS)
			self._attente()
		elif event == K_LEFT:
			print("Mouvement vers la gauche")
			if self._estValide(x=-1):
				self.position[0] -= 1
		elif event == K_RIGHT:
			print("Mouvement vers la droite")
			if self._estValide(x=1):
				self.position[0] += 1
		elif event == K_DOWN:
			print("Mouvement vers le bas")
			if self._estValide(y=1):
				self.position[1] += 1
		elif event == K_UP:
			print("Mouvement de rotation")
			if self._estValide(r=1):
				self.position[2] = (self.position[2] + 1) %len(self.current)
		elif event == K_SPACE:
			print("Mouvement de chute %s / %s" % (self.position, self.coordonnees))
			if self.position[1] <=0:
				self.position[1] = 1
				self._calculerDonneesPieceCourante()
			a = 0
			while self._estValide(y=a):
				a+=1
			self.position[1] += a-1
		self._calculerDonneesPieceCourante()
	def _gererGravite(self):
		if time.time() - self.derniere_chute > 0.35:
			self.derniere_chute = time.time()
			if not self._estValide():
				print ("On est dans une position invalide")
				self.position[1] -= 1
				self._calculerDonneesPieceCourante()
				self._poserPiece()
			elif self._estValide() and not self._estValide(y=1):
				self._calculerDonneesPieceCourante()
				self._poserPiece()
			else:
				print("On déplace vers le bas")
				self.position[1] += 1
				self._calculerDonneesPieceCourante()
	def _dessinerPlateau(self):
		self.surface.fill(COULEURS.get(0))
		pygame.draw.rect(self.surface, COULEURS[8], START_PLABORD+TAILLE_PLABORD, BORDURE_PLATEAU)
		for i, ligne in enumerate(self.plateau):
			for j, case in enumerate(ligne):
				couleur = COULEURS[case]
				position = j, i
				coordonnees = tuple([START_PLATEAU[k] + position[k] * TAILLE_BLOC[k] for k in range(2)])
				pygame.draw.rect(self.surface, couleur, coordonnees + TAILLE_BLOC)
		if self.current is not None:
			for position in self.coordonnees:
				couleur = COULEURS.get(self._getCurrentPieceColor())
				coordonnees = tuple([START_PLATEAU[k] + position[k] * TAILLE_BLOC[k] for k in range(2)])
				pygame.draw.rect(self.surface, couleur, coordonnees + TAILLE_BLOC)
		self.score, self.pieces, self.lignes, self.tetris, self.niveau#TODO
		self._afficherTexte('Score: >%s' % self.score, POSITION_SCORE)
		self._afficherTexte('Pièces: %s' % self.pieces, POSITION_PIECES)
		self._afficherTexte('Lignes: %s' % self.lignes, POSITION_LIGNES)
		self._afficherTexte('Tetris: %s' % self.tetris, POSITION_TETRIS)
		self._afficherTexte('Niveau: %s' % self.niveau, POSITION_NIVEAU)

		self._rendre()
	def play(self):
		print("Jouer")
		self.surface.fill(COULEURS.get(0))
		self._first()
		while not self.perdu:
			if self.current is None:
				self._next()
			self._gererEvenements()
			self._gererGravite()
			self._dessinerPlateau()

if __name__ == '__main__':
	j = Jeu()
	print("Jeu prêt")
	j.start()
	print("Partie démarée")
	j.play()
	print("Partie terminée")
	j.stop()
	print("Arrêt du programme")

