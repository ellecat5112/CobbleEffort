"""Bongwater, the Bubbler Pokémon (Water/Poison), the Nicodex's Water type before it evolves (the user's design): a
little round glass flask half full of water, with a tall glass neck, a brass mouthpiece rim, a brass downstem and bowl
sticking out of its side, two big eyes and bubbles drifting up inside it.

Shiny: violet glass and water.

Front is -z, y is up. 20 units tall; baseScale 0.48 (0.6 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _nico import eye_on, palette, puff, translucent

SHINY = {"glass": (222, 196, 246, 110), "water": (170, 110, 220, 150), "brass": (200, 200, 214)}
P, solid, ramp = palette(SHINY)
SCALE = 0.48
HITBOX = [0.8, 1.25]
KIND = "quadruped"
K = 5
HEIGHT = 20
LOOK = "a little round glass flask half full of water with a tall glass neck, a brass downstem and bowl and big eyes"
eyes = eye_on(P, "teal", [(-1.5, 6.0), (1.5, 6.0)], 1.0)


def glassf(x, y, z, face, variant, **k):
    e = eyes(x, y, z, face, variant)
    if e:
        return e, None
    return P(variant)["glass"], None


def build() -> Model:
    m = Model("bongwater")
    top = m.bone("bongwater", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    m.round_box(bd, 0, 0, 4.4, 4.2, 0.0, 9.0, glassf, cut=1.6)                  # the glass flask
    m.round_box(bd, 0, 0, 3.6, 3.4, 0.4, 5.0, translucent(P, "water"), cut=1.2) # water inside
    for c, r in (((1.0, 3.0, 0.4), 0.5), ((-1.2, 5.6, -0.8), 0.6), ((0.4, 7.6, 0.6), 0.5)):
        puff(m, bd, c, r, translucent(P, "mist"))                               # bubbles
    hd = m.bone("head", bd, (0, 9, 0))
    rod(m, hd, (0, 8.6, 0), (0, 18.4, 0.4), 2.6, translucent(P, "glass"), extend=0.4)   # the tall glass neck
    m.round_box(hd, 0, 0.4, 1.8, 1.8, 18.0, 19.4, solid("brass"), cut=0.6)       # brass mouthpiece rim
    rod(m, bd, (2.2, 3.6, -1.4), (4.6, 9.4, -3.8), 1.2, solid("brass"), extend=0.4)    # the downstem
    m.round_box(bd, 4.8, -4.0, 1.2, 1.2, 9.0, 10.6, solid("brass"), cut=0.4)     # and bowl
    return m
