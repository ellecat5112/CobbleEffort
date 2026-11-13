"""Shared colours for the grass starter line (Wigwoof, Wolfevel, Lycanmoon), after the art of the A. Fakemon fanpage
(names kept): a green wolf pup with a blond wig of hair, a scrappy leafy werewolf and a brawling werewolf with a vine
lasso.

Shiny: a moonlit night wolf: slate-blue fur, silver hair, violet tips, grey skin.
"""
from __future__ import annotations

from _afake import ramp_of, solid_of
from _route import pal

BASE = {"green": (126, 198, 74), "green_dark": (72, 152, 62), "green_light": (170, 222, 106), "yellow": (246, 212, 92),
        "yellow_dark": (226, 172, 58), "orange": (240, 148, 52), "orange_dark": (212, 102, 40), "red": (204, 54, 42),
        "brown": (160, 120, 92), "brown_dark": (118, 84, 62), "brown_light": (190, 152, 122), "nose": (140, 92, 62),
        "eye": (214, 78, 32), "pupil": (40, 20, 16), "white": (250, 248, 240), "claw": (236, 236, 236),
        "claw_red": (200, 50, 40), "vine": (70, 152, 112), "vine_dark": (44, 112, 82), "mouth": (196, 60, 52),
        "glove": (190, 74, 46)}
SHINY = {"green": (104, 140, 196), "green_dark": (66, 96, 156), "green_light": (146, 178, 222),
         "yellow": (222, 226, 238), "yellow_dark": (176, 182, 204), "orange": (170, 120, 220),
         "orange_dark": (126, 82, 186), "red": (98, 60, 168), "brown": (140, 138, 150), "brown_dark": (100, 98, 112),
         "brown_light": (176, 174, 186), "eye": (240, 200, 60), "glove": (110, 80, 170), "claw_red": (120, 80, 190)}


def P(v):
    return pal(BASE, SHINY, v)


solid = solid_of(P)
ramp = ramp_of(P)
