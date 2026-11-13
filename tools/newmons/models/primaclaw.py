"""Primaclaw, the Primordial Imitator Pokémon (Bug/Ground), Crabgron evolved, after the art by @dude.dude.art (shown
there as a variant Crabgron; the name is ours) and the user's idea: its claws make up nine tenths of it. A tiny black
crab body with a spiky crown and glowing blue eyes rides on long white spider legs, and two long white arms hold up
two enormous claws: the left imitates the red, plated head of the continent Pokémon (black eye markings, a jaw of
jagged grey teeth), the right the blue head of the sea Pokémon (a white jaw and spot, red-tipped fins, grey teeth).

Shiny: a golden land-claw and a magenta sea-claw.

Front is -z, y is up. 34 units tall to the top of its claws; baseScale 0.75 (1.6 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _mimic import crab_body, crab_legs, solid
from _route import pal, tone

SCALE = 0.75
HITBOX = [2.4, 2.2]
KIND = "quadruped"
K = 3
HEIGHT = 34
LOOK = ("a tiny black spiky crab on long white legs holding up two enormous claws: a red plated land-titan head and a "
        "blue sea-titan head, both with jagged teeth")

BASE = {"shell": (40, 40, 46), "belly": (90, 92, 100), "brow": (14, 14, 18), "eye": (90, 200, 250), "eye_glow": True,
        "leg": (230, 230, 234), "red": (200, 60, 40), "red_dark": (140, 36, 26), "grey": (130, 120, 112),
        "blue": (40, 90, 190), "blue_dark": (26, 60, 140), "white": (244, 244, 246), "fin": (200, 50, 50),
        "black": (22, 22, 26), "tooth": (210, 210, 214)}
SHINY = {"red": (222, 180, 60), "red_dark": (164, 124, 30), "blue": (184, 70, 160), "blue_dark": (130, 40, 112),
         "fin": (240, 210, 90)}


def P(v):
    return pal(BASE, SHINY, v)


def landf(x, y, z, face, variant, **k):
    """The land-titan claw (snout toward -x): red plates with darker seams, a black eye marking with a white glint on
    each side."""
    p = P(variant)
    u = -9.0 - x                                                               # distance toward its snout
    if face in ("north", "south") and 2.6 < u < 5.2 and 24.6 < y < 26.4:
        return (p["white"] if 3.4 < u < 4.0 and y > 25.6 else p["black"]), None
    if face != "down" and (abs(((x + 20) % 3.0) - 1.5) < 0.2):
        return tone(p["red_dark"], face), None                                 # seams between its plates
    if face == "down":
        return p["black"], None
    return tone(p["red"], face), None


def seaf(x, y, z, face, variant, **k):
    """The sea-titan claw (snout toward +x): blue above, white below, a white oval spot and a black eye each side."""
    p = P(variant)
    u = x - 9.0
    if face in ("north", "south"):
        if 3.6 < u < 5.6 and 25.2 < y < 26.4:
            return p["black"], None
        if math.hypot((u - 0.6) / 1.6, (y - 27.2) / 0.8) < 1:
            return p["white"], None
    if y < 23.6 or face == "down":
        return tone(p["white"], face), None
    return tone(p["blue"], face), None


def build() -> Model:
    m = Model("primaclaw")
    top = m.bone("primaclaw", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    crab_body(m, bd, P, 0, 0, 3.0, 2.6, 6.0, 10.6, 8.6, 1.1, -2.6, cut=1.2)  # the tiny body
    for i in range(5):                                                          # its spiky crown
        a = (i - 2) * 0.45
        spike(m, bd, (math.sin(a) * 1.6, 10.2, 0.2), (math.sin(a), 1, 0.2), 1.4, 2.6 + (i == 2) * 1.4,
              solid("shell", P), tip=0.9)
    crab_legs(m, P, top, 3, 0, 7.4, 2.6, 8.0, (-2.0, 0.4, 2.6), t=1.2)
    # two long white arms holding up the enormous claws, each head facing outward
    for nm, sx, shader, key in (("arm_left", -1, landf, "land"), ("arm_right", 1, seaf, "sea")):
        ar = m.bone(nm, bd, (sx * 2.6, 9.6, -0.6))
        hx, hz = sx * 9.0, -1.0
        rod(m, ar, (sx * 2.6, 9.6, -0.6), (sx * 6.0, 16.0, -1.0), 1.6, solid("leg", P), extend=0.3)
        rod(m, ar, (sx * 6.0, 16.0, -1.0), (hx, 21.0, hz), 1.6, solid("leg", P), extend=0.3)
        m.round_box(ar, hx + sx * 0.6, hz, 6.0, 4.6, 23.0, 30.0, shader, cut=2.0)          # the great head
        m.round_box(ar, hx + sx * 5.6, hz, 2.0, 3.4, 23.2, 28.4, shader, cut=1.2)          # its snout
        m.round_box(ar, hx + sx * 0.8, hz, 5.4, 4.2, 19.4, 22.6,
                    solid("grey" if key == "land" else "white", P), cut=1.6)                # its jaw
        for dz in (-2.6, -1.3, 0, 1.3, 2.6):                                                # jagged teeth
            spike(m, ar, (hx + sx * 6.6, 23.0, hz + dz), (0, -1, 0), 1.2, 1.6, solid("tooth", P))
        for dz in (-2.0, -0.6, 0.8, 2.2):
            spike(m, ar, (hx + sx * 5.4, 22.4, hz + dz), (0, 1, 0), 1.2, 1.4, solid("tooth", P))
        if key == "land":                                                        # stacked plates on the land claw
            for dx, h in ((3.0, 2.4), (-0.4, 3.0), (-3.8, 2.4)):
                x0 = hx + sx * dx
                m.box(ar, x0 - 1.4, 29.4, hz - 4.0, x0 + 1.4, 29.4 + h, hz + 4.0, landf,
                      rotation=(0, 0, sx * 14), pivot=(x0, 29.6, hz))
        else:                                                                    # red-tipped fins on the sea claw
            for fsz in (-1, 1):
                spike(m, ar, (hx - sx * 0.6, 26.0, hz + fsz * 3.8), (-sx * 0.9, 0.3, fsz * 1), 1.8, 3.6,
                      solid("blue_dark", P), tip=1.0)
                spike(m, ar, (hx - sx * 2.8, 26.8, hz + fsz * 6.2), (-sx * 1, 0.2, fsz * 0.6), 1.2, 1.6, solid("fin", P))
            spike(m, ar, (hx - sx * 2.0, 29.6, hz), (-sx * 1, 0.6, 0), 1.8, 4.0, solid("blue_dark", P), tip=1.0)
    return m
