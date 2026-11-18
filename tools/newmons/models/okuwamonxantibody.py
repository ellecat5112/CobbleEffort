"""Okuwamon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; after the official art on wikimon.net): Okuwamon changed by the X-Antibody: a darker gunmetal stag beetle banded red with longer straight pincers, a wide fanged maw and more limbs.
25 blocks tall.

Front is -z, y is up. 50 units tall; Perfect stage. Kuwagamon's body (_kuwagamon.make) with its own colours.
"""
from _digi import sized
from _variant import clone

_K = clone("_kuwagamon", "okuwamonxantibody", base={"red": (120, 120, 130), "red_dark": (50, 50, 58), "red_light": (190, 190, 200), "black": (150, 30, 30)},
           shiny={"red": (230, 190, 80), "red_dark": (160, 120, 30), "red_light": (255, 230, 150)})
HEIGHT = 50
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "Okuwamon changed by the X-Antibody: a darker gunmetal stag beetle banded red with longer straight pincers, a wide fanged maw and more limbs"
build = _K.make("okuwamonxantibody", x=True)
