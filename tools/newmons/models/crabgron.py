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
from _route import pal

SCALE = 0.45
HITBOX = [3.0, 2.6]
KIND = "quadruped"
K = 4
HEIGHT = 36
LOOK = ("a charcoal crab with glowing blue eyes and a spiky shell; its right claw is an Aggron's head, borrowed from "
        "Cobblemon's own Aggron, its left a big white pincer")
# its claw: Aggron's head from Cobblemon's model, snout turned out to the right
BORROW = [{"src": "aggron", "parent": "arm_right", "at": (6.0, 17.0, -1.0), "rotation": (0, -65, 0), "prefix": "aggron_"}]

BASE = {"shell": (52, 54, 60), "belly": (196, 198, 204), "brow": (20, 20, 24), "eye": (90, 200, 250), "eye_glow": True,
        "leg": (120, 122, 130), "claw": (232, 232, 236)}
SHINY = {"shell": (34, 44, 78), "claw": (190, 208, 236)}


def P(v):
    return pal(BASE, SHINY, v)


def build() -> Model:
    m = Model("crabgron")
    top = m.bone("crabgron", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    crab_body(m, bd, P, 0, 0, 5.2, 4.2, 3.6, 11.0, 8.6, 2.0, -4.2, cut=1.8)
    for x, h in ((-2.4, 2.6), (0, 3.6), (2.4, 2.6)):                            # spikes along its shell
        spike(m, bd, (x, 10.6, 0.8), (x * 0.15, 1, 0.5), 1.8, h, solid("shell", P), tip=1.0)
    crab_legs(m, P, top, 3, 0, 6.0, 4.6, 6.6, (-2.2, 0.4, 3.0), t=1.5)
    ar = m.bone("arm_right", bd, (4.4, 9.0, -1.0))
    rod(m, ar, (4.2, 9.0, -1.0), (5.6, 14.0, -1.0), 2.0, solid("leg", P), extend=0.4)       # the arm up to its head
    al = m.bone("arm_left", bd, (-4.6, 7.6, -1.0))
    pincer(m, al, P, (-4.6, 7.6, -1.0), (-8.4, 6.6, -5.0), 4.6)                              # a big white pincer
    return m
