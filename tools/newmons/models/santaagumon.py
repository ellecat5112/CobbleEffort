"""Santa Agumon (a Digimon of the CobbleEffort: Digital crossover; built after the official art on wikimon.net): Agumon
in a red Santa hat with a white fur brim and a white pompom flopping to one side. 1 block.

Front is -z, y is up. 28 units tall; Child stage. The Agumon body (_agumon.build_agumon) plus the hat.
"""
from __future__ import annotations

from _agumon import build_agumon
from _boxmodel import rod
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, fur
from _route import pal

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 1.3)
KIND = "biped"
K = 5
LOOK = "Agumon in a red Santa hat with a white fur brim and a white pompom"
_BASE = {"red": (210, 30, 40), "red_dark": (130, 10, 16), "white": (250, 250, 252), "white_dark": (200, 200, 210)}
_SHINY = {"red": (40, 140, 70), "red_dark": (14, 80, 30)}


def P(v):
    return pal(_BASE, _SHINY, v)


def build():
    m = build_agumon("santaagumon")
    RED = fabric(P, "red", "red_dark", axis="y", period=2.0)
    FUR = fur(P, "white", "white_dark", length=0.8)
    m.round_box("head", 0, -1.8, 3.8, 4.0, 21.4, 23.0, FUR, cut=1)                         # fur brim
    m.round_box("head", 0, -1.4, 3.2, 3.4, 23.0, 25.0, RED, cut=1)
    rod(m, "head", (0, 25.0, -1.4), (1.6, 27.0, 0.6), 2, RED, extend=0.4)
    rod(m, "head", (1.6, 27.0, 0.6), (4.0, 25.6, 2.6), 1, RED, extend=0.3, t2=2)
    ball(m, "head", (4.4, 25.0, 3.0), 1.2, FUR, layers=2)                                 # pompom
    return m
