"""Blue Meramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a man of cold blue flame. A tall hunched figure whose whole body is dark navy fire licked by
blue-violet flames, tongues of fire rising from its head, shoulders, back and arms, a jagged grinning mouth and
bright pale eyes, with a ball of icy blue fire burning in its right hand. 25 blocks tall.

Front is -z, y is up. 62 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import cutout, fbm, flame_inside, local, mix
from _route import pal, tone

HEIGHT = 62
SCALE, HITBOX = sized(25, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a hunched man of cold blue flame: a dark navy fire body licked by blue-violet flames, a jagged grin, pale "
        "eyes and a ball of icy blue fire in its hand")
BASE = {"navy": (40, 40, 100), "navy_dark": (14, 14, 44), "violet": (110, 100, 220), "violet_light": (190, 180, 255),
        "flame": (120, 140, 255, 210), "flame_core": (220, 230, 255, 235), "ice": (120, 200, 255, 200),
        "ice_core": (230, 250, 255, 240), "eye": (230, 240, 255), "mouth": (8, 8, 20)}
SHINY = {"navy": (90, 30, 30), "navy_dark": (40, 8, 8), "violet": (240, 120, 60), "violet_light": (255, 210, 140),
         "flame": (255, 150, 60, 210), "flame_core": (255, 240, 200, 235), "ice": (255, 200, 80, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def firebody(x, y, z, face, variant, box=None, **k):
    """Dark navy flame with rising blue-violet licks (the licks glow)."""
    p = P(variant)
    n = fbm(x * 0.4, y * 0.18 - 0.0, z * 0.4, 7)
    lick = (n + 0.25 * math.sin(y * 0.9 + x)) % 1
    if lick > 0.78:
        c = mix(p["violet"], p["violet_light"], (lick - 0.78) * 4)
        return c + (255,), c
    return tone(mix(p["navy_dark"], p["navy"], n), face), None


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.2) < 0.7 and abs(y - 58.4 + sx * 0.0) < 0.4:
                return p["eye"], p["eye"]
        zig = 55.6 + 0.6 * abs(((x * 1.2) % 2) - 1)
        if abs(x) < 2.0 and zig - 0.5 < y < zig + 0.3:
            return tone(p["mouth"], face), None
    return firebody(x, y, z, face, variant, box=box, **k)


def flamef(key, core):
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        c = p[core] if v / max(H, 1e-6) < 0.3 else p[key]
        return c, c[:3]
    return s


def tongue(m, bone, c, w, h, rot=(0, 0, 0), seed=0, key="flame", core="flame_core"):
    m.box(bone, c[0] - w / 2, c[1], c[2], c[0] + w / 2, c[1] + h, c[2],
          cutout(flame_inside(3, 0.1 * ((seed % 3) - 1), seed), flamef(key, core)), rotation=rot, pivot=c)


def build():
    m = Model("bluemeramon")
    mats = {"skin": firebody}
    a = humanoid(m, mats, bulk=1.1, arm_bulk=1.2, leg_bulk=1.0, claws=True, name="bluemeramon")
    mats["claw"] = firebody
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, -1))
    m.round_box(hd, 0, -1.2, 2.6, 2.8, 54.0, 61.0, facef, cut=1)
    for i in range(5):                                                 # flames rising off the head
        tongue(m, hd, ((i - 2) * 1.2, 60.0, -1.0 + (i % 2) * 1.6), 3.4, 7.0, (0, i * 36, (i - 2) * 10), seed=i)
    for i in range(10):                                                # licks off the shoulders and back
        ang = math.radians(-90 + i * 20)
        c = (6.0 * math.sin(ang), 48.0 + (i % 3), 2.0 - 3.0 * math.cos(ang))
        tongue(m, bd, c, 4.0, 8.0 + (i % 3) * 2.0, (-20, math.degrees(ang), 10 * math.sin(ang)), seed=i + 10)
    for j in range(6):
        tongue(m, bd, (0, 32.0 + j * 3.0, 3.6), 6.0, 8.0, (-40, 0, 0), seed=j + 20)
    for nm in ("arm_left", "arm_right", "leg_left", "leg_right"):      # flames along the limbs
        ab = a[nm]
        p0 = ab.get("elbow", ab.get("knee"))
        for j in range(3):
            tongue(m, ab["bone"], (p0[0], p0[1] - 4.0 + j * 4.0, p0[2] + 1.6), 3.0, 5.0, (-60, 0, 0), seed=j + 30)
    # the ball of icy blue fire in its right hand
    h = a["arm_right"]["hand"]
    fb = m.bone("fireball", a["arm_right"]["bone"], h)
    for j, ang in enumerate((0, 45, 90, 135)):
        tongue(m, fb, (h[0] - 1.0, h[1] - 3.0, h[2] - 3.0), 7.0, 10.0, (0, ang, 0), seed=j + 40, key="ice",
               core="ice_core")
    return m
