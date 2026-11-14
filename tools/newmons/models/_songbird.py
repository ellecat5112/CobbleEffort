"""Shared colours for the second A. Fakemon grass starter line (Whissant, Arpsant, Violinisant), after the art of the
A. Fakemon fanpage (@a.fakemon; names and types from its art): green musician birds: a round whistling chick, a
slender harpist with a leafy lyre and a tall violinist with a white crest, a long beak and a twig for a bow.

Shiny: rose-pink plumage with lilac spots.
"""
from __future__ import annotations

from _afake import ramp_of, solid_of
from _route import pal

BASE = {"green": (122, 182, 92), "green_dark": (72, 132, 72), "green_light": (182, 222, 124), "yellow": (236, 222, 110),
        "orange": (240, 142, 52), "red": (210, 72, 50), "white": (246, 246, 240), "beak": (240, 204, 124),
        "eye": (230, 220, 70), "pupil": (30, 30, 30), "leg": (232, 210, 90), "stick": (122, 84, 62),
        "claw": (220, 220, 226)}
SHINY = {"green": (222, 144, 172), "green_dark": (176, 96, 132), "green_light": (244, 192, 210), "yellow": (206, 180, 236),
         "orange": (170, 120, 230)}


def P(v):
    return pal(BASE, SHINY, v)


solid = solid_of(P)
ramp = ramp_of(P)
