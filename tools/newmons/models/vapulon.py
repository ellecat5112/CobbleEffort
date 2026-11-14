"""Vapulon, the Vapor Pod Pokémon (Electric/Flying), the Nicodex's Electric type (the user's design): a sleek
metallic hummingbird shaped like a pod vape: a gunmetal pod body with a glowing teal light strip and glowing eyes, a
long black mouthpiece beak, a silver plug for a tail, whirring wings, and trailing clouds of dense vapor.

Shiny: a rose-gold pod with a pink light strip.

Front is -z, y is up. 15 units tall; baseScale 0.42 (0.4 m). A floater.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _nico import palette, puff, translucent
from _route import tone

SHINY = {"gunmetal": (210, 150, 130), "cyan": (255, 140, 200), "steel": (240, 210, 200)}
P, solid, ramp = palette(SHINY)
SCALE = 0.42
HITBOX = [0.8, 0.95]
KIND = "floater"
K = 6
HEIGHT = 15
LOOK = ("a sleek metallic hummingbird shaped like a pod vape: a gunmetal pod with a glowing light strip, a long black "
        "mouthpiece beak, a silver plug tail, whirring wings and trailing vapor")
ANIM = {"wing_flap": 34}


def podf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and abs(y - 7.0) < 0.35:
        return p["cyan"], p["cyan"]                                           # the glowing light strip
    if face in ("east", "west") and abs(y - 8.3) < 0.55 and abs(z + 2.6) < 0.55:
        return p["cyan"], p["cyan"]                                           # glowing eyes
    return tone(p["gunmetal"], face), None


def wingf(x, y, z, face, variant, **k):
    return (190, 220, 240, 150), None


def build() -> Model:
    m = Model("vapulon")
    top = m.bone("vapulon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 1.0, 2.8, 5.4, 5.0, 10.8, podf, cut=1.0)                 # the pod body
    hd = m.bone("head", bd, (0, 8, -4))
    rod(m, hd, (0, 8.6, -3.8), (0, 8.0, -10.4), 1.4, solid("black"), extend=0.3) # the mouthpiece beak
    m.box(bd, -1.0, 6.4, 5.8, 1.0, 8.4, 7.8, solid("steel"))                    # the plug tail
    for sx, side in ((-1, "left"), (1, "right")):
        w = m.bone(f"wing_{side}", bd, (sx * 2.6, 9, 0))
        x0, x1 = sorted((sx * 2.6, sx * 8.0))
        m.box(w, x0, 9.0, -1.6, x1, 9.0, 2.6, wingf, rotation=(0, 0, sx * 20), pivot=(sx * 2.6, 9.0, 0))
    for c, r in (((0.0, 3.6, 4.0), 1.6), ((1.2, 2.4, 6.6), 1.3), ((-1.0, 1.6, 8.6), 1.1)):
        puff(m, bd, c, r, translucent(P, "mist"))                                # trailing vapor
    return m
