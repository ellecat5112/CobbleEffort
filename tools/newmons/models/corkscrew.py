"""Corkscrew, the Corkscrew Pokémon (Flying/Steel), a Liquor Meadows Pokémon (the user's design): a nimble little
winged sprite shaped like a winged wine opener: a polished steel body and round head with a knob crown, two
lever-arm wings with wide paddle tips that pop up when it launches, and a spiral drill-like worm for a tail.

Shiny: gold with copper wings.

Front is -z, y is up. 18 units tall; baseScale 0.45 (0.5 m). A floater; the drill is a `spin` bone.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _liquor import eye_on, helix, palette, puff
from _route import tone

SHINY = {"silver": (236, 200, 90), "steel": (210, 170, 70), "steel_dark": (160, 120, 40), "iron_light": (210, 130, 80)}
P, solid, ramp = palette(SHINY)
SCALE = 0.45
HITBOX = [0.8, 1.0]
KIND = "floater"
K = 5
HEIGHT = 18
LOOK = "a winged steel wine-opener sprite with lever-arm wings and a spiral drill tail"
ANIM = {"wing_flap": 16}
eyes = eye_on(P, "cyan" if False else "steel_dark", [(-0.9, 14.4), (0.9, 14.4)], 0.6)


def bodyf(x, y, z, face, variant, **k):
    e = eyes(x, y, z, face, variant)
    if e:
        return e, None
    return tone(P(variant)["silver"], face), None


def build() -> Model:
    m = Model("corkscrew")
    top = m.bone("corkscrew", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 0))
    m.round_box(bd, 0, 0, 1.4, 1.4, 6.0, 12.4, solid("steel"), cut=0.5)       # the shaft body
    hd = m.bone("head", bd, (0, 13, 0))
    puff(m, hd, (0, 14.4, 0), 2.2, bodyf)                                     # round head
    m.round_box(hd, 0, 0, 0.9, 0.9, 16.4, 18.0, solid("steel_dark"), cut=0.3) # the knob crown
    sp = m.bone("spin_tail", bd, (0, 6, 0))
    helix(m, sp, (0, 0, 0), 1.1, 0.4, 6.0, 3.0, 0.6, solid("silver"))         # the spiral worm
    rod(m, sp, (0, 1.0, 0), (0, -0.6, 0), 0.4, solid("steel_dark"), extend=0.1)
    for sx, side in ((-1, "left"), (1, "right")):
        w = m.bone(f"wing_{side}", bd, (sx * 1.2, 11, 0))
        rod(m, w, (sx * 1.2, 11.0, 0.0), (sx * 6.6, 14.2, 0.0), 1.0, solid("steel"), extend=0.3)   # lever arm
        m.round_box(w, sx * 7.2, 0, 1.4, 1.0, 13.2, 16.6, solid("iron_light"), cut=0.4)          # paddle tip
    return m
