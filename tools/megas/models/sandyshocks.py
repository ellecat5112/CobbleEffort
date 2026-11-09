"""Mega Sandy Shocks, hand-built from boxes in Cobblemon's style.

Sandy Shocks (official art: an ancient Magneton: three grey spheres, each with a yellow eye and screws, one on top
and two below, with U-shaped magnet arms and legs (grey, red and blue tips) clumped with black spiky iron sand) as a
mega: bigger magnet arches crackling with glowing electric arcs, more iron-sand spikes, and a spiked crown of iron
sand on its top sphere.

Front is -z, y is up. ~44 units tall; baseScale 1.0 (about 2.75 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, spike

SCALE = 1.0
HITBOX = [2.2, 2.8]
LOOK = ("three grey Magneton spheres with yellow eyes and screws, great magnet arches with red and blue tips crackling "
        "with glowing yellow arcs, black iron-sand spikes everywhere and a spiked iron-sand crown")
KIND = "biped"
ANIM = {"leg_amp": 12}

BASE = {
    "metal": (196, 204, 214), "metal_light": (222, 228, 236), "metal_dark": (150, 158, 170), "screw": (120, 126, 138),
    "eye": (246, 220, 70), "pupil": (40, 36, 30), "magnet": (176, 182, 194), "red": (214, 60, 60), "blue": (60, 120, 220),
    "sand": (42, 42, 48), "sand_light": (76, 76, 86), "spark": (255, 240, 110),
}
SHINY = {"metal": (214, 196, 170), "metal_light": (236, 222, 200), "metal_dark": (176, 156, 128), "magnet": (200, 180, 150),
         "sand": (110, 70, 40), "sand_light": (150, 100, 60), "spark": (140, 230, 255)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def sphere(cx, cy, cz):
    """A sphere shader: metal with a yellow eye on the front and screws on the sides."""
    def s(x, y, z, face, variant, **k):
        P = palette(variant)
        if face == "north":
            dx, dy = x - cx, y - cy
            if dx * dx + dy * dy <= 6.5:
                if dx * dx + dy * dy <= 1.2:
                    return P["pupil"]
                return P["eye"], P["eye"]
        if face in ("east", "west") and abs(y - cy) <= 1 and abs(z - cz) <= 1:
            return P["screw"]
        if face == "down":
            return P["metal_dark"]
        return P["metal_light"] if face == "up" else P["metal"]
    return s


def magnet(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["metal_dark"] if face == "down" else P["magnet"]


def red(x, y, z, face, variant, **k):
    return palette(variant)["red"]


def blue(x, y, z, face, variant, **k):
    return palette(variant)["blue"]


def sand(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["sand_light"] if face in ("up", "north") else P["sand"]


def spark(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["spark"], P["spark"]


def ball(m, bone, cx, cy, cz, r):
    """A sphere from three crossed boxes."""
    sh = sphere(cx, cy, cz)
    m.box(bone, cx - r, cy - r + 1, cz - r + 1, cx + r, cy + r - 1, cz + r - 1, sh)
    m.box(bone, cx - r + 1, cy - r, cz - r + 1, cx + r - 1, cy + r, cz + r - 1, sh)
    m.box(bone, cx - r + 1, cy - r + 1, cz - r, cx + r - 1, cy + r - 1, cz + r, sh)


def sand_clump(m, bone, cx, cy, cz, n=5, size=4):
    """A spiky clump of iron sand."""
    m.box(bone, cx - 1.5, cy - 1.5, cz - 1.5, cx + 1.5, cy + 1.5, cz + 1.5, sand)
    for i in range(n):
        a = 2 * math.pi * i / n
        d = (math.cos(a), 0.6 + 0.4 * math.sin(a * 2), math.sin(a))
        spike(m, bone, (cx, cy, cz), d, 2, size, sand)


def u_magnet(m, bone, top, down, side, length, tip_red):
    """A U magnet hanging from `top`: two prongs `length` long joined by an arch, coloured tips."""
    x, y, z = top
    for dz in (-3, 3):
        m.box(bone, x - 1.5, y - length, z + dz - 1.5, x + 1.5, y, z + dz + 1.5, magnet)
        m.box(bone, x - 1.5, y - length - 2, z + dz - 1.5, x + 1.5, y - length, z + dz + 1.5, red if (dz < 0) == tip_red else blue)
    m.box(bone, x - 1.5, y, z - 4.5, x + 1.5, y + 3, z + 4.5, magnet)


def build() -> Model:
    m = Model("sandyshocks_mega")
    root = m.bone("sandyshocks_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 20, 0))
    # the two lower spheres, joined
    ball(m, body, 6, 20, 0, 6)
    ball(m, body, -6, 20, 0, 6)
    m.box(body, -2, 18, -2, 2, 22, 2, magnet)
    # crackling arcs between them and up to the head
    for (a, b) in (((0, 26, -3), (2, 29, -4)), ((2, 29, -4), (-1, 32, -3)), ((-6, 14, -6), (6, 14, -6))):
        chain(m, body, [a, b], [1], spark)

    head = m.bone("head", body, (0, 30, 0))
    ball(m, head, 0, 34, 0, 6)
    m.box(head, -1.5, 26, -1.5, 1.5, 29, 1.5, magnet)
    # the iron-sand crown
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        spike(m, head, (4 * math.sin(a), 39, -4 * math.cos(a)), (math.sin(a) * 0.6, 1, -math.cos(a) * 0.6), 3, 6, sand, tip=1)
    sand_clump(m, head, 0, 41, 0, n=6, size=5)

    # arms: big magnets out to the sides, iron sand on the ends
    for sgn, nm in ((1, "arm_left"), (-1, "arm_right")):
        arm = m.bone(nm, body, (sgn * 10, 26, 0))
        chain(m, arm, [(sgn * 9, 26, 0), (sgn * 15, 31, 0), (sgn * 21, 31, 0), (sgn * 24, 26, 0)], [3, 3, 3], magnet)
        m.box(arm, sgn * 24 - 1.5, 21, -1.5, sgn * 24 + 1.5, 26, 1.5, red if sgn > 0 else blue)
        sand_clump(m, arm, sgn * 24, 20, 0)
        chain(m, arm, [(sgn * 15, 33, -1), (sgn * 19, 36, -1), (sgn * 22, 33, -1)], [1, 1], spark)

    # legs: great U magnets, sand round the feet
    for sgn, nm in ((1, "leg_front_left"), (-1, "leg_front_right")):
        leg = m.bone(nm, root, (sgn * 7, 15, 0))
        u_magnet(m, leg, (sgn * 7, 13, 0), True, sgn, 11, sgn > 0)
        for dz in (-3, 3):
            sand_clump(m, leg, sgn * 7, 1, dz, n=4, size=3)
    return m
