"""Kiq, the Kickbox Pokémon (Fighting), after @magikdex's Cornera region art (name kept): Chawp's third evolution,
beside Sawk and Throh. A tall kickboxer of rounded, quilted grey-blue segments: big round shoulder pads with dark
crescents, a V-shaped muscular chest, arms raised in a boxing guard, a black tunic with a white hem and belt, thick
legs and big rounded feet; its small round head is crossed by a dark X-shaped mask whose bands jut far out to the sides,
one steady grey eye showing.

Shiny: a pale mask and greener skin.

Front is -z, y is up. 37 units tall; baseScale 0.61 (1.4 m).
"""
from __future__ import annotations

from _boxmodel import Model
from _gi import eye_disc, near_seg, palette
from _kiq import HEAD_Y, build_body, mask_x

SHINY = {"skin": (180, 212, 198), "skin_shade": (144, 178, 164), "seam": (112, 146, 134), "mask": (232, 232, 226)}
P, solid, ramp = palette(SHINY)
SCALE = 0.61
HITBOX = [1.0, 2.3]
KIND = "biped"
K = 4
HEIGHT = 37
LOOK = ("a tall kickboxer of rounded quilted grey-blue segments with big shoulder pads, a black tunic and white belt, "
        "arms raised in a guard and an X-shaped mask across its small round head")
EYE = (-1.3, HEAD_Y + 0.05)


def face(x, y, f, p):
    if f != "north":
        return None
    e = eye_disc(p, x, y, EYE[0], EYE[1], 0.85, "eye", ry=0.75)
    if e is not None:
        return e
    if near_seg(x, y, (2.6, HEAD_Y + 2.7), (-2.6, HEAD_Y - 2.5), 0.62):
        return p["mask"]                                               # the X's other band
    return None


def build() -> Model:
    m = Model("kiq")
    top = m.bone("kiq", None, (0, 0, 0))
    bd, hd = build_body(m, top, P, solid, face=face)
    m.box(hd, -7.2, HEAD_Y - 1.0, -3.75, 7.2, HEAD_Y + 1.0, -3.75,
          mask_x(P, "mask", [(EYE[0], EYE[1], 0.85, None)], half=0.95))           # the band that juts out to the sides
    return m
