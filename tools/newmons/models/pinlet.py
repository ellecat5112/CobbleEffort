"""Pinlet, the Nestling Pokémon (Normal/Flying), the first of the pinbird line: a round little chick with a white face
and belly, a red cap with a tuft on top, big grey eyes with star-shaped glints, a small yellow beak, little brown wings
held up with white tips, a stubby pair of banded tail streamers and yellow feet.

Front is -z, y is up. 14 units tall to the tuft; baseScale 0.45 (0.4 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _pinbird import P, beakf, bodyf, eye, feetf, redf, streamer, whitef, wingf
from _route import tone

SCALE = 0.45
HITBOX = [0.9, 0.9]
KIND = "biped"
K = 6
HEIGHT = 14
LOOK = ("a round chick with a white face and belly, a red cap and tuft, big grey eyes with star glints, a small "
        "yellow beak, little raised brown wings and a stubby banded tail")


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    for sx in (-1, 1):
        c = eye(face, x, y, sx * 1.4, 10.0, 1.05, variant, star=True)
        if c is not None:
            return c, None
    if face == "up" or y > 11.4 or face == "south" or (face in ("east", "west") and y > 10.6):
        return redf(x, y, z, face, variant)                                # the red cap
    return whitef(x, y, z, face, variant)


def build() -> Model:
    m = Model("pinlet")
    top = m.bone("pinlet", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    m.round_box(bd, 0, 0.2, 2.8, 2.6, 2.2, 7.6, bodyf(8.0, 2.1), cut=1.4)       # round body, white belly
    hd = m.bone("head", bd, (0, 8, -0.3))
    m.round_box(hd, 0, -0.4, 3.3, 3.0, 7.2, 12.8, headf, cut=1.4)              # a big round head
    m.box(hd, -0.65, 8.7, -4.0, 0.65, 9.6, -3.3, beakf)                          # little beak
    m.box(hd, -0.45, 8.2, -3.7, 0.45, 8.7, -3.3, beakf)
    rod(m, hd, (0, 12.5, -0.4), (0, 14.0, 1.2), 1.3, redf, extend=0.2, t2=0.9)  # the tuft on its cap
    for nm, sx in (("wing_left", 1), ("wing_right", -1)):                       # little raised wings
        w = m.bone(nm, bd, (sx * 2.7, 6.6, 0))
        x0, x1 = sx * 2.5, sx * 7.0
        m.box(w, min(x0, x1), 6.6, -1.6, max(x0, x1), 6.6, 2.4, wingf(x0, x1, -1.6, 2.4, feathers=4, tip_white=True),
              rotation=(0, 0, -sx * 34), pivot=(sx * 2.6, 6.6, 0))
    tl = m.bone("tail", bd, (0, 4, 2.6))
    for sx in (-1, 1):                                                          # stubby banded streamers
        streamer(m, tl, [(sx * 0.6, 4.2, 2.4), (sx * 0.9, 3.4, 4.4), (sx * 1.1, 3.0, 6.0)], 1.1, 0.9, period=1.4)
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):
        lg = m.bone(nm, top, (sx * 1.2, 2.6, 0))
        rod(m, lg, (sx * 1.2, 2.6, 0), (sx * 1.2, 0.5, -0.2), 0.8, feetf, extend=0.1)
        for dx, dz in ((-0.5, -1.2), (0.5, -1.2), (0, 0.7)):
            rod(m, lg, (sx * 1.2, 0.35, -0.2), (sx * 1.2 + dx, 0.2, dz - 0.2), 0.5, feetf, extend=0.1)
    return m
