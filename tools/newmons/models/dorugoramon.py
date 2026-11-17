"""DORUgoramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the dragon knight of the DORU line. An upright armoured dragon in gleaming silver plate over a
dark violet body, a horned dragon-helm with violet eyes, sweeping black-and-gold horn blades, great dark violet wings
ribbed with silver, steel talon feet, a spiked tail ending in a crescent axe-blade, and two rings of golden flame
circling its body. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digibody import dome, humanoid
from _digidetail import armour, cutout, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 3.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("an upright silver-armoured dragon knight over a dark violet body, with a horned helm, black-and-gold horn "
        "blades, great violet wings ribbed with silver, a crescent axe tail and two rings of golden flame")
BASE = {"silver": (220, 224, 236), "silver_dark": (110, 114, 128), "silver_light": (255, 255, 255),
        "violet": (70, 50, 120), "violet_dark": (24, 16, 50), "violet_light": (140, 120, 200), "black": (30, 28, 36),
        "gold": (240, 196, 60), "eye": (180, 120, 255), "flame": (255, 190, 60, 210), "flame_core": (255, 245, 190, 235)}
SHINY = {"violet": (150, 40, 50), "violet_dark": (70, 10, 14), "violet_light": (230, 120, 120)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "silver", "silver_dark", light="silver_light", trim="gold", trim_w=0.25)
BODY = skin(P, "violet", dark="violet_dark", light="violet_light")
SILVER = metal(P, "silver", dark="silver_dark")


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return tone(p["violet"] if (u % 4.0) > 0.5 else p["silver"], face), None


def build():
    m = Model("dorugoramon")
    mats = {"skin": BODY, "chest": PLATE, "abs": BODY, "pelvis": PLATE, "neck": BODY, "deltoid": PLATE,
            "upper_arm": BODY, "forearm": PLATE, "hand": PLATE, "finger": PLATE, "claw": SILVER, "thigh": PLATE,
            "knee": PLATE, "shin": PLATE, "calf": PLATE, "foot": PLATE, "talon": SILVER}
    a = humanoid(m, mats, bulk=1.1, arm_bulk=1.1, leg_bulk=1.15, claws=True, talons=True, digitigrade=True,
                 name="dorugoramon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.4, 2.8, 4.0, 54.0, 60.0, PLATE, cut=1)                        # dragon-helm
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.6, sx * 2.9), 57.4, -5.5, max(sx * 1.6, sx * 2.9), 58.2, -5.3, solid(P, "eye", glow=True))
        for j, (lift, reach) in enumerate(((10.0, 6.0), (6.0, 10.0))):                 # horn blades
            pts = [(sx * 2.4, 59.0, 0.0), (sx * (3.0 + reach * 0.5), 59.0 + lift * 0.6, 4.0),
                   (sx * (3.0 + reach), 59.0 + lift, 10.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, hd, p0, p1, 1, solid(P, "black" if j else "gold"), extend=0.4, t2=2)
        dome(m, bd, (sx * 8.0, 49.0, 0), 3.8, 3.4, PLATE)
        for j in range(3):
            spike(m, bd, (sx * 9.0, 52.0, -2.0 + j * 2.0), (sx * 0.6, 1, 0.3), 1.0, 4.0, SILVER, tip=0.25)
    for side in (1, -1):                                                               # great violet wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 50.0, 3.6))
        bat_wing(m, wb, (side * 3.0, 50.0, 3.6), 30.0, 28.0, 5, SILVER, cutout(lambda *a_: True, wingf), side=side,
                 sweep=25)
    tl = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32.0, 3.0), (0, 22.0, 10.0), (3.0, 12.0, 16.0), (6.0, 4.0, 18.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 3 - j, PLATE, extend=0.5)
    for j in range(5):                                                                 # crescent axe-blade
        ang = math.radians(-60 + j * 30)
        rod(m, tl, (6.0, 4.0, 18.0), (6.0 + 5.0 * math.cos(ang), 4.0 + 5.0 * math.sin(ang), 20.0), 1, SILVER,
            extend=0.3, t2=2)

    def ringf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        c = p["flame_core"] if (x + z) % 3.0 < 1.0 else p["flame"]
        return c, c[:3]
    for r_i, (cy, r, tilt) in enumerate(((44.0, 16.0, 20.0), (30.0, 18.0, -15.0))):  # rings of golden flame
        rb = m.bone("ring_flame_%d" % r_i, bd, (0, cy, 0))
        for i in range(16):
            a0 = 2 * math.pi * i / 16
            a1 = 2 * math.pi * (i + 1) / 16
            p0 = (r * math.cos(a0), cy + r * math.sin(a0) * math.sin(math.radians(tilt)), r * math.sin(a0))
            p1 = (r * math.cos(a1), cy + r * math.sin(a1) * math.sin(math.radians(tilt)), r * math.sin(a1))
            rod(m, rb, p0, p1, 2, ringf, extend=0.6)
    return m
