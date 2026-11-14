"""Ufly, the Neon Light Pokémon (Bug/Psychic), after @maumesdex's art (name kept): a plump little purple bug with a
lime-green back, two big translucent wings standing up like ears, two great teal compound eyes and glowing teal
spots. Alone it is tiny and harmless; its ability Neon Swarm calls thousands more, and they fly as one great saucer
(ufly_swarm.py).

Shiny: magenta with an orange back and gold lights.

Front is -z, y is up. 15 units tall (to the wing tips); baseScale 0.5 (0.4 m).
"""
from __future__ import annotations

from _boxmodel import Model
from _route import tone
from _ufly import P, compound_eye, solid, spotted, wing

SCALE = 0.5
HITBOX = [0.9, 0.8]
KIND = "floater"
K = 8
HEIGHT = 15
LOOK = ("a plump little purple bug with a lime-green back, two big translucent wings standing up like ears, great teal "
        "compound eyes and glowing teal spots")


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and y < 6.5:
        for sx in (-1, 1):
            c = compound_eye(p, x - sx * 2.2, y - 3.6, 2.1)
            if c is not None:
                return c
    if y > 5.6 - 0.25 * max(0.0, -z):                                  # the lime back, lower behind
        return tone(p["lime"] if y > 6.2 else p["lime_dark"], face), None
    return spotted("purple", 2.0, 0.42)(x, y, z, face, variant)


def build() -> Model:
    m = Model("ufly")
    top = m.bone("ufly", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    m.round_box(bd, 0, 0, 4.0, 3.6, 1, 2, bodyf, cut=1.5)
    m.round_box(bd, 0, 0, 5.0, 4.6, 2, 7, bodyf, cut=1.8)
    m.round_box(bd, 0, 0.3, 4.2, 3.8, 7, 8.6, bodyf, cut=1.5)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                 # little dark feet
        lg = m.bone(nm, top, (sx * 2.2, 1.5, -1))
        m.box(lg, sx * 2.2 - 0.8, 0, -2.4, sx * 2.2 + 0.8, 1.6, -0.6, solid("foot"))
        m.box(lg, sx * 2.6 - 0.8, 0, 1.2, sx * 2.6 + 0.8, 1.6, 2.8, solid("foot"))
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):               # two big wings standing up like ears
        w = m.bone(nm, bd, (sx * 2.0, 8.2, 0.8))
        x0, x1 = sorted((sx * 1.0, sx * 5.0))
        m.box(w, x0, 8, 0.8, x1, 15, 0.8, wing(), rotation=(-8, 0, -sx * 24), pivot=(sx * 2.0, 8.2, 0.8))
    return m
