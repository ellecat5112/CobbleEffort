"""BlitzGreymon (Steel/Fire; a Digimon of the CobbleEffort: Digital crossover, built after the official art): a
towering red war-machine: crimson armour plates with grey joints, two huge shoulder cannon pods, Gatling forearms with
clusters of barrels, a crested red helmet with a yellow visor, three-clawed grey feet and a thruster pack glowing on
its back. 35 blocks tall.

Front is -z, y is up. 46 units tall; baseScale 12.4 (35 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import P, claw_fan, solid
from _route import tone
from _scarab import slab_xy

SCALE = 12.4
HITBOX = [1.6, 2.85]
KIND = "biped"
K = 3
HEIGHT = 46
ANIM = {"leg_amp": 10}
LOOK = ("a towering red war-machine: crimson armour with grey joints, two huge shoulder cannon pods, Gatling forearms, a "
        "crested red helmet with a yellow visor, three-clawed grey feet and a glowing thruster pack")


def armour(key="mech", line_every=4.2, seed=0.0):
    """Crimson armour plating: darker panel seams, a lighter rim on the top faces."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        a = {"up": x + z, "down": x + z, "north": x + y, "south": x + y, "east": z + y * 0.3, "west": z + y * 0.3}[face]
        if (a + seed) % line_every < 0.35:
            return tone(p[key + "_dark"], face), None
        if face == "up":
            return tone(p[key + "_light"], face), None
        return tone(p[key], face), None
    return s


def podf(x, y, z, face, variant, box=None, **k):
    """A shoulder cannon pod: crimson, three dark muzzles on its front face."""
    p = P(variant)
    if face == "north":
        cx = box.lo[0] + box.size[0] / 2
        cy = box.lo[1] + box.size[1] / 2
        for ox, oy in ((-1.8, 1.2), (1.8, 1.2), (0, -1.8)):
            d = math.hypot(x - cx - ox, y - cy - oy)
            if d < 1.3:
                return p["pupil"], None
            if d < 1.7:
                return tone(p["joint"], face), None
    return armour(seed=1.3)(x, y, z, face, variant)


def visorf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and 38.6 < y < 39.6 and abs(x) < 2.6:
        return p["blade"], p["blade"]                                   # the glowing yellow visor
    return armour(seed=0.7)(x, y, z, face, variant)


def build() -> Model:
    m = Model("blitzgreymon")
    top = m.bone("blitzgreymon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 1))
    m.round_box(bd, 0, 1.0, 4.4, 3.6, 18.0, 23.0, solid("joint"), cut=1.2)        # the grey waist
    m.round_box(bd, 0, 0.5, 6.5, 5.0, 22.5, 33.5, armour(), cut=2.0)              # the armoured chest
    m.box(bd, -3.0, 25.0, -5.0, 3.0, 30.0, -4.2, solid("mech_light"))
    m.box(bd, -4.5, 24.0, 5.0, 4.5, 33.0, 9.0, solid("joint"))                    # the thruster pack
    for sx in (-1, 1):
        rod(m, bd, (sx * 2.4, 25.0, 9.0), (sx * 2.4, 22.0, 11.5), 2.4, solid("flame", glow=True), extend=0.2)
    hd = m.bone("head", bd, (0, 34, -1))
    m.round_box(hd, 0, -1.5, 3.4, 3.6, 33.5, 41.0, visorf, cut=1.2)
    m.box(hd, -2.0, 33.5, -6.6, 2.0, 36.5, -4.0, solid("joint"))                 # the grey jaw
    spike(m, hd, (0, 40.5, -3.5), (0, 1, 0.4), 2.2, 5.5, solid("metal_light"), tip=0.5)   # crest
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.6, 40.0, -1.0), (sx * 0.8, 1, 0.6), 1.6, 4.5, solid("metal_light"), tip=0.4)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        a = m.bone(nm, bd, (sx * 8.0, 31.0, 0.0))
        slab_xy(m, a, sx * 11.5, 36.0, 4.8, 4.6, -8.0, 9.0, podf, cut=2)          # the shoulder cannon pod
        rod(m, a, (sx * 8.0, 31.0, 0.0), (sx * 10.0, 24.5, -2.0), 3.2, solid("joint"), extend=0.6)
        slab_xy(m, a, sx * 10.5, 22.0, 3.4, 3.4, -10.0, 1.5, armour(seed=2.1), cut=1)   # the Gatling forearm
        for ox, oy in ((-1.2, 1.2), (1.2, 1.2), (-1.2, -1.2), (1.2, -1.2)):
            rod(m, a, (sx * 10.5 + ox, 22.0 + oy, -10.0), (sx * 10.5 + ox, 22.0 + oy, -14.0), 1.2,
                solid("cannon_dark"), extend=0.0)
        claw_fan(m, a, (sx * 10.5, 18.8, -7.0), (0, -1, -0.5), 3, 1.0, 3.0, 1.4, key="metal")
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.2, 19.0, 1.0))
        m.round_box(lg, sx * 4.4, 1.0, 3.2, 3.6, 11.5, 20.0, armour(seed=sx), cut=1.2)   # thigh armour
        m.round_box(lg, sx * 4.4, 0.5, 2.2, 2.2, 9.0, 12.5, solid("joint"), cut=0.6)     # knee
        m.round_box(lg, sx * 4.4, 0.5, 2.8, 3.2, 2.5, 9.5, armour(seed=sx + 2), cut=1.0)  # shin
        spike(m, lg, (sx * 4.4, 10.5, -2.4), (0, 0.6, -1), 2.0, 3.0, solid("mech_light"), tip=0.5)   # knee spike
        m.box(lg, sx * 4.4 - 2.6, 0.0, -3.0, sx * 4.4 + 2.6, 2.6, 4.0, solid("joint"))
        claw_fan(m, lg, (sx * 4.4, 0.9, -3.0), (0, -0.15, -1), 3, 1.2, 3.4, 1.7, key="metal")
        spike(m, lg, (sx * 4.4, 1.2, 4.0), (0, -0.2, 1), 1.4, 2.6, solid("metal"), tip=0.4)   # heel claw
    return m
