"""Holy Digitamamon (a Digimon of the CobbleEffort: Digital crossover; after its pixel-sprite art on wikimon.net, the
only picture there is): a haloed egg-shaped figure flanked by little winged arms on two clawed feet, from a monochrome
virtual-pet sprite turned into a block figure (each pixel 2 units, gaps left open). 35 blocks tall.

Front is -z, y is up. 32 units tall; Ultimate stage.
"""
from _digi import sized
from _dot import make

HEIGHT = 32
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "floater"
K = 4
LOOK = "a haloed egg-shaped figure with little winged arms on clawed feet, as a block-figure pixel sprite"
ROWS = ['......AAAA......', '.....A....A.....', '......AAAA......', '................', '......AAAA......',
        '..AA.A....A.AA..', '.A..AA....AA..A.', 'A.A.A......A.A.A', 'AA..A.AAAA.A..AA', 'A.AA.A.AA.A.AA.A',
        'AA.A.AAAAAA.A.AA', 'A.A.A.AAAA.A.A.A', 'AA..A......A..AA', 'A....A....A....A', '....AAAAAAAA....',
        '...AAA....AAA...']
BASE = {'A': (60, 56, 50)}
SHINY = {'A': (200, 170, 70)}
build = make("holydigitamamon", ROWS, BASE, SHINY, px=2.0, depth=4)
