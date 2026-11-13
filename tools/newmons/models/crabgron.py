"""Crabgron, the Imitator Pokémon (Bug/Steel), Tyrucrab evolved, after the art by @dude.dude.art (the art's own name):
a charcoal crab with fierce glowing blue eyes, spikes along its shell and grey legs. Its right claw now imitates a
steel-armoured Pokémon's head: a white steel helmet with two long swept-back horns, a dark eye and a jaw lined with
jagged steel teeth. Its left claw is a big white pincer.

Shiny: a navy shell and a blued-steel helmet.

Front is -z, y is up. 26 units tall to the horn tips; baseScale 0.62 (1.0 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _mimic import crab_body, crab_legs, pincer, solid
from _route import pal, tone

SCALE = 0.62
HITBOX = [1.8, 1.6]
KIND = "quadruped"
K = 4
HEIGHT = 26
LOOK = ("a charcoal crab with glowing blue eyes and a spiky shell; its right claw is a white steel-helmeted head with "
        "two long horns and jagged teeth, its left a big white pincer")

BASE = {"shell": (52, 54, 60), "belly": (196, 198, 204), "brow": (20, 20, 24), "eye": (90, 200, 250), "eye_glow": True,
        "leg": (120, 122, 130), "claw": (232, 232, 236), "steel": (230, 232, 236), "steel_shade": (180, 184, 192),
        "mouth": (40, 40, 46), "pupil": (24, 24, 28)}
SHINY = {"shell": (34, 44, 78), "steel": (176, 196, 226), "steel_shade": (130, 150, 184), "claw": (190, 208, 236)}


def P(v):
    return pal(BASE, SHINY, v)


def helmetf(x, y, z, face, variant, **k):
    """The steel helmet (snout along +x): a dark eye on each side."""
    p = P(variant)
    if face in ("north", "south") and 9.2 < x < 10.8 and 16.0 < y < 17.4:
        return p["pupil"], None
    if face == "down":
        return p["mouth"], None
    return tone(p["steel"] if face in ("up", "north", "south", "east") else p["steel_shade"], face), None


def build() -> Model:
    m = Model("crabgron")
    top = m.bone("crabgron", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    crab_body(m, bd, P, 0, 0, 4.2, 3.4, 3.0, 9.0, 6.8, 1.6, -3.4, cut=1.6)
    for x, h in ((-2.0, 2.2), (0, 3.0), (2.0, 2.2)):                            # spikes along its shell
        spike(m, bd, (x, 8.6, 0.6), (x * 0.15, 1, 0.5), 1.6, h, solid("shell", P), tip=1.0)
    crab_legs(m, P, top, 3, 0, 5.0, 3.6, 5.4, (-1.8, 0.4, 2.4), t=1.3)
    # the right claw: a steel-helmeted head with long horns, its snout pointing out to the side
    ar = m.bone("arm_right", bd, (3.6, 7.6, -1.0))
    rod(m, ar, (3.4, 7.6, -1.0), (6.2, 13.0, -1.6), 1.8, solid("leg", P), extend=0.4)
    hx, hz = 8.2, -1.8
    m.round_box(ar, hx + 0.6, hz, 4.6, 3.4, 15.0, 19.8, helmetf, cut=1.4)     # the helmet
    m.round_box(ar, hx + 4.6, hz, 1.6, 2.6, 15.2, 18.2, helmetf, cut=0.8)     # its brow ridge
    for dz in (-1.6, 1.6):                                                      # two long swept-back horns
        rod(m, ar, (hx + 1.0, 19.0, hz + dz), (hx - 6.0, 25.0, hz + dz * 1.4), 1.8, solid("steel", P), extend=0.3, t2=1.2)
    jw = m.bone("jaw", ar, (hx - 2.0, 14.8, hz))
    m.round_box(jw, hx + 1.0, hz, 4.0, 3.0, 11.6, 13.8, helmetf, cut=1.2)     # the lower jaw
    for dz in (-1.8, -0.6, 0.6, 1.8):                                           # jagged steel teeth
        spike(m, ar, (hx + 4.6, 15.0, hz + dz), (0, -1, 0), 1.0, 1.2, solid("steel", P))
    for dz in (-1.2, 0, 1.2):
        spike(m, jw, (hx + 4.2, 13.6, hz + dz), (0, 1, 0), 1.0, 1.2, solid("steel", P))
    # the left claw: a big white pincer
    al = m.bone("arm_left", bd, (-3.6, 6.6, -1.0))
    pincer(m, al, P, (-3.6, 6.6, -1.0), (-6.4, 5.6, -4.4), 3.8)
    return m
