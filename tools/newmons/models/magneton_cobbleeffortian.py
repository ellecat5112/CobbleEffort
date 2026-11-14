"""CobbleEffortian Magneton (Electric/Psychic), after the art of the A. Fakemon fanpage: a stack of three linked
saucers: a wide silver saucer in the middle whose open centre shows a small green eye between a yellow and a red
magnet, a domed pod with a big green eye on top and another hanging beneath, each with an antenna, and a ring of
rainbow light spinning round the whole stack.

Shiny: gold hulls with violet eyes.

Front is -z, y is up. 24 units tall; baseScale 0.72 (1.05 m). A floater.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _route import tone
from _ufo import P, antenna, eye_at, hull, ring, solid

SCALE = 0.72
HITBOX = [1.4, 1.5]
KIND = "floater"
K = 4
HEIGHT = 24
LOOK = ("three linked silver saucers: a wide middle saucer with a small eye between a yellow and a red magnet, domed "
        "eye pods above and below with antennae, and a spinning ring of rainbow light")
L = 2.0


def middlef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up" and abs(x) < 2.4 and -1.0 < z < 3.0:
        return p["dark"], None                                                # its open centre
    if face == "north":
        e = eye_at(p, x, y - (10.6 + L), 1.1)
        if e:
            return e
    if face not in ("up", "down") and abs(y - (9.4 + L)) < 0.5:
        return p["dark"], None
    return tone(p["silver_light"] if face == "up" else p["silver"], face), None


def build() -> Model:
    m = Model("magneton_cobbleeffortian")
    top = m.bone("magneton_cobbleeffortian", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10 + L, 0))
    m.round_box(bd, 0, 0, 6.4, 6.4, 8.6 + L, 11.8 + L, middlef, cut=2.2)            # the wide middle saucer
    for sx, key in ((-1, "yellow"), (1, "red")):                                   # a magnet either side of its eye
        rod(m, bd, (sx * 3.0, 12.6 + L, -1.6), (sx * 1.8, 12.6 + L, -3.2), 1.0, solid(key, glow=True), extend=0.3)
        rod(m, bd, (sx * 3.0, 12.6 + L, -1.6), (sx * 3.4, 12.6 + L, 0.4), 1.0, solid(key, glow=True), extend=0.3)
    hd = m.bone("head", bd, (0, 14 + L, 0))
    m.box(hd, -1.0, 11.6 + L, -1.0, 1.0, 13.4 + L, 1.0, solid("dark"))              # the link
    m.round_box(hd, 0, 0, 3.0, 3.0, 13.2 + L, 19.4 + L, hull(eye=(0, 16.4 + L, 1.8)), cut=1.2)   # the top pod
    antenna(m, hd, (0, 19.2 + L, 0.4), (0, 22.6 + L, 0.8), 1.4)
    m.box(bd, -0.8, 7.0 + L, -0.8, 0.8, 8.8 + L, 0.8, solid("dark"))
    m.round_box(bd, 0, 0, 2.6, 2.6, 2.4 + L, 7.2 + L, hull(eye=(0, 4.8 + L, 1.5)), cut=1.0)       # the bottom pod
    antenna(m, bd, (0, 2.6 + L, 0.0), (0, -0.4 + L, 0.0), 1.2)
    rg = m.bone("ring_orbit", bd, (0, 10 + L, 0))                                    # the spinning rainbow ring
    ring(m, rg, (0, 10.0 + L, 0), 9.6, 0.9, plane="xy", n=24)
    return m
