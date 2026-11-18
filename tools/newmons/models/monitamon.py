"""Monitamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a little ninja whose head is a boxy olive-green CRT monitor with a dark screen, ringed by a
corrugated cable collar, an olive suit with an ammo belt of brown pouches, an orange satchel, a red gloved hand
holding a dagger, and stubby feet. 1 block tall.

Front is -z, y is up. 30 units tall; Child stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, fabric, leather, local, metal, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a little ninja whose head is a boxy olive-green CRT monitor, an olive suit, an ammo belt of pouches and a dagger"
BASE = {"olive": (120, 130, 60), "olive_dark": (60, 70, 24), "screen": (40, 60, 40), "screen_light": (100, 130, 90),
        "cable": (110, 110, 120), "brown": (150, 100, 50), "brown_dark": (90, 56, 24), "orange": (220, 130, 40),
        "red": (210, 40, 40), "steel": (200, 204, 214)}
SHINY = {"olive": (60, 70, 130), "olive_dark": (24, 30, 80)}


def P(v):
    return pal(BASE, SHINY, v)


CASE = armour(P, "olive", "olive_dark", trim="olive_dark", trim_w=0.3)
SUIT = fabric(P, "olive", "olive_dark")


def screenf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return tone(p["screen_light"] if u / max(W, 1e-6) + v / max(H, 1e-6) > 1.4 else p["screen"], face), None


def build():
    m = Model("monitamon")
    top = m.bone("monitamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0.4, 4.0, 3.4, 4.0, 15.0, SUIT, cut=1)                            # olive suit body
    m.round_box(bd, 0, 0.4, 4.3, 3.7, 8.0, 9.4, leather(P, "brown", "brown_dark"), cut=1)  # ammo belt
    for j in range(5):
        m.box(bd, -3.6 + j * 1.8, 7.4, -4.4, -2.6 + j * 1.8, 9.0, -3.8, solid(P, "brown_dark"))
    m.round_box(bd, 4.6, 1.0, 1.2, 2.4, 8.0, 12.0, solid(P, "orange"), cut=0)            # satchel
    m.round_box(bd, 0, 0.0, 3.6, 3.6, 15.0, 16.6, metal(P, "cable"), cut=1)              # cable collar
    hd = m.bone("head", bd, (0, 17, 0))
    m.round_box(hd, 0, 0.6, 6.0, 6.0, 16.6, 28.0, CASE, cut=1)                           # CRT monitor head
    m.box(hd, -4.6, 18.2, -5.5, 4.6, 26.4, -5.3, screenf)
    m.box(hd, -1.4, 27.6, -1.0, 1.4, 28.6, 3.0, CASE)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.0, 13.0, 0))
        rod(m, ab, (sx * 4.0, 13.0, 0), (sx * 4.6, 9.0, -2.4), 2, SUIT, extend=0.3)
        m.round_box(ab, sx * 4.6, -3.0, 1.2, 1.2, 7.4, 9.4, solid(P, "red"), cut=0)
    rod(m, "arm_right", (-4.6, 8.6, -3.6), (-4.0, 13.0, -6.0), 1, metal(P, "steel"), extend=0.2, t2=1)  # dagger
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.0, 5.0, 0))
        rod(m, lg, (sx * 2.0, 5.0, 0.4), (sx * 2.0, 1.0, 0.4), 2, SUIT, extend=0.3)
        m.round_box(lg, sx * 2.0, -0.2, 1.4, 1.8, 0.0, 1.4, CASE, cut=0)
    return m
