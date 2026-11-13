"""Tyrucrab, the Imitator Pokémon (Bug/Rock), after the art by @dude.dude.art (the art's own name): a little brown crab
with an angry face, an orange spike on its back and thin grey legs. Its right claw imitates a tyrannosaur Pokémon's
head: a big brown snout with orange spikes, a spiky white frill behind and a huge white lower jaw that snaps like a
pincer. Its left claw is a plain grey pincer.

Shiny: a slate-blue shell with golden spikes.

Front is -z, y is up. 15 units tall to the top of its claw-head; baseScale 0.55 (0.5 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _mimic import crab_body, crab_legs, pincer, solid
from _route import pal

SCALE = 0.32
HITBOX = [2.6, 2.2]
KIND = "quadruped"
K = 5
HEIGHT = 26
LOOK = ("a little brown crab with an angry face and an orange back spike; its right claw is a Tyrunt's head, borrowed "
        "from Cobblemon's own Tyrunt")
# its claw: Tyrunt's head from Cobblemon's model (tools/newmons/borrow_heads.py), snout turned out to the right and a little forward (rotation y: -90 points it to +x)
BORROW = [{"src": "tyrunt", "parent": "arm_right", "at": (3.0, 16.0, -1.0), "rotation": (0, -65, 0), "prefix": "tyrunt_"}]

BASE = {"shell": (124, 92, 72), "belly": (92, 66, 52), "brow": (40, 28, 24), "eye": (250, 248, 240), "leg": (196, 196, 200),
        "claw": (200, 200, 206), "spike": (236, 136, 32)}
SHINY = {"shell": (82, 104, 128), "belly": (58, 74, 94), "spike": (240, 200, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def build() -> Model:
    m = Model("tyrucrab")
    top = m.bone("tyrucrab", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    crab_body(m, bd, P, 0, 0, 4.6, 3.8, 3.0, 9.8, 7.4, 1.8, -3.8, cut=1.6)
    spike(m, bd, (-1.0, 9.6, 1.0), (-0.3, 1, 0.4), 2.0, 3.0, solid("spike", P), tip=1.2)      # orange back spike
    crab_legs(m, P, top, 3, 0, 5.0, 4.0, 5.6, (-2.0, 0.4, 2.6), t=1.3)
    ar = m.bone("arm_right", bd, (3.6, 8.0, -1.0))
    rod(m, ar, (3.4, 8.0, -1.0), (3.4, 14.0, -1.0), 1.6, solid("leg", P), extend=0.3)        # the arm up to its head
    al = m.bone("arm_left", bd, (-3.8, 6.4, -1.0))
    pincer(m, al, P, (-3.8, 6.4, -1.0), (-7.4, 6.8, -3.6), 3.2)                              # a plain grey pincer
    return m
