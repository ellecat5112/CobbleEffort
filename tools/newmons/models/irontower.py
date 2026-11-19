"""Iron Tower (Rock/Electric), the paradox Regirock, built from boxes after @Alex_LR04's art (the art's own name).

A small grey helmet sunk between its shoulders, its black visor showing Regirock's seven dots (an H) in glowing
orange. A broad light grey chest plate with a crease down the middle and glowing orange pads on its lower corners,
side guards over a dark charcoal core with a seam down its front. Two huge dark pillars rise from its back, tipped with
glowing orange cones and banded with orange; its short arms swell into enormous forearms ending in glowing orange
rounded fists, raised outward. It stands on short ball-jointed legs with orange marks on its feet.

Shiny: sandstone armour with turquoise energy.

Front is -z, y is up. 41 units tall to the pillar tips; about 1.7 blocks.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _regi import H, dot_at, ellipsoid, glowing, speck
from _route import pal, tone

HEIGHT = 41
SCALE = round(1.7 * 16 / HEIGHT, 3)
HITBOX = [1.4, HEIGHT / 16]
KIND = "biped"
K = 3
LOOK = ("a grey armoured golem with a small black-visored helmet of orange dots, two dark back pillars tipped with "
        "glowing orange cones and huge forearms ending in glowing orange fists")

BASE = {"light": (224, 224, 228), "grey": (186, 188, 194), "grey_dark": (142, 144, 152), "char": (68, 66, 70),
        "char_light": (92, 90, 96), "char_dark": (44, 42, 46), "visor": (24, 24, 28), "glow": (255, 150, 36),
        "glow_light": (255, 198, 112), "fleck": (255, 250, 236)}
SHINY = {"light": (228, 206, 166), "grey": (196, 172, 134), "grey_dark": (150, 126, 94), "char": (96, 72, 58),
         "char_light": (122, 96, 78), "char_dark": (66, 48, 38), "glow": (56, 224, 206), "glow_light": (160, 246, 236),
         "fleck": (236, 255, 252)}


def P(v):
    return pal(BASE, SHINY, v)


GLOW = glowing(P, "glow", light="glow_light")


def orange(x, y, z, face, p):
    c = p["fleck"] if speck(x, y, z, face) else p["glow"]
    return c, c


def solid(key):
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s


def chestf(x, y, z, face, variant, **k):
    p = P(variant)
    ax = abs(x)
    if face == "north":
        if 4.8 <= ax <= 7.9 and 17.9 <= y <= 19.8:
            return orange(x, y, z, face, p)                              # the glowing pads on its lower corners
        if ax < 2.6 and y > 25.1:
            return tone(p["grey_dark"], face), None                      # the notch under the helmet
        if ax < 0.22 and 21.5 < y < 25.2:
            return p["grey_dark"], None                                  # the crease down the middle
        if 19.6 < y < 20.1 and ax < 4.8:
            return p["grey"], None                                       # the plate's lower lip
    if face == "up":
        return p["light"], None
    return tone(p["light"] if face in ("north", "east", "west") else p["grey"], face), None


def guardf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and y > 17.9 and abs(x) < 7.9:
        return orange(x, y, z, face, p)
    return tone(p["light"] if face != "south" else p["grey"], face), None


def coref(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        if abs(x) < 0.25:
            return p["char_dark"], None                                  # the seam down its core
        if (abs(x) - 4.3) ** 2 + (y - 12.0) ** 2 < 2.2 ** 2:
            return tone(p["char_light"], face), None                     # rounded side bulges
    return tone(p["char"], face), None


def helmetf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(x) <= 2.4 and 25.6 <= y <= 30.0:
        if dot_at(-x, y - 27.8, H, 0.62):
            return p["glow"], p["glow"]
        return p["visor"], None
    return tone(p["grey"] if face != "up" else p["light"], face), None


def pillarf(x, y, z, face, variant, **k):
    """The dark back pillars (rods: z runs back from the base at z = 4.5 along them): two orange bands."""
    p = P(variant)
    d = 4.5 - z
    if face not in ("north", "south") and (3.0 < d < 3.9 or 4.9 < d < 5.8):
        return orange(x, y, z, face, p)
    return tone(p["char"], face), None


def footf(sx):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "north":
            u = (x - sx * 4.2) * sx - 0.8
            if y <= 2.4 and abs(u) < (2.6 - y) * 0.75:
                return orange(x, y, z, face, p)                          # an orange mark on each foot
        return tone(p["grey"], face), None
    return s


def build() -> Model:
    m = Model("irontower")
    top = m.bone("irontower", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 0, 8.5, 6, 18, 26.5, chestf, cut=2)                # the broad chest plate
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 5.8, sx * 8.4))
        m.box(bd, x0, 14.5, -5.0, x1, 18.5, 4.0, guardf)                 # side guards
    m.round_box(bd, 0, 0.5, 5.5, 4.5, 8, 18.5, coref, cut=1.5)            # the dark charcoal core
    m.round_box(bd, 0, 0.5, 3, 3, 6.5, 8.5, solid("char_dark"), cut=1)
    hd = m.bone("head", bd, (0, 26, 0.5))
    m.round_box(hd, 0, 0.5, 3.5, 3.5, 24.5, 31, helmetf, cut=1)           # the small helmet
    m.box(hd, -1.0, 31, -1.0, 1.0, 32, 2.0, solid("grey_dark"))           # its ridge
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 3.4, sx * 4.4))
        m.box(hd, x0, 26, -1.0, x1, 29, 2.0, solid("grey_dark"))         # side vents
    # the two dark back pillars with glowing orange cones
    for nm, sx in (("pillar_left", -1), ("pillar_right", 1)):
        pl = m.bone(nm, bd, (sx * 9.5, 23, 4.5))
        a, d = (sx * 9.5, 22.0, 4.5), (sx * 0.34, 1, 0.18)
        b = tuple(av + dv * 11 for av, dv in zip(a, d))
        rod(m, pl, a, b, 8, pillarf, extend=0.5, t2=6)
        rod(m, pl, a, b, 6, pillarf, extend=0.5, t2=8)
        for i, w in enumerate((8, 6, 4, 2)):                              # the cone tip, in four narrowing steps
            a2 = tuple(bv + dv * (1.6 * i) for bv, dv in zip(b, d))
            b2 = tuple(bv + dv * (1.6 * (i + 1) + 0.4) for bv, dv in zip(b, d))
            rod(m, pl, a2, b2, w, GLOW, extend=0.2)
    # short arms swelling into huge forearms with glowing orange fists
    for nm, sx in (("arm_left", -1), ("arm_right", 1)):
        arm = m.bone(nm, bd, (sx * 9.4, 23, 0))
        ellipsoid(m, arm, sx * 9.6, 23, 0, 2.2, 2.2, 2.2, solid("grey"), step=1)        # shoulder joint
        rod(m, arm, (sx * 9.6, 22.5, 0), (sx * 13, 17.5, -0.5), 3.4, solid("grey"), extend=0.5)
        ellipsoid(m, arm, sx * 13.4, 17.5, -0.6, 2.4, 2.4, 2.4, solid("light"), step=1)  # elbow
        e, f = (sx * 13.6, 17.8, -0.8), (sx * 28.5, 26.0, -2.5)
        lerp = lambda t: tuple(ev + (fv - ev) * t for ev, fv in zip(e, f))
        rod(m, arm, e, lerp(0.38), 6, solid("grey"), extend=0.4)
        rod(m, arm, lerp(0.3), lerp(0.46), 8, solid("light"), extend=0.2)
        for t0, t1, w in ((0.42, 0.47, 8), (0.46, 0.84, 10), (0.83, 0.91, 8), (0.9, 0.96, 6), (0.95, 1.0, 3)):
            rod(m, arm, lerp(t0), lerp(t1), w, GLOW, extend=0.2)                         # the glowing fist
            if w >= 6:
                rod(m, arm, lerp(t0), lerp(t1), w - 3, GLOW, extend=0.2, t2=w + 1)
                rod(m, arm, lerp(t0), lerp(t1), w + 1, GLOW, extend=0.2, t2=w - 3)
    for nm, sx in (("leg_left", -1), ("leg_right", 1)):
        lg = m.bone(nm, bd, (sx * 4.2, 10, -0.5))
        ellipsoid(m, lg, sx * 4.2, 9.0, -0.5, 3.0, 3.0, 3.0, solid("light"), step=1)    # thigh balls
        m.round_box(lg, sx * 4.2, -0.5, 1.5, 1.5, 2.5, 7, solid("grey"), cut=0.5)       # shins
        m.round_box(lg, sx * 4.2, -1.0, 2.5, 3.0, 0, 2.5, footf(sx), cut=1)             # feet
    return m
