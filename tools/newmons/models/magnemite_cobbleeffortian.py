"""CobbleEffortian Magnemite (Electric/Psychic), after the art of the A. Fakemon fanpage: a little silver flying saucer
with a domed top, one big glowing green cyclops eye, an antenna tipped with a ball, a dark underside and a yellow
tractor beam shining down from it.

Shiny: a gold saucer with a violet eye.

Front is -z, y is up. 14 units tall; baseScale 0.5 (0.45 m). A floater.
"""
from __future__ import annotations

from _boxmodel import Model
from _ufo import antenna, beam, hull, solid

SCALE = 0.5
HITBOX = [0.9, 0.9]
KIND = "floater"
K = 5
HEIGHT = 14
LOOK = "a little silver flying saucer with a domed top, one big glowing green eye, an antenna and a yellow tractor beam"
L = 4.0


def build() -> Model:
    m = Model("magnemite_cobbleeffortian")
    top = m.bone("magnemite_cobbleeffortian", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4 + L, 0))
    m.round_box(bd, 0, 0, 5.4, 5.4, 2.6 + L, 4.0 + L, hull(band=(2.6 + L, 3.2 + L), lights=(0, 8, 5)), cut=1.8)   # the saucer
    m.round_box(bd, 0, 0, 2.8, 2.8, 1.2 + L, 2.8 + L, solid("dark"), cut=0.8)                                  # dark underside
    m.round_box(bd, 0, 0, 3.4, 3.2, 3.8 + L, 8.6 + L, hull(eye=(0, 6.2 + L, 1.9)), cut=1.2)                   # the dome
    antenna(m, bd, (0, 8.4 + L, 0.4), (0, 11.6 + L, 0.6), 1.4)
    beam(m, bd, 0, 0, 0.0, 1.4 + L, 1.4, 3.0)                                                                  # tractor beam
    return m
