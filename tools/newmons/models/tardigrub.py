"""Tardigrub, the Water Bear Pokémon (Water/Bug), after @victorious_trainer's Pokémon Victory art (name kept): a plump,
glossy teal tardigrade with a segmented back, a darker belly, a round red mouth ring set in a black X on its blunt face,
round spots on the sides of its head and four pairs of stubby legs with little toe nubs.

Shiny: pink with a teal mouth ring.

Front is -z, y is up. 9.2 units tall; baseScale 0.7 (0.4 m).
"""
from __future__ import annotations

from _boxmodel import Model
from _tardi import grub, palette

SHINY = {"teal": (240, 170, 200), "teal_light": (252, 214, 232), "teal_dark": (200, 116, 160), "teal_deep": (150, 80, 124),
         "mouth": (60, 190, 190), "mouth_dark": (24, 90, 96)}
P, solid, ramp = palette(SHINY)
SCALE = 0.7
HITBOX = [0.9, 0.6]
KIND = "quadruped"
K = 6
HEIGHT = 9
LOOK = ("a plump glossy teal tardigrade with a segmented back, a red mouth ring in a black X on its blunt face and four "
        "pairs of stubby legs")


def build() -> Model:
    m = Model("tardigrub")
    top = m.bone("tardigrub", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    hd = m.bone("head", bd, (0, 5, -5))
    legs = {}

    def leg_bone(i, side):
        name = f"leg_{i + 1}_{side}"
        if name not in legs:
            legs[name] = m.bone(name, top, (4.4 if side == "left" else -4.4, 2.6, (-3.6, -1.0, 1.8, 4.6)[i]))
        return legs[name]
    grub(m, bd, (0, 0, 0), 1.0, P, leg_bone=leg_bone, head_bone=hd)
    return m
