"""Pipider, the Seed Spider Pokémon (Bug/Grass), a route-one Pokémon, hand-built from boxes from the user's design.

A SUPER tiny spider that wears a seed on its back like a shell: a big glossy dark-brown seed with a pale streak, a
little round face peeking out under its front edge with two big orange eyes ringed in lime green, two curly green
sprout feelers, and eight tiny lime legs.

Front is -z, y is up. 13 units tall; baseScale 0.13 (0.1 m: smaller than anything but the tiniest Pokémon).
"""
from __future__ import annotations

from _boxmodel import Model, chain, mix, rod
from _route import pal, round_eye, tone

SCALE = 0.13
HITBOX = [1.92, 1.54]
KIND = "quadruped"
K = 8
LOOK = ("a super tiny spider wearing a big glossy seed on its back like a shell, with two big lime-ringed orange "
        "eyes, curly sprout feelers and eight tiny lime legs")

BASE = {"seed": (104, 92, 82), "seed_dark": (70, 60, 54), "streak": (226, 214, 204), "face": (90, 78, 70),
        "lime": (206, 240, 80), "lime_dark": (150, 190, 40), "iris": (255, 110, 10), "gold": (232, 210, 40)}
SHINY = {"seed": (196, 150, 70), "seed_dark": (150, 104, 40), "streak": (255, 240, 200), "iris": (60, 200, 255),
         "lime": (255, 170, 60), "lime_dark": (210, 120, 30)}


def seed(x, y, z, face, variant, **k):
    P = pal(BASE, SHINY, variant)
    if face in ("north", "west", "up") and abs((x + z) * 0.6 - (y - 9) * 0.9) < 0.6 and y > 7:
        return P["streak"], None                                   # the pale streak down its gloss
    c = mix(P["seed"], P["seed_dark"], max(0.0, min(1.0, (5 - y) / 3)))
    return tone(c, face), None


def facef(x, y, z, face, variant, **k):
    P = pal(BASE, SHINY, variant)
    if face == "north":
        for sx in (-1, 1):
            e = round_eye(x - sx * 1.25, y - 3.4, 1.1, P["iris"], ring=P["lime"])
            if e:
                return e
    return tone(P["face"], face), None


def lime(x, y, z, face, variant, **k):
    return tone(pal(BASE, SHINY, variant)["lime"], face), None


def build() -> Model:
    m = Model("pipider")
    top = m.bone("pipider", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    m.round_box(bd, 0, 0.5, 4, 4.5, 2.5, 10, seed, cut=2)                 # the seed shell
    m.round_box(bd, 0, 1.2, 2.6, 3, 10, 12, seed, cut=1)
    m.box(bd, -1, 12, 0.7, 1, 13, 2.2, seed)                                # its tip
    m.box(bd, -4.2, 2.2, -3.5, 4.2, 3, 4.5, lime)                          # a lime rim along the shell's edge
    hd = m.bone("head", bd, (0, 3, -3.5))
    m.round_box(hd, 0, -4.2, 2.6, 1.6, 1.4, 5.6, facef, cut=1)
    for sx in (-1, 1):                                                      # curly sprout feelers
        chain(m, hd, [(sx * 1.2, 5.4, -4.4), (sx * 2.2, 7, -5.2), (sx * 3.2, 7.3, -4.2), (sx * 3.0, 6.6, -3.4)],
              [0.8, 0.8, 0.8], lime)
    legs = [("leg_front_left", -1, -2.5), ("leg_front_right", 1, -2.5), ("leg_mid1_left", -1, -0.5),
            ("leg_mid1_right", 1, -0.5), ("leg_mid2_left", -1, 1.5), ("leg_mid2_right", 1, 1.5),
            ("leg_back_left", -1, 3.5), ("leg_back_right", 1, 3.5)]
    for nm, sx, lz in legs:
        leg = m.bone(nm, top, (sx * 3.2, 3, lz))
        rod(m, leg, (sx * 3.2, 3, lz), (sx * 5, 0.2, lz * 1.25), 1, lime)
    return m
