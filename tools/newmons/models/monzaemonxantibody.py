"""Monzaemon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a giant patchwork teddy bear of tan and brown felt with pink heart paw pads and ears, a red bow, a halo and bubbles of hearts floating round it. 25 blocks tall.

Front is -z, y is up. 54 units tall; Perfect stage. Built by _monzaemon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _monzaemon import make

HEIGHT = 54
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a giant patchwork teddy bear of tan and brown felt with pink heart paw pads and ears, a red bow, a halo and bubbles of hearts floating round it"
build = make("monzaemonxantibody", x=True)
