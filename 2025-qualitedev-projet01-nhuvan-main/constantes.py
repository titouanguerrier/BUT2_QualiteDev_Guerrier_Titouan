#les dimensions de l'aire de jeu
TAILLE_FENETRE = 640, 480
DIM_PLATEAU = 10, 20
BORDURE_PLATEAU = 4
TAILLE_BLOC = 20, 20

TAILLE_PLATEAU = tuple([DIM_PLATEAU[i] * TAILLE_BLOC[i] for i in range(2)])
TAILLE_PLABORD = tuple(
    [DIM_PLATEAU[i] * TAILLE_BLOC[i] + BORDURE_PLATEAU * 2 for i in range(2)])

MARGE = tuple([
    TAILLE_FENETRE[i] - TAILLE_PLATEAU[i] - BORDURE_PLATEAU * 2
    for i in range(2)
])
START_PLATEAU = int(MARGE[0] / 2), MARGE[1] + 2 * BORDURE_PLATEAU
START_PLABORD = int(MARGE[0] / 2) - BORDURE_PLATEAU, MARGE[1] + BORDURE_PLATEAU

CENTRE_FENETRE = tuple([TAILLE_FENETRE[i] / 2 for i in range(2)])
POS = CENTRE_FENETRE[0], CENTRE_FENETRE[1] + 100
POSITION_SCORE = TAILLE_FENETRE[0] - START_PLABORD[0] / 2, 120
POSITION_PIECES = POSITION_SCORE[0], 150
POSITION_LIGNES = POSITION_SCORE[0], 180
POSITION_TETRIS = POSITION_SCORE[0], 210
POSITION_NIVEAU = POSITION_SCORE[0], 240
#les différentes pièces composant le tetris
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
    ]
}
#la palette de couleur dispo
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