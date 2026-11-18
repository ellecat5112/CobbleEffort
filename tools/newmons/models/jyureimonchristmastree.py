"""Jyureimon (Christmas Tree) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): Jyureimon dressed for Christmas, a tiered fir crowned with a golden star and a red bow, hung with
coloured baubles and a golden bell, with wrapped presents round its roots. 35 blocks tall.

Front is -z, y is up. 44 units tall; Ultimate stage. Built by _jyureimon.make(xmas=True).
"""
from __future__ import annotations

from _digi import sized
from _jyureimon import make

HEIGHT = 44
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 0}
LOOK = "a tiered festive fir tree with a golden star, a red bow, coloured baubles and presents round its roots"
build = make("jyureimonchristmastree", xmas=True)
