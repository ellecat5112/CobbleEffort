"""Rust Tyranomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the ancient war machine: the Dark Tyranomon body rebuilt in corroded rust-brown armour
and cables, a huge long-barrelled cannon mounted on its back, steel claws, a red-fanged steel jaw and a green energy
core glowing in its chest. 35 blocks.

Front is -z, y is up. 46 units tall; Ultimate stage. The Dark Tyranomon body (_darktyranomon) with its own colours.
"""
from __future__ import annotations

from _boxmodel import rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, riveted, solid
from _route import pal
from _variant import clone

_T = clone("_darktyranomon", "rusttyranomon",
           base={"black": (110, 64, 40), "black_dark": (54, 28, 14), "black_light": (170, 110, 70),
                 "grey": (130, 90, 60), "grey_dark": (70, 40, 20), "grey_light": (190, 140, 90), "belly": (90, 70, 60)},
           shiny={"black": (70, 90, 110), "black_dark": (24, 36, 50), "black_light": (130, 160, 190)})
HEIGHT = 46
SCALE, HITBOX = sized(35, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a corroded rust-brown cyborg tyranosaur with a huge long-barrelled back cannon, steel claws and a glowing green chest core"
_EXTRA = {"rust": (130, 80, 50), "rust_dark": (60, 34, 16), "steel": (170, 174, 186), "steel_dark": (80, 84, 96),
          "core": (90, 240, 160), "red": (210, 40, 40)}


def P(v):
    return pal(_EXTRA, {"core": (250, 120, 60), "rust": (90, 110, 130), "rust_dark": (40, 50, 64)}, v)


_body = _T.make("rusttyranomon", x=True)


def build():
    m = _body()
    RUST = riveted(P, "rust", "rust_dark")
    STEEL = metal(P, "steel", dark="steel_dark")
    rod(m, "body", (0, 32.0, 6.0), (0, 48.0, -4.0), 4, RUST, extend=0.6)                    # back cannon
    rod(m, "body", (0, 30.0, 10.0), (0, 34.0, 4.0), 3, STEEL, extend=0.4)
    ball(m, "body", (0, 26.0, -6.6), 1.8, solid(P, "core", glow=True), layers=2)            # energy core
    for sx in (-1, 1):
        rod(m, "body", (sx * 4.0, 30.0, 4.0), (sx * 6.0, 22.0, 6.0), 1, STEEL, extend=0.2)   # cables
        for j in range(3):
            spike(m, "arm_left" if sx > 0 else "arm_right", (sx * 9.0 + (j - 1) * 1.2, 15.0, -12.0), (0, -0.4, -1),
                  1.0, 3.0, STEEL, tip=0.8)
    return m
