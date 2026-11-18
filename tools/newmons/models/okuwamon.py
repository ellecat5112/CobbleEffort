"""Okuwamon (a Digimon of the CobbleEffort: Digital crossover; after the official art on wikimon.net): the silver stag beetle: Kuwagamon grown huge in grey-silver armour streaked red, its serrated pincers spread wide, a black mane, a gaping fanged maw, clawed arms and translucent wings.
25 blocks tall.

Front is -z, y is up. 50 units tall; Perfect stage. Kuwagamon's body (_kuwagamon.make) with its own colours.
"""
from _digi import sized
from _variant import clone

_K = clone("_kuwagamon", "okuwamon", base={"red": (200, 204, 214), "red_dark": (110, 114, 126), "red_light": (240, 242, 250), "black": (170, 30, 40)},
           shiny={"red": (230, 190, 80), "red_dark": (160, 120, 30), "red_light": (255, 230, 150)})
HEIGHT = 50
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "the silver stag beetle: Kuwagamon grown huge in grey-silver armour streaked red, its serrated pincers spread wide, a black mane, a gaping fanged maw, clawed arms and translucent wings"
build = _K.make("okuwamon", x=False)
