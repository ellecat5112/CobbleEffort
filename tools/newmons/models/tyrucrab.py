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
from _route import pal, tone

SCALE = 0.55
HITBOX = [1.4, 1.0]
KIND = "quadruped"
K = 5
HEIGHT = 15
LOOK = ("a little brown crab with an angry face and an orange back spike; its right claw is a tyrannosaur-like head "
        "with orange spikes, a white frill and a huge white jaw")

BASE = {"shell": (124, 92, 72), "belly": (92, 66, 52), "brow": (40, 28, 24), "eye": (250, 248, 240), "leg": (196, 196, 200),
        "claw": (200, 200, 206), "spike": (236, 136, 32), "jaw": (238, 236, 232), "frill": (246, 246, 246),
        "mouth": (70, 40, 40)}
SHINY = {"shell": (82, 104, 128), "belly": (58, 74, 94), "spike": (240, 200, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, **k):
    """The tyrannosaur head-claw (its snout points out along +x): brown, a white slit eye on each side."""
    p = P(variant)
    if face in ("north", "south") and 7.4 < x < 8.6 and 11.4 < y < 12.9:
        return p["eye"], None
    if face == "down":
        return p["mouth"], None
    return tone(p["shell"], face), None


def build() -> Model:
    m = Model("tyrucrab")
    top = m.bone("tyrucrab", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    crab_body(m, bd, P, 0, 0, 3.2, 2.7, 2.2, 6.6, 5.0, 1.2, -2.7, cut=1.2)
    spike(m, bd, (0.6, 6.4, 0.8), (0.3, 1, 0.4), 1.6, 2.2, solid("spike", P), tip=1.0)      # orange back spike
    crab_legs(m, P, top, 3, 0, 3.6, 2.8, 4.0, (-1.4, 0.4, 2.0))
    # the right claw: a tyrannosaur head on a grey arm, its snout pointing out to the side
    ar = m.bone("arm_right", bd, (2.6, 5.4, -1.0))
    rod(m, ar, (2.4, 5.4, -1.0), (4.6, 9.0, -1.6), 1.4, solid("leg", P), extend=0.3)
    hx, hz = 6.2, -1.8
    m.round_box(ar, hx + 0.4, hz, 4.0, 3.0, 10.6, 14.4, headf, cut=1.3)       # the big snout
    m.round_box(ar, hx + 3.6, hz, 1.6, 2.3, 10.8, 13.4, headf, cut=0.7)       # its blunt nose
    for dx in (-2.0, 0.6):                                                      # orange spikes on top
        spike(m, ar, (hx + dx, 14.2, hz), (-0.3, 1, 0), 1.4, 1.8, solid("spike", P), tip=0.9)
    for i, (dy, dz) in enumerate(((1.4, 0.6), (0, 1.2), (-1.4, 0.6))):        # the white frill behind
        for sz in (-1, 1):
            spike(m, ar, (hx - 3.4, 12.0 + dy, hz + sz * dz), (-1, dy * 0.6, sz * 0.4), 1.4, 2.4 + (i % 2) * 0.6,
                  solid("frill", P), tip=0.8)
    jw = m.bone("jaw", ar, (hx - 1.0, 10.4, hz))
    m.round_box(jw, hx + 0.6, hz, 3.6, 3.2, 8.2, 10.0, solid("jaw", P), cut=1.2)   # the huge white lower jaw
    m.box(jw, hx + 3.4, 9.8, hz - 2.0, hx + 4.4, 10.6, hz + 2.0, solid("jaw", P))  # its upturned lip
    # the left claw: a plain grey pincer
    al = m.bone("arm_left", bd, (-2.6, 4.6, -1.0))
    pincer(m, al, P, (-2.6, 4.6, -1.0), (-5.0, 4.8, -3.0), 2.4)
    return m
