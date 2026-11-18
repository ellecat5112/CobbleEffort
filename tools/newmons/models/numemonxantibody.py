"""Numemon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; after the official art on wikimon.net):
Numemon changed by the X-Antibody: a hot-pink slime blob with violet patches, its eye stalks crossed in an X, a huge
fanged grin and a long violet tongue. 15 blocks tall.

Front is -z, y is up. 30 units tall; Adult stage. Built by _numemon.make(look="x").
"""
from _boxmodel import rod
from _digi import sized
from _digidetail import solid
from _numemon import make
from _route import pal

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = "a hot-pink slime blob with violet patches, X-crossed eye stalks, a huge fanged grin and a long violet tongue"
_body = make("numemonxantibody", "x", shiny_look={"slime": (120, 200, 240), "slime_dark": (60, 130, 190),
                                                  "slime_light": (210, 240, 255), "spot": (40, 70, 150)})


def P(v):
    return pal({"violet": (130, 70, 190)}, {"violet": (40, 70, 150)}, v)


def build():
    m = _body()
    for sx in (-1, 1):                                                                   # the X of crossed stalks
        rod(m, "body", (sx * 3.0, 14.0, -2.0), (-sx * 3.0, 22.0, -2.0), 1, solid(P, "violet"), extend=0.2, t2=2)
    return m
