"""Death-X-mon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the X-program reaper. A lean demonic knight in angular violet armour edged with gold, its helm a
silver dragon mask with tall back-swept horns and glowing green eyes, a green crystal set in its chest, long red
hooked claws on its hands and feet, crimson feather wings fanning from its back and a ring of jagged violet blades
spread round its hips like a skirt. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import armour, feathers, gem, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean demonic knight in angular violet armour edged with gold, a silver dragon-mask helm with back-swept "
        "horns and green eyes, red hooked claws, crimson feather wings and a ring of jagged violet hip blades")
BASE = {"violet": (100, 50, 150), "violet_dark": (40, 14, 70), "violet_light": (180, 130, 230), "gold": (240, 200, 70),
        "silver": (210, 214, 226), "silver_dark": (110, 114, 128), "red": (200, 30, 40), "red_light": (255, 140, 150),
        "feather": (190, 30, 40), "feather_dark": (90, 10, 20), "green": (60, 230, 160), "green_light": (210, 255, 230),
        "black": (30, 26, 34)}
SHINY = {"violet": (40, 110, 90), "violet_dark": (10, 50, 40), "violet_light": (120, 210, 180),
         "feather": (230, 160, 40), "feather_dark": (150, 80, 10)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "violet", "violet_dark", light="violet_light", trim="gold", trim_w=0.3)
SILVER = metal(P, "silver", dark="silver_dark")
CLAW = gem(P, "red", "red_light", glow=False)
FEATH = feathers(P, "feather", "feather_dark", size=(1.4, 3.0), tip="black")


def build():
    m = Model("deathxmon")
    mats = {"skin": PLATE, "chest": PLATE, "abs": solid(P, "black"), "pelvis": PLATE, "neck": SILVER,
            "deltoid": PLATE, "upper_arm": solid(P, "black"), "forearm": PLATE, "hand": PLATE, "finger": PLATE,
            "claw": CLAW, "thigh": PLATE, "knee": SILVER, "shin": PLATE, "calf": PLATE, "foot": PLATE, "talon": CLAW}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=1.0, leg_bulk=1.0, digitigrade=True, claws=True, talons=True,
                 name="deathxmon")
    bd = a["body"]
    m.round_box(bd, 0, a["chest_front"] + 0.6, 1.6, 1.0, 45.0, 48.6, gem(P, "green", "green_light"), cut=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.6, 3.2, 54.0, 60.0, SILVER, cut=1)                    # dragon-mask helm
    spike(m, hd, (0, 56.0, -3.4), (0, -0.2, -1), 2.6, 4.0, SILVER, tip=0.3)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.2), 57.6, -3.9, max(sx * 0.8, sx * 2.2), 58.4, -3.5, solid(P, "green", glow=True))
        pts = [(sx * 2.0, 59.6, 0.0), (sx * 3.6, 63.0, 4.0), (sx * 4.6, 66.0, 9.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 2 - j, SILVER, extend=0.4)
    for nm in ("arm_left", "arm_right"):                                           # long red hooked claws
        ar = a[nm]
        hx, hy, hz = ar["hand"]
        for j in range(3):
            spike(m, ar["bone"], (hx + (j - 1) * 1.0, hy - 2.6, hz - 1.0), (0, -1, -0.6), 0.9, 5.0, CLAW, tip=0.2)
    for i in range(10):                                                            # ring of jagged hip blades
        ang = math.radians(i * 36 + 18)
        d = (math.sin(ang), -0.5, -math.cos(ang))
        spike(m, bd, (4.4 * d[0], 32.0, 3.4 * d[2]), d, 2.0, 7.0 + (i % 2) * 3.0, PLATE, tip=0.15)
    for side in (1, -1):                                                           # crimson feather wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 50.0, 3.4))
        feather_wing(m, wb, (side * 3.0, 50.0, 3.4), 24.0, 16.0, 3, FEATH, side=side, sweep=25, droop=-6.0)
    return m
