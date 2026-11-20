"""Proto-Dialga (Rock/Dragon), the ancient paradox Dialga, built from boxes after the art the user shared (the art's
own name; artist not named).

A Dialga of living blue crystal, its body traced with glowing cyan veins and flecked with white stars like the night
sky. Silver armour frames a great glowing diamond on its chest and plates its shoulders, legs and feet; long blades
of pale crystal, striped white, fan up and back from its shoulders like wings, and more crystal fins run along its
neck and spike its tail. Its long head carries a silver crest blade.

Shiny: green crystal with golden veins.

Front is -z, y is up. 55 units tall (to the crystal blades); about 6.0 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _dialga import BODY_Y, dialga
from _pgen1 import stars
from _regi import lit
from _route import mix, pal, tone

HEIGHT = 55
SCALE = round(6.0 * 16 / HEIGHT, 3)
HITBOX = [3.0, HEIGHT / 16]
KIND = "quadruped"
K = 3
LOOK = ("a Dialga of glowing blue crystal veined in cyan and flecked with stars, silver armour round a glowing "
        "chest diamond and long striped crystal blades fanning from its shoulders like wings")

BASE = {"crystal": (96, 172, 238), "crystal_dark": (46, 96, 190), "crystal_light": (176, 226, 255),
        "vein": (130, 244, 255), "star": (255, 255, 255), "silver": (196, 204, 222), "silver_dark": (122, 132, 160),
        "core": (220, 250, 255), "core_rim": (120, 220, 255), "eye": (200, 250, 255), "blade": (150, 210, 255),
        "blade_stripe": (236, 248, 255), "blade_edge": (70, 140, 226)}
SHINY = {"crystal": (90, 200, 150), "crystal_dark": (40, 130, 100), "crystal_light": (170, 246, 210),
         "vein": (255, 220, 110), "core_rim": (255, 220, 110), "blade": (150, 236, 196),
         "blade_edge": (50, 160, 110)}


def P(v):
    return pal(BASE, SHINY, v)


def vein(x, y, z):
    """Wandering glowing lines over the crystal."""
    a = math.sin(x * 0.55 + math.sin(y * 0.33) * 1.7 + z * 0.2)
    b = math.sin(z * 0.45 + math.sin(x * 0.4 + y * 0.2) * 1.5 - y * 0.25)
    return abs(a + b * 0.8) < 0.11


def crystalf(x, y, z, face, variant, **k):
    p = P(variant)
    if stars(x, y, z, face, cell=1.6, r=0.25, prob=0.3):
        return p["star"], p["star"]
    if vein(x, y, z):
        return p["vein"], p["vein"]
    if face == "up":
        return p["crystal_light"], None
    return lit(p["crystal"], face, y, BODY_Y, 10), None


def silverf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up":
        return mix(p["silver"], (255, 255, 255), 0.25), None
    return tone(p["silver"] if face != "down" else p["silver_dark"], face), None


def shinf(x, y, z, face, variant, **k):
    """A lower leg: crystal with a silver plate down its front (a downward rod shows its local "up" face to the
    front)."""
    if face == "up":
        return silverf(x, y, z, face, variant)
    return crystalf(x, y, z, face, variant)


def coref(x, y, z, face, variant, **k):
    p = P(variant)
    r = math.hypot(x, (y - BODY_Y - 0.4) * 0.75)
    c = p["core"] if r < 1.6 else p["core_rim"]
    return c, c


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and math.hypot(z + 18.6, y - (BODY_Y + 26.4)) < 0.8:
        return p["eye"], p["eye"]
    return crystalf(x, y, z, face, variant)


def bladef(x, y, z, face, variant, box=None, **k):
    """A crystal blade: translucent pale blue, striped white along its length, darker at its edges (rods: z runs back
    from the root, y across its broad face)."""
    p = P(variant)
    cy = box.lo[1] + box.size[1] / 2
    v = (y - cy) / (box.size[1] / 2)
    if abs(v) > 0.8:
        return p["blade_edge"], None
    if abs(v - 0.2) < 0.18:
        return p["blade_stripe"], p["blade_stripe"]
    return p["blade"], None


def build() -> Model:
    m = Model("protodialga")
    mats = {"skin": crystalf, "belly": crystalf, "neck": crystalf, "head": headf, "crest": silverf,
            "armour": silverf, "plate": silverf, "leg_upper": crystalf, "leg_lower": shinf, "foot": silverf,
            "claw": silverf, "tail": crystalf, "core": coref}
    a = dialga(m, mats, "protodialga")
    bd = a["body"]
    for nm, sx in (("wing_left", 1), ("wing_right", -1)):                        # crystal blades fanned like wings
        wg = m.bone(nm, bd, (sx * 3.6, BODY_Y + 6.0, -4.0))
        for i in range(5):
            ang = math.radians(28 + i * 15)
            d = (sx * (0.55 - 0.06 * i), math.cos(ang) * 1.2, math.sin(ang))
            root = (sx * (3.6 + 0.4 * i), BODY_Y + 6.0 - 0.4 * i, -4.0 + 1.6 * i)
            L = 22.0 + 6.0 * math.sin((i + 0.5) / 5 * math.pi)
            n = math.sqrt(sum(v * v for v in d))
            mid = tuple(r + q / n * L * 0.62 for r, q in zip(root, d))
            end = tuple(r + q / n * L for r, q in zip(root, d))
            rod(m, wg, root, mid, 1.0, bladef, extend=0.4, t2=5.0)
            rod(m, wg, mid, end, 1.0, bladef, extend=0.4, t2=3.4)
        spike(m, wg, (sx * 6.0, BODY_Y + 5.0, -6.0), (sx * 1, 0.4, -0.2), 2.4, 5.0, silverf, tip=1.0)
    for i, f in enumerate((0.25, 0.5, 0.75)):                                   # crystal fins along the neck
        nk = a["neck"]
        y, z = BODY_Y + 6.0 + 15.0 * f, -12.0 - 3.0 * f
        spike(m, nk, (0, y, z + 2.0), (0, 0.3, 1), 1.0, 3.6 - i * 0.6, bladef, tip=0.6)
    for i, p in enumerate(a["tail_pts"][2:-1:2]):                               # spikes along the tail
        for sx in (-1, 1):
            spike(m, a["tail"], p, (sx * 1, 0.6, 0.3), 1.2, 3.0, bladef, tip=0.6)
    return m
