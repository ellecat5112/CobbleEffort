"""Shared builder for Dorbickmon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): the dragon
general. An armoured dragon-man in layered crimson plates edged with black spikes, round grey shoulder cannons, a
long dragon head with black swept horns and a red crest, huge clawed hands and feet with steel talons and a spiked
tail. make(name, mode):

- None: Dorbickmon itself.
- "army": Darkness Mode (Dragon Army), with two vast golden bat wings.
- "huang": Darkness Mode (Huanglongmon), riding a great golden dragon with a spiny back, horned head and a long tail.
- "flare": Darkness Mode (Flare Lizamon), riding a long-necked golden dragon and holding a sword of fire high.

Riders are built as a whole Dorbickmon and then moved onto the mount: `mount()` renames the rider's bones (prefix
"rider_"), parents them to the mount's body, and shifts its boxes while keeping each shader reading its original
coordinates, so painted patterns stay where they were.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import bat_wing, quadruped
from _digibody import dome, humanoid
from _digidetail import armour, cutout, flame_inside, local, metal, scales, solid
from _route import pal, tone

BASE = {"red": (170, 30, 40), "red_dark": (70, 8, 14), "red_light": (230, 110, 110), "black": (34, 32, 38),
        "black_dark": (10, 10, 12), "grey": (150, 150, 160), "grey_dark": (70, 70, 80), "steel": (210, 214, 226),
        "steel_dark": (100, 104, 116), "gold": (240, 200, 60), "gold_dark": (170, 120, 20), "gold_light": (255, 240, 150),
        "wing": (240, 190, 50), "wing_dark": (170, 110, 20), "eye": (250, 220, 60), "mouth": (130, 20, 30),
        "tooth": (250, 250, 246), "fire": (255, 150, 30, 210), "fire_core": (255, 240, 160, 235)}
SHINY = {"red": (40, 60, 160), "red_dark": (10, 20, 70), "red_light": (120, 150, 230), "gold": (200, 210, 230),
         "gold_dark": (110, 120, 150), "wing": (200, 210, 230), "wing_dark": (110, 120, 150)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "red", "red_dark", light="red_light", trim="black", trim_w=0.3)
STEEL = metal(P, "steel", dark="steel_dark")
GREY = armour(P, "grey", "grey_dark")
GOLD = scales(P, "gold", "gold_dark", size=1.6, light="gold_light", rim_mix=0.3)


def _shifted(sh, dy, dz):
    def s(x, y, z, face, variant, box=None, **k):
        return sh(x, y - dy, z - dz, face, variant, box=box, **k)
    return s


def mount(m, i_box, i_bone, dy, dz, parent):
    """Move everything built since (i_box, i_bone) up by dy and back by dz, rename its bones "rider_<name>" and hang
    its root bone from `parent`."""
    names = {}
    for b in m.bones[i_bone:]:
        old = b["name"]
        names[old] = "rider_" + old
        b["name"] = names[old]
        b["pivot"] = [b["pivot"][0], b["pivot"][1] + dy, b["pivot"][2] + dz]
    for b in m.bones[i_bone:]:
        b["parent"] = names.get(b["parent"], parent if b["parent"] is None else b["parent"])
    for bx in m.boxes[i_box:]:
        bx.bone = names.get(bx.bone, bx.bone)
        bx.lo = (bx.lo[0], bx.lo[1] + dy, bx.lo[2] + dz)
        if bx.pivot is not None:
            bx.pivot = (bx.pivot[0], bx.pivot[1] + dy, bx.pivot[2] + dz)
        bx.shader = _shifted(bx.shader, dy, dz)


def rider(m, name):
    """Dorbickmon itself; returns its anchors."""
    mats = {"skin": PLATE, "chest": PLATE, "abs": solid(P, "black"), "pelvis": PLATE, "neck": PLATE, "deltoid": PLATE,
            "upper_arm": PLATE, "forearm": PLATE, "hand": PLATE, "finger": PLATE, "claw": STEEL, "thigh": PLATE,
            "knee": PLATE, "shin": PLATE, "calf": PLATE, "foot": PLATE, "talon": STEEL}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.2, leg_bulk=1.2, claws=True, talons=True, digitigrade=True, name=name)
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.4, 2.8, 4.0, 54.0, 60.0, PLATE, cut=1)                         # dragon head
    m.box(hd, -2.0, 54.0, -7.4, 2.0, 56.0, -4.6, PLATE)
    m.box(hd, -1.8, 54.6, -7.6, 1.8, 55.2, -4.6, solid(P, "mouth"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.8, sx * 2.9), 57.4, -5.5, max(sx * 1.8, sx * 2.9), 58.2, -5.3, solid(P, "eye", glow=True))
        pts = [(sx * 2.4, 59.6, 0.0), (sx * 4.4, 63.0, 3.0), (sx * 4.8, 67.0, 7.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                                  # black swept horns
            rod(m, hd, p0, p1, 2 - j, solid(P, "black"), extend=0.4)
        dome(m, bd, (sx * 8.0, 49.0, 0), 3.4, 3.0, GREY)                                  # shoulder cannons
        m.round_box(bd, sx * 8.0, -3.6, 1.0, 0.6, 48.4, 50.6, solid(P, "black"), cut=0)
    for i in range(5):
        spike(m, hd, (0, 60.0, -2.0 + i * 1.4), (0, 1, 0.6), 1.0, 3.0 - i * 0.3, solid(P, "red"), tip=0.25)  # crest
    for i in range(16):                                                                  # black edge spikes
        ang = i * 2.3
        y = 30.0 + (i * 7) % 22
        d = (math.sin(ang), 0.2, math.cos(ang) * 0.6)
        spike(m, bd, (5.4 * d[0], y, 4.0 * d[2]), d, 1.0, 3.6, solid(P, "black"), tip=0.25)
    tl = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32.0, 3.0), (0, 24.0, 10.0), (2.0, 14.0, 16.0), (4.0, 6.0, 20.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 3 - j, PLATE, extend=0.5)
        spike(m, tl, p1, (0, 1, 0.4), 1.0, 2.4, solid(P, "black"), tip=0.25)
    return a


def dragon(m, name, long_neck=False):
    """The golden dragon mount."""
    mats = {"skin": GOLD, "belly": GOLD, "neck": GOLD, "head": GOLD, "snout": GOLD, "jaw": GOLD,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": GOLD, "leg_lower": GOLD, "paw": GOLD,
            "claw": STEEL, "tail": GOLD}
    neck = ((0, 26, -20), (0, 40, -30)) if long_neck else ((0, 22, -20), (0, 26, -26))
    a = quadruped(m, mats, name, length=44.0, body_y=18.0, body_rx=7.6, body_ry=7.0, chest_bulk=1.2, neck=neck,
                  head_len=10.0, head_w=3.8, head_h=4.0, snout=0.6, mouth_open=18, teeth=4, leg_bulk=1.7, toes=4,
                  tail=((0, 18, 22), (3, 14, 30), (8, 10, 36), (14, 9, 40)), tail_r=(3.0, 2.4, 1.8, 1.2))
    hd, bd = a["head"], a["body"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.3, ez + 0.6,
              solid(P, "eye", glow=True))
        pts = [(sx * 2.0, ey + 1.6, ez + 2.0), (sx * 3.6, ey + 6.0, ez + 6.0), (sx * 3.0, ey + 9.0, ez + 10.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "gold_light"), extend=0.4, t2=2)
    for i in range(12):                                                                  # spiny back
        t = i / 11
        spike(m, bd if i < 8 else a["tail"], (0, 25.0 - 8.0 * t, -16.0 + 50.0 * t), (0, 1, 0.5), 1.6, 4.0 - 2.0 * t,
              solid(P, "gold_light"), tip=0.4)
    return a


def make(name, mode=None):
    def build():
        m = Model(name)
        if mode in ("huang", "flare"):
            d = dragon(m, name, long_neck=mode == "flare")
            i_box, i_bone = len(m.boxes), len(m.bones)
            a = rider(m, "rider")
            if mode == "flare":                                                          # sword of fire held high
                ar = a["arm_right"]
                hx, hy, hz = ar["hand"]
                rod(m, ar["bone"], (hx, hy, hz), (hx, hy + 6.0, hz), 1, STEEL, extend=0, t2=2)

                def firef(x, y, z, face, variant, box=None, **k):
                    p = P(variant)
                    u, v, W, H = local(x, y, z, face, box)
                    c = p["fire_core"] if abs(u - W / 2) < W * 0.2 else p["fire"]
                    return c, c[:3]
                for ang in (0, 90):
                    m.box(ar["bone"], hx - 3.0, hy + 4.0, hz, hx + 3.0, hy + 28.0, hz,
                          cutout(flame_inside(5, 0.0, ang), firef), rotation=(0, ang, 0), pivot=(hx, hy + 4.0, hz))
            mount(m, i_box, i_bone, 14.0, 2.0, "body")
        else:
            rider(m, name)
            if mode == "army":                                                           # vast golden bat wings
                def wingf(x, y, z, face, variant, box=None, **k):
                    p = P(variant)
                    u, v, W, H = local(x, y, z, face, box)
                    return tone(p["wing"] if v / max(H, 1e-6) > 0.3 else p["wing_dark"], face), None
                for side in (1, -1):
                    wb = m.bone("wing_left" if side > 0 else "wing_right", "body", (side * 3.0, 50.0, 3.6))
                    bat_wing(m, wb, (side * 3.0, 50.0, 3.6), 36.0, 26.0, 4, PLATE, cutout(lambda *a_: True, wingf),
                             side=side, sweep=15)
        return m
    return build
