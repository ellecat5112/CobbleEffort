"""Ancient Beatmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the ancient warrior of thunder, a colossal beetle. A navy carapace head with a great
forked horn, two enormous navy scythe-horns sweeping down in front, a crimson body under riveted silver plates
bristling with gold spikes, translucent amber wings fanned behind and six jointed crimson legs with gold claws.
35 blocks tall.

Front is -z, y is up. 52 units tall (the horn); Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, slab_z
from _digidetail import armour, cutout, local, metal, mix, riveted, solid
from _route import pal, tone

HEIGHT = 52
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a colossal ancient beetle: a navy carapace head with a forked horn, two huge scythe-horns, a crimson body "
        "under riveted silver plates with gold spikes, amber wings and six crimson legs with gold claws")
BASE = {"navy": (40, 46, 110), "navy_dark": (14, 16, 50), "navy_light": (110, 120, 200), "red": (170, 40, 30),
        "red_dark": (90, 16, 12), "red_light": (230, 110, 80), "silver": (190, 194, 206), "silver_dark": (90, 94, 106),
        "gold": (236, 186, 50), "gold_dark": (160, 110, 20), "gold_light": (255, 236, 150),
        "wing": (250, 200, 80, 150), "wing_vein": (200, 130, 30, 220), "eye": (255, 230, 80)}
SHINY = {"navy": (30, 110, 60), "navy_dark": (10, 50, 24), "navy_light": (100, 190, 120), "red": (60, 60, 70),
         "red_dark": (30, 30, 36), "red_light": (120, 120, 134), "wing": (140, 220, 255, 150),
         "wing_vein": (60, 140, 220, 220)}


def P(v):
    return pal(BASE, SHINY, v)


NAVY = armour(P, "navy", "navy_dark", light="navy_light")
RED = armour(P, "red", "red_dark", light="red_light")
SILVER = riveted(P, "silver", "silver_dark")
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if abs(((u * 0.8 + v * 0.3) % 3.0) - 1.5) < 0.14 or abs(u - W * 0.1) < 0.2:
        return p["wing_vein"], None
    return p["wing"], None


def wing_shape(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    t = u / max(W, 1e-6)
    return abs(v / max(H, 1e-6) - 0.5) < 0.5 * math.sqrt(max(0.0, 1 - t * t)) + 0.05


def build():
    m = Model("ancientbeatmon")
    top = m.bone("ancientbeatmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    for i in range(7):                                           # the body: crimson slices under silver plates
        z0 = -10 + i * 3.4
        r = 9.0 - abs(i - 3) * 1.1
        slab_z(m, bd, 0, 18.0, z0, z0 + 3.6, r, r * 0.8, RED)
        slab_z(m, bd, 0, 18.0 + r * 0.55, z0 + 0.4, z0 + 3.2, r * 0.82, r * 0.35, SILVER)
        for sx in (-1, 1):                                       # gold spikes down the flanks
            spike(m, bd, (sx * r * 0.9, 20.0, z0 + 1.8), (sx, 0.5, 0.2), 1.6, 4.0, GOLD, tip=0.6)
    hd = m.bone("head", bd, (0, 22, -11))
    ball(m, hd, (0, 23.0, -14.0), 6.4, NAVY, layers=6, squash=1.1)
    for sx in (-1, 1):
        m.box(hd, sx * 3.0 - 1.2, 22.4, -20.2, sx * 3.0 + 1.2, 23.8, -19.0, solid(P, "eye", glow=True))
    hp = [(0, 27.0, -16.0), (0, 36.0, -20.0), (0, 44.0, -18.0), (0, 50.0, -13.0)]   # the great forked horn
    for j, (p0, p1) in enumerate(zip(hp, hp[1:])):
        rod(m, hd, p0, p1, 4 - j, NAVY, extend=0.5)
    for sx in (-1, 1):
        rod(m, hd, hp[-2], (sx * 4.0, 51.0, -16.0), 2, NAVY, extend=0.3)
        spike(m, hd, (0, 34.0, -19.6), (sx, 0.2, -0.4), 1.6, 3.6, GOLD)
    for sx in (-1, 1):                                           # the scythe horns sweeping down in front
        pts = [(sx * 5.0, 22.0, -18.0), (sx * 9.0, 30.0, -22.0), (sx * 12.0, 26.0, -28.0), (sx * 11.0, 14.0, -32.0),
               (sx * 7.0, 3.0, -30.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 3 if j < 3 else 2, NAVY, extend=0.5)
        spike(m, hd, pts[-1], (-sx * 0.5, -0.3, 0.6), 1.4, 4.0, NAVY)
        spike(m, hd, (sx * 9.0, 30.0, -22.0), (sx * 0.4, 1, 0.2), 1.6, 4.0, GOLD, tip=0.6)
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # amber wings fanned behind
        wb = m.bone(nm, bd, (sx * 4.0, 26.0, -2.0))
        for j, ang in enumerate((25, 45)):
            x0, x1 = sorted((sx * 4.0, sx * 30.0))
            m.box(wb, x0, 26.0 - 6.0, -2.0 + j * 2, x1, 26.0 + 6.0, -2.0 + j * 2, cutout(wing_shape, wingf), rotation=(-30, sx * 20, sx * ang), pivot=(sx * 4.0, 26.0, -2.0 + j * 2))
    for i, zz in enumerate((-8.0, 0.0, 8.0)):                    # six jointed legs
        for sx in (1, -1):
            nm = f"leg_{'front' if i == 0 else 'back' if i == 2 else 'mid'}_{'left' if sx > 0 else 'right'}"
            lg = m.bone(nm, top, (sx * 7.0, 14.0, zz))
            knee = (sx * 15.0, 18.0, zz - 2.0 + i * 2.0)
            foot = (sx * 19.0, 1.0, zz - 4.0 + i * 4.0)
            rod(m, lg, (sx * 7.0, 14.0, zz), knee, 3, RED, extend=0.6)
            rod(m, lg, knee, foot, 2, RED, extend=0.5)
            spike(m, lg, knee, (sx, 0.8, 0), 1.4, 3.0, GOLD)
            for d in ((sx * 0.4, -0.3, -1), (sx * 0.4, -0.3, 1)):
                spike(m, lg, foot, d, 1.2, 2.6, GOLD)
    return m
