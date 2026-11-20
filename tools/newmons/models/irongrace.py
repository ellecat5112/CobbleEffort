"""Iron Grace (Grass/Fairy), the future paradox Shaymin, built from boxes after elite.4's art (the art's own name).

A Shaymin sealed inside a glass dome like a terrarium: soft green moss heaped over its back, a band of pink round
its base, a great pink Gracidea flower with dark seeds set at its side among green leaves, and a dark visor of a face
glowing with pink pixel eyes. Beneath the dome its white body walks on four little white legs striped in pink.

Shiny: blue-green moss and a golden flower.

Front is -z, y is up. 20 units tall; about 1.0 block.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import CLEAR
from _regi import ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 20
SCALE = round(1.0 * 16 / HEIGHT, 3)
HITBOX = [1.2, HEIGHT / 16]
KIND = "quadruped"
K = 3
LOOK = ("a Shaymin sealed in a glass dome: green moss over its back, a pink band, a great pink Gracidea flower among "
        "leaves, a dark visor face with pink pixel eyes and a white body on four pink-striped legs")

BASE = {"moss": (160, 206, 120), "moss_dark": (116, 160, 84), "moss_light": (200, 232, 160), "pink": (240, 140, 160),
        "pink_light": (255, 196, 210), "flower": (240, 120, 140), "flower_light": (255, 176, 190), "seed": (120, 40, 60),
        "leaf": (60, 140, 70), "leaf_dark": (36, 100, 50), "white": (246, 246, 250), "grey": (160, 160, 176),
        "visor": (50, 36, 40), "eye": (255, 120, 150), "glass": (220, 236, 250, 70), "glass_light": (255, 255, 255, 150),
        "mark": (240, 220, 140)}
SHINY = {"moss": (110, 200, 190), "moss_dark": (70, 150, 150), "moss_light": (170, 236, 226), "flower": (250, 200, 80),
         "flower_light": (255, 236, 160), "seed": (140, 90, 30)}
DC = (0.0, 11.0, 0.4)       # the dome's centre
FC = (3.0, 9.6, -6.6)       # the flower's centre (x, y, plane z)


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def mossf(x, y, z, face, variant, **k):
    """Soft moss, lighter in tufts, with two little yellow marks on its front."""
    p = P(variant)
    if face == "north" and math.hypot(x - 0.4, y - 13.4) < 0.5:
        return p["mark"], None
    n = math.sin(x * 1.1 + z * 0.7) + math.sin(z * 1.0 - y * 0.8)
    c = p["moss_light"] if n > 1.0 else (p["moss_dark"] if n < -1.1 else p["moss"])
    return lit(c, face, y, 12, 4), None


def bandf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "south", "east", "west") and (math.atan2(z, x) * 6) % 1.0 < 0.15:
        return p["pink_light"], None
    return tone(p["pink"], face), None


def glassf(x, y, z, face, variant, **k):
    """The glass dome: faint, with a bright highlight high on its front left."""
    p = P(variant)
    if face in ("north", "up") and math.hypot(x + 3.4, y - 16.0) < 1.6:
        return p["glass_light"], None
    return p["glass"], None


def visorf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - (-2.6 + sx * 1.3), y - 7.6
            if abs(dx) < 0.5 and abs(dy) < 0.9 and ((x * 3) % 1.0 < 0.7):
                return p["eye"], p["eye"]
    return lit(p["visor"], face, y, 7.6, 2.4), None


def flowerf(x, y, z, face, variant, **k):
    """The Gracidea (an xy plane): five round pink petals, lighter at their edges, dark seeds round the centre."""
    p = P(variant)
    dx, dy = x - FC[0], y - FC[1]
    r = math.hypot(dx, dy)
    a = math.atan2(dy, dx)
    R = 2.4 + 1.4 * abs(math.cos(2.5 * a))
    if r > R:
        return CLEAR
    for i in range(7):
        q = 2 * math.pi * i / 7
        if math.hypot(dx - math.cos(q) * 1.4, dy - math.sin(q) * 1.4) < 0.3:
            return p["seed"], None
    if math.hypot(dx, dy) < 0.4:
        return p["seed"], None
    return (p["flower_light"] if r > R - 0.5 else p["flower"]), None


def leaff(cx, cy, ang, L=4.0, W=1.4):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        a = math.radians(ang)
        along = (x - cx) * math.cos(a) + (y - cy) * math.sin(a)
        across = -(x - cx) * math.sin(a) + (y - cy) * math.cos(a)
        if not 0 <= along <= L:
            return CLEAR
        w = W * math.sin(math.pi * along / L)
        if abs(across) > w:
            return CLEAR
        return (p["leaf_dark"] if abs(across) < 0.2 else p["leaf"]), None
    return s


def build() -> Model:
    m = Model("irongrace")
    top = m.bone("irongrace", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7.0, 0))
    ellipsoid(m, bd, 0, 6.6, 0.4, 6.6, 3.0, 6.6, solid("white"), step=1)            # white body
    m.round_box(bd, 0, 0.4, 6.8, 6.8, 8.0, 9.6, bandf, cut=2)                        # pink band
    ellipsoid(m, bd, 0, 11.6, 0.8, 6.2, 4.6, 6.2, mossf, step=1)                     # heaped moss
    for i in range(7):                                                           # mossy tufts on top
        a = 2 * math.pi * i / 7
        ellipsoid(m, bd, math.cos(a) * 3.4, 15.0, 0.8 + math.sin(a) * 3.4, 1.8, 1.4, 1.8, mossf, step=1)
    hd = m.bone("head", bd, (-2.6, 7.6, -5.6))
    ellipsoid(m, hd, -2.6, 7.6, -5.4, 2.8, 2.4, 2.0, visorf, step=1)                 # dark visor face
    m.box(bd, FC[0] - 4.0, FC[1] - 4.0, FC[2] - 0.6, FC[0] + 4.0, FC[1] + 4.0, FC[2] - 0.6, flowerf)   # Gracidea
    for ang, cx, cy in ((20, 6.2, 9.6), (160, -0.2, 10.4), (-60, 4.0, 6.4)):
        m.box(bd, cx - 4.4, cy - 4.4, FC[2] - 0.2, cx + 4.4, cy + 4.4, FC[2] - 0.2, leaff(cx, cy, ang))
    ellipsoid(m, bd, DC[0], DC[1], DC[2], 9.4, 9.0, 9.4, glassf, step=3)              # the glass dome
    for nm, sx, z in (("leg_front_left", 1, -3.4), ("leg_front_right", -1, -3.4), ("leg_back_left", 1, 4.0),
                      ("leg_back_right", -1, 4.0)):
        lg = m.bone(nm, top, (sx * 3.6, 4.0, z))
        rod(m, lg, (sx * 3.6, 4.4, z), (sx * 4.4, 0.6, z - 0.4), 2.0, solid("white"), extend=0.4)
        m.box(lg, sx * 4.4 - 0.9, 0, z - 1.6, sx * 4.4 + 0.9, 0.8, z + 0.6, solid("grey"))
        m.box(lg, sx * 4.4 - 1.05, 2.0, z - 1.4, sx * 4.4 + 1.05, 2.5, z + 0.6, solid("pink"))
    return m
