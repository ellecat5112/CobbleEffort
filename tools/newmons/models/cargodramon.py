"""Cargodramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the transport-plane dragon. A long navy fuselage whose open sides show a white ribcage, yellow
hazard panels, a tan dragon-skull nose with a jaw full of teeth and red spines, a big front propeller, two huge
engine nacelles with rotors on its back, a tail with fins and red-striped blades, and a gun turret under its chin.
25 blocks long.

Front is -z, y is up. 30 units tall, 62 long; Perfect stage (floats).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import slab_z
from _digidetail import armour, metal, riveted, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(25 * 30 / 62, HEIGHT, 3.4)
KIND = "floater"
K = 3
LOOK = ("a long navy transport-plane dragon with a ribcage fuselage, a tan dragon-skull nose with teeth, a front "
        "propeller, two engine nacelles with rotors and a finned tail")
BASE = {"navy": (40, 50, 90), "navy_dark": (16, 20, 44), "navy_light": (90, 110, 170), "bone": (226, 214, 180),
        "bone_dark": (160, 140, 100), "rib": (240, 240, 244), "yellow": (240, 210, 40), "red": (210, 40, 40),
        "steel": (180, 184, 196), "steel_dark": (70, 74, 86), "black": (24, 24, 30), "tooth": (250, 250, 246),
        "eye": (250, 200, 40)}
SHINY = {"navy": (110, 120, 60), "navy_dark": (50, 56, 20), "navy_light": (170, 180, 110)}


def P(v):
    return pal(BASE, SHINY, v)


NAVY = riveted(P, "navy", "navy_dark", light="navy_light")
BONE = armour(P, "bone", "bone_dark")
STEEL = metal(P, "steel", dark="steel_dark")
CY = 14.0


def hullf(x, y, z, face, variant, box=None, **k):
    """Navy hull; the sides open onto a white ribcage behind the cockpit, with yellow hazard panels."""
    p = P(variant)
    if face in ("east", "west") and -8.0 < z < 14.0 and abs(y - CY) < 3.6:
        return tone(p["rib"] if z % 2.4 < 1.0 else p["black"], face), None
    if face in ("east", "west") and 14.0 < z < 18.0 and abs(y - CY - 1.0) < 1.2:
        return tone(p["yellow"] if (z * 2) % 2 < 1 else p["black"], face), None
    return NAVY(x, y, z, face, variant, box=box, **k)


def bladef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["red"] if abs(y - round(y / 6) * 6) < 0.8 and abs(x) > 4 else p["black"], face), None


def build():
    m = Model("cargodramon")
    top = m.bone("cargodramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    for i in range(12):                                                       # the fuselage
        z0 = -18.0 + i * 3.6
        r = 6.0 if i < 9 else 6.0 - (i - 8) * 1.2
        slab_z(m, bd, 0, CY, z0 - 0.2, z0 + 3.8, r, r * 0.9, hullf)
    hd = m.bone("head", bd, (0, CY, -18))                                     # dragon-skull nose
    m.round_box(hd, 0, -22.0, 4.6, 4.0, CY - 2.0, CY + 4.4, BONE, cut=1)
    m.box(hd, -3.4, CY - 1.0, -30.0, 3.4, CY + 2.4, -24.0, BONE)
    jw = m.bone("jaw", hd, (0, CY - 2.0, -20))
    m.box(jw, -3.0, CY - 4.0, -29.0, 3.0, CY - 2.0, -20.0, BONE, rotation=(16, 0, 0), pivot=(0, CY - 2.0, -20.0))
    for i in range(5):
        for sx in (-1, 1):
            spike(m, hd, (sx * 2.8, CY - 1.0, -29.0 + i * 1.4), (0, -1, 0), 0.8, 1.4, solid(P, "tooth"))
        spike(m, hd, (0, CY + 4.0, -22.0 + i * 1.6), (0, 1, 0.4), 1.2, 2.0, solid(P, "red"))
    for sx in (-1, 1):
        m.box(hd, sx * 4.6 - 0.2, CY + 1.6, -24.4, sx * 4.6 + 0.2, CY + 2.6, -23.0, solid(P, "eye", glow=True))
    sp = m.bone("spin_prop", hd, (0, CY + 1.0, -30.4))                       # front propeller
    m.round_box(sp, 0, -30.8, 1.2, 0.8, CY, CY + 2.0, STEEL, cut=1)
    for ang in (0, 120, 240):
        m.box(sp, -0.8, CY + 1.0, -31.2, 0.8, CY + 13.0, -30.8, bladef, rotation=(0, 0, ang), pivot=(0, CY + 1.0, -31.0))
    # two engine nacelles with rotors on the back
    for sx in (-1, 1):
        nc = (sx * 8.0, CY + 9.0, -2.0)
        rod(m, bd, (sx * 3.0, CY + 5.0, -2.0), nc, 2, NAVY, extend=0.4)
        slab_z(m, bd, nc[0], nc[1], -10.0, 6.0, 3.4, 3.4, NAVY)
        m.box(bd, nc[0] - 2.0, nc[1] - 2.0, -11.2, nc[0] + 2.0, nc[1] + 2.0, -10.0, solid(P, "black"))
        rb = m.bone(f"spin_rotor_{'left' if sx > 0 else 'right'}", bd, (nc[0], nc[1], -11.0))
        for ang in (0, 120, 240):
            m.box(rb, nc[0] - 0.6, nc[1], -11.4, nc[0] + 0.6, nc[1] + 12.0, -11.0, bladef, rotation=(0, 0, ang),
                  pivot=(nc[0], nc[1], -11.2))
    # tail fins
    for sx in (-1, 1):
        m.box(bd, min(sx * 2.0, sx * 10.0), CY + 1.0, 22.0, max(sx * 2.0, sx * 10.0), CY + 1.6, 28.0, NAVY)
    m.box(bd, -0.4, CY + 2.0, 21.0, 0.4, CY + 12.0, 28.0, NAVY)
    m.box(bd, -0.45, CY + 9.0, 25.0, 0.45, CY + 10.0, 28.0, solid(P, "red"))
    m.box(bd, -2.0, CY - 7.6, -14.0, 2.0, CY - 5.0, -10.0, STEEL)              # chin gun turret
    rod(m, bd, (0, CY - 6.4, -14.0), (0, CY - 6.4, -19.0), 1, solid(P, "black"), extend=0)
    return m
