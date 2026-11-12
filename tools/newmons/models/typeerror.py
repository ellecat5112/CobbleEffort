"""Type: Error, the Corrupted Pokémon (shown as Normal; Error type in battle through its ability System Error), built
from boxes after the user's idea and the concept art they shared: a bipedal, more evil Type: Null built for heavy
attacks and speed.

A lean, dark-grey biped standing in a crouch: a brown helmet-mask shaped like an almond with a slit through which one
eye glares, four spikes radiating from it studded with green gems, a great white spiky mane behind it; one long arm
ending in a heavy silver pincer claw with glowing cyan tips, the other in a huge blue fin-shaped club notched along its
edge and hooked at the end; brown knee guards, tufts of spiky fur at its shoulders, hips and ankles, and tan talons.

Front is -z, y is up. 31 units tall; baseScale 0.98 (1.9 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain, mix, rod, spike
from _route import pal, tone

SCALE = 0.98
HITBOX = [1.0, 1.9]
KIND = "biped"
K = 4
HEIGHT = 31
LOOK = ("a lean, dark biped with a spiked brown mask and one glaring eye, a white spiky mane, a silver pincer claw "
        "with glowing cyan tips on one arm and a huge blue fin club on the other")

BASE = {"body": (66, 66, 72), "body_dark": (44, 44, 50), "mask": (160, 100, 70), "mask_dark": (118, 70, 48),
        "gem": (110, 170, 80), "mane": (246, 246, 250), "claw": (200, 202, 208), "claw_dark": (150, 152, 160),
        "cyan": (130, 240, 250), "club": (96, 146, 172), "club_dark": (66, 104, 128), "knee": (150, 74, 60),
        "talon": (228, 206, 150), "eye": (20, 20, 24)}
SHINY = {"body": (70, 54, 92), "body_dark": (48, 36, 66), "mask": (212, 170, 70), "mask_dark": (160, 120, 40),
         "gem": (220, 70, 90), "club": (196, 82, 124), "club_dark": (140, 50, 88), "cyan": (255, 210, 90)}


def P(v):
    return pal(BASE, SHINY, v)


def solid(key):
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s


def maskf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        if abs(x) < 0.25 and y > 24.5:
            return p["mask_dark"], None                              # the slit
        if ((x - 0.9) / 0.55) ** 2 + ((y - 26.4) / 0.4) ** 2 < 1:
            return p["eye"], None                                    # the glaring eye
        if abs(x + 0.7 - 0.3 * (y - 26)) < 0.15 and abs(y - 27) < 1.2:
            return p["mask_dark"], None
    return tone(p["mask"], face), None


def gemmed(x, y, z, face, variant, **k):
    """A mask spike with a green gem stud near its base."""
    p = P(variant)
    return tone(p["mask"], face), None


def fur(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["body_dark"] if int((x + z) * 2) % 3 == 0 else p["body"], face), None


def clawf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if box is not None and box.size[2] > 0:
        t = (box.lo[2] + box.size[2] - z) / box.size[2]
        if t > 0.8:
            return p["cyan"], p["cyan"]                              # glowing cyan tips
    return tone(p["claw"] if face != "down" else p["claw_dark"], face), None


def clubf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and abs((y * 0.8 + z * 0.4) % 3.0 - 1.5) < 0.12:
        return p["club_dark"], None                                  # a ragged seam
    return tone(p["club"], face), None


def build() -> Model:
    m = Model("typeerror")
    top = m.bone("typeerror", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 13, 0))
    m.round_box(bd, 0, 0, 3.5, 2.5, 12, 22, solid("body"), cut=1)                # lean torso
    m.round_box(bd, 0, -0.5, 1.4, 0.8, 13, 15, solid("knee"), cut=0.4)            # a brown core gem
    for sx in (-1, 1):                                                             # spiky shoulder tufts
        spike(m, bd, (sx * 3.6, 21.5, 0), (sx * 0.8, 0.6, 0.2), 2, 3, fur, tip=1)
    hd = m.bone("head", bd, (0, 22, -0.5))
    m.round_box(hd, 0, -0.5, 2.6, 2.6, 22, 28, solid("body_dark"), cut=1)
    m.round_box(hd, 0, -2.4, 3, 1.2, 22.5, 30.5, maskf, cut=1)                    # the almond mask
    for (dx, dy) in ((1, 1), (-1, 1), (1, -1), (-1, -1)):                          # four spikes in an X, gem-studded
        base = (dx * 2, 26.5 + dy * 2.2, -3)
        spike(m, hd, base, (dx * 1.0, dy * 0.8, 0.1), 1.6, 5.5, gemmed, tip=0.8)
        gx, gy = dx * 3.2, 26.5 + dy * 3.1
        m.box(hd, gx - 0.6, gy - 0.6, -3.9, gx + 0.6, gy + 0.6, -3.1, solid("gem"))
    mane = m.bone("mane", hd, (0, 27, 1.5))                                         # the great white spiky mane
    for i, (dx, dy, ln) in enumerate(((0, 1, 7), (0.7, 0.8, 6.5), (-0.7, 0.8, 6.5), (1, 0.2, 6), (-1, 0.2, 6),
                                      (0.8, -0.5, 5), (-0.8, -0.5, 5), (0.35, 1, 6.8), (-0.35, 1, 6.8))):
        spike(m, mane, (dx * 1.5, 27 + dy * 1.5, 2), (dx, dy, 0.35), 3, ln, solid("mane"), tip=1.4)
    # one arm: a heavy silver pincer claw
    a = m.bone("arm_left", bd, (4, 21, 0))
    rod(m, a, (4, 21, 0), (6, 15, -1), 1.8, solid("body"))
    rod(m, a, (6, 15, -1), (7, 9.5, -2), 1.8, solid("body"))
    m.round_box(a, 7.2, -2, 2.2, 2.6, 4, 11, solid("claw"), cut=1)                  # the claw's casing
    for dz, dy in ((-1.2, 0), (1.0, 0.3)):
        rod(m, a, (7.2, 4.6 + dy, -2 + dz), (6.0, 2.4 + dy, -4.2 + dz), 1.3, clawf)  # the pincer's two prongs
    # the other arm: a huge blue fin club
    c = m.bone("arm_right", bd, (-4, 21, 0))
    rod(m, c, (-4, 21, 0), (-6.5, 17, -3), 1.8, solid("body"))
    rod(m, c, (-6.5, 17, -3), (-8.5, 14, -6), 1.8, solid("body"))
    m.round_box(c, -10, -8, 2.5, 4, 3.5, 14.5, clubf, cut=1.5)                      # the club, a big rounded fin
    m.round_box(c, -10, -8.5, 2, 3, 1.5, 4.5, clubf, cut=1)
    for i in range(3):                                                              # notches along its edge
        spike(m, c, (-10, 13 - i * 3, -11.4), (0, 0.4, -1), 1.5, 2, clubf)
    rod(m, c, (-10, 2.6, -7), (-10, 1.4, -10), 1.6, clubf)                           # its hooked end
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                             # digitigrade legs
        lg = m.bone(nm, top, (sx * 2.2, 13, 0.5))
        rod(m, lg, (sx * 2.2, 13, 0.5), (sx * 3.4, 7.5, -1.5), 2.4, solid("body"))
        m.round_box(lg, sx * 3.4, -2, 1.5, 1.4, 6.5, 9, solid("knee"), cut=0.5)    # knee guard
        rod(m, lg, (sx * 3.4, 7.5, -1.5), (sx * 3.4, 2, 1.5), 2, solid("body"))
        spike(m, lg, (sx * 3.4, 3, 2), (sx * 0.5, 0.2, 1), 1.5, 2.5, fur)            # ankle tuft
        m.box(lg, sx * 3.4 - 1.4, 0, -1.5, sx * 3.4 + 1.4, 2.2, 2, solid("body"))
        for dx in (-0.9, 0, 0.9):
            rod(m, lg, (sx * 3.4 + dx, 0.6, -1.4), (sx * 3.4 + dx, 0.2, -3), 0.7, solid("talon"))
    return m
