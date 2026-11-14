"""Shared colours for the second A. Fakemon water starter line (Brenkey, Splakey, Slackey), after the art of the A.
Fakemon fanpage (@a.fakemon; names and types from its art): blue-and-white water monkeys with orange faces, hands and
feet: a squat little monkey with a bamboo straw, a lean splashing monkey in a headband and a big lazy brute lounging
in a swim ring.

Shiny: teal-green fur and golden faces.
"""
from __future__ import annotations

from _afake import ramp_of, solid_of
from _route import pal

BASE = {"blue": (92, 162, 216), "blue_dark": (40, 72, 124), "blue_light": (172, 214, 238), "white": (244, 248, 252),
        "orange": (238, 140, 70), "orange_light": (248, 190, 130), "cream": (250, 232, 204), "pupil": (40, 40, 50),
        "eye": (60, 60, 70), "bamboo": (152, 192, 110), "bamboo_dark": (110, 150, 80), "leaf": (110, 170, 80),
        "mouth": (120, 60, 50), "red_eye": (190, 70, 60)}
SHINY = {"blue": (82, 190, 150), "blue_dark": (30, 100, 90), "blue_light": (170, 230, 206), "orange": (238, 196, 76),
         "orange_light": (250, 222, 140)}


def P(v):
    return pal(BASE, SHINY, v)


solid = solid_of(P)
ramp = ramp_of(P)
