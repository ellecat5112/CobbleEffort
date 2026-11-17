"""Dot Falcomon (a Digimon of the CobbleEffort: Digital crossover; after the pixel-sprite art on wikimon.net): a little navy owl ninja of chunky pixel blocks with ear tufts, red eyes, an orange beak, a purple scarf and orange feet. Its
sprite turned into a block figure (each pixel 2 units). Child stage, 1 block tall.

Front is -z, y is up. 26 units tall.
"""
from _digi import sized
from _dot import make

HEIGHT = 26
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a little navy owl ninja of chunky pixel blocks with ear tufts, red eyes, an orange beak, a purple scarf and orange feet"
ROWS = ['..N......N..', '..NN....NN..', '..NNNNNNNN..', '.NNNNNNNNNN.', '.NWWRWWRWWN.', '.NWWWOOWWWN.', '..NNNOONNN..', '.PPPPPPPPPP.', 'NN.NNNNNN.NN', 'N..NNNNNN..N', '...NNNNNN...', '...OO..OO...', '..OOO..OOO..']
BASE = {'N': (50, 50, 110), 'W': (240, 236, 220), 'R': (220, 30, 40), 'O': (250, 150, 40), 'P': (130, 60, 170)}
SHINY = {'N': (110, 60, 40), 'P': (40, 150, 90)}
build = make("dotfalcomon", ROWS, BASE, SHINY, px=2.0, depth=4, head_rows=7, leg_rows=2, deep={'W': 5, 'R': 5, 'O': 5, 'P': 5})
