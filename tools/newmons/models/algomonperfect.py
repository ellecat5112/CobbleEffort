"""Algomon (Perfect) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a lean humanoid in a black bodysuit traced with green vine lines, violet plates on its
chest, hips and thighs each opening a yellow eye, a long black helmet with a green crest and a pale mask face, red
claws, two great sprays of lime feathers on its back and long green whip-tentacles ending in claws. 25 blocks tall.

Front is -z, y is up. 70 units tall (the feathers); Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid, shell
from _algo import BLACK, CLAW, GREEN, P, VIOLET, tentaclef
from _digidetail import armour, feathers, local, plane, skin, solid, torso_bulges
from _route import tone

HEIGHT = 70
SCALE, HITBOX = sized(25, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a lean humanoid in a black bodysuit traced with green vines, violet eye-plates on chest, hips and thighs, a "
        "long black helmet with a green crest, red claws, two sprays of lime feathers and long green whip-tentacles")
PLUME = feathers(P, "feather", "feather_dark", size=(1.4, 3.6), flow=(0, 1), tip="green_light")
TENT = tentaclef()
SUIT = skin(P, "black", light="black_light", bulges=torso_bulges(0, 50.0, 5.0, abs_rows=3), var=0.03)


def vined(base):
    """Black with green vine lines winding over it (sinuous bands)."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        a, b = plane(x, y, z, face)
        if abs(math.sin(a * 0.9 + b * 0.25) * 2.2 - (b % 7.0 - 3.5) * 0.6) < 0.32:
            return tone(p["green"], face), None
        return base(x, y, z, face, variant, box=box, **k)
    return s


def eyeplate(x, y, z, face, variant, box=None, **k):
    """A violet plate with a green rim and a yellow eye in its middle."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if face in ("north", "south", "east", "west"):
        du, dv = u - W / 2, v - H / 2
        if (du / max(W * 0.24, 0.5)) ** 2 + (dv / max(H * 0.18, 0.5)) ** 2 < 1:
            return (p["eye_y"] if abs(du) > 0.3 else p["pupil"]), None
        if min(u, W - u, v, H - v) < 0.45:
            return tone(p["green"], face), None
    return VIOLET(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("algomonperfect")
    V = vined(BLACK)
    mats = {"skin": V, "chest": SUIT, "abs": SUIT, "pelvis": V, "neck": BLACK, "deltoid": V, "upper_arm": V,
            "forearm": V, "hand": BLACK, "finger": BLACK, "claw": CLAW, "thigh": V, "knee": BLACK, "shin": V,
            "calf": V, "foot": BLACK, "talon": CLAW}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.9, leg_bulk=0.95, digitigrade=True, claws=True, talons=True,
                 name="algomonperfect", hand_pose="open")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.8, 54.5, 61.0, BLACK, cut=1)
    m.box(hd, -1.6, 55.0, -5.6, 1.6, 59.0, -2.0, solid(P, "white"), rotation=(-10, 0, 0), pivot=(0, 57, -2))  # mask
    for sx in (-1, 1):
        m.box(hd, sx * 0.9 - 0.4, 57.6, -5.8, sx * 0.9 + 0.4, 58.2, -4.8, solid(P, "eye_r", glow=True))
    rod(m, hd, (0, 60.5, -1.5), (0, 66.0, 4.0), 2, GREEN, extend=0.3)                 # green crest sweeping back
    rod(m, hd, (0, 61.0, -3.0), (0, 63.5, -4.0), 1, GREEN, extend=0.3)
    # violet eye plates: chest pair, hip pair, thighs
    for sx in (-1, 1):
        m.box(bd, sx * 2.6 - 2.0, 44.0, -5.0, sx * 2.6 + 2.0, 49.0, -4.0, eyeplate,
              rotation=(0, 0, sx * 12), pivot=(sx * 2.6, 46.5, -4.5))
        m.box(bd, sx * 4.0 - 1.4, 29.0, -4.4, sx * 4.0 + 1.4, 34.0, -3.4, eyeplate)
        lg = a["leg_left" if sx > 0 else "leg_right"]
        m.box(lg["bone"], lg["knee"][0] - 1.6, 21.0, -4.8, lg["knee"][0] + 1.6, 28.0, -3.8, eyeplate)
    shell(m, bd, (0, 0, 0.4), 4.0, 50.0, 52.4, -100, 100, 7, 1.0, GREEN)               # collar
    # two great sprays of feathers rising from the back
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
        wb = m.bone(nm, bd, (sx * 3.0, 48.0, 3.0))
        for i in range(9):
            ang = math.radians(10 + i * 9)
            ln = 13.0 + (i % 3) * 3
            tip = (sx * (3.0 + ln * math.cos(ang)), 48.0 + ln * math.sin(ang), 5.0 + i * 0.6)
            rod(m, wb, (sx * 3.0, 48.0, 3.5), tip, 3, PLUME, extend=0.3, t2=1)
    # long whip tentacles from the shoulder blades, ending in red claws
    for sx in (-1, 1):
        tb = m.bone("tail" if sx > 0 else "tail_2", bd, (sx * 2.0, 46.0, 3.0))
        pts = [(sx * 2.0, 46.0, 3.0), (sx * 8.0, 52.0, 8.0), (sx * 16.0, 55.0, 6.0), (sx * 22.0, 50.0, 0.0),
               (sx * 25.0, 44.0, -4.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tb, p0, p1, 2 if j < 2 else 1, TENT, extend=0.4)
        for d in ((sx * 0.4, -1, -0.4), (sx * 1, -0.6, -0.2), (0, -1, 0.3)):
            spike(m, tb, pts[-1], d, 1.0, 2.6, CLAW)
    # blue-tipped drops hanging from the forearms (its "algorithm" droplets)
    for nm in ("arm_left", "arm_right"):
        w = a[nm]["wrist"]
        m.box(a[nm]["bone"], w[0] - 0.8, w[1] - 7.0, w[2] - 0.8, w[0] + 0.8, w[1] - 4.0, w[2] + 0.8,
              solid(P, "drop", glow=True))
    return m
