"""Iron Sentry (Steel/Electric), the paradox Registeel, built from boxes after @Alex_LR04's art (the art's own name).

A wide white sphere of curved armour plates split by seams, a black band down its face showing Registeel's seven
dots (a hexagon round a centre) in glowing red, and glowing red seams flecked with white running round it. Two small
white spheres sit on its shoulders, each banded in red. From under them hang thin black jointed arms, each elbow
hooked up into a black horn, ending in long black hands marked with red triangles and three long glowing red fingers.
Below the sphere a black ribbed stalk stands on a round grey platform, and two short grey legs with red-marked feet
carry it.

Shiny: gunmetal blue armour with cyan energy.

Front is -z, y is up. 41 units tall; about 1.9 blocks.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _regi import HEX, dot_at, ellipsoid, glowing, lit, speck
from _route import pal, tone

HEIGHT = 41
SCALE = round(1.9 * 16 / HEIGHT, 3)
HITBOX = [1.5, HEIGHT / 16]
KIND = "biped"
K = 3
LOOK = ("a wide white armoured sphere with a black face band of glowing red dots, red-banded shoulder spheres, thin "
        "black arms with long glowing red fingers, on a round platform and two short legs")

BASE = {"white": (240, 240, 244), "white_shade": (208, 208, 216), "seg": (196, 198, 206), "seam": (120, 122, 132),
        "black": (32, 32, 38), "black_light": (58, 58, 66), "grey": (184, 184, 190), "grey_dark": (136, 136, 144),
        "glow": (255, 60, 66), "glow_light": (255, 150, 150), "fleck": (255, 246, 246)}
SHINY = {"white": (150, 168, 200), "white_shade": (118, 136, 170), "seg": (130, 148, 182), "seam": (70, 82, 110),
         "grey": (120, 136, 164), "grey_dark": (86, 100, 128), "glow": (60, 228, 255), "glow_light": (170, 244, 255),
         "fleck": (236, 255, 255)}

CY = 28.5                    # the sphere's centre
BAND = 6.4                   # half-width of the black face band


def P(v):
    return pal(BASE, SHINY, v)


GLOW = glowing(P, "glow", light="glow_light")


def red(x, y, z, face, p):
    """Glowing red seams flecked with white -> (colour, glow)."""
    c = p["fleck"] if speck(x, y, z, face, cell=1.6, r=0.28, prob=0.35) else p["glow"]
    return c, c


def spheref(x, y, z, face, variant, **k):
    p = P(variant)
    front = face == "north" or (face in ("up", "down") and z < -2)
    if front and abs(x) < BAND:
        if face == "north" and dot_at(-x, y - 28.2, HEX, 0.95):
            return p["glow"], p["glow"]
        return lit(p["black"], face, y, CY, 12), None
    ax = abs(x)
    # the glowing red seams: a band above and one below the face band, curving down to the shoulders, and round
    # each side of the sphere
    if face in ("north", "up", "down") and ax >= BAND:
        for sgn in (1, -1):
            yy = CY + sgn * (8.0 - 0.18 * (ax - BAND))
            if abs(y - yy) < 0.45:
                return red(x, y, z, face, p)
    if face in ("east", "west"):
        if abs(((y - CY) / 8.2) ** 2 + (z / 8.6) ** 2 - 1) < 0.12:
            return red(x, y, z, face, p)
    if face == "north" and (abs(ax - BAND) < 0.25 or abs(ax - 9.6) < 0.22):
        return p["seam"], None
    if face == "north" and ax < 9.6:
        return lit(p["seg"], face, y, CY, 12), None
    return lit(p["white"] if face != "south" else p["white_shade"], face, y, CY, 12), None


def shoulderf(x, y, z, face, variant, **k):
    p = P(variant)
    if abs(y - 33.4) < 0.6 and face != "up":
        return red(x, y, z, face, p)
    if face == "down":
        return red(x, y, z, face, p)
    return lit(p["white"], face, y, 33.5, 4.5), None


def solid(key):
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s


def stalkf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["black_light"] if (y % 1.6) < 0.4 else p["black"], face), None


def handf(x, y, z, face, variant, **k):
    """A long black hand marked with red triangles (on its broad faces)."""
    p = P(variant)
    if face in ("north", "south", "up", "down"):
        u, v = (x, -z) if face in ("up", "down") else (x, y)
    return tone(p["black"], face), None


def footf(sx):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "north":
            u = (x - sx * 5.0) * sx - 0.6                                  # across the foot, outward positive
            if 0.2 <= y <= 5.2 and abs(u) < (5.2 - y) * 0.42:
                return red(x, y, z, face, p)                                # a red triangle on the foot's front
        return tone(p["grey"] if face != "down" else p["grey_dark"], face), None
    return s


def build() -> Model:
    m = Model("ironsentry")
    top = m.bone("ironsentry", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    ellipsoid(m, bd, 0, CY, 0, 14.5, 12.0, 12.0, spheref, step=1)        # the armoured sphere
    m.round_box(bd, 0, 0, 3, 3, 13, 18, stalkf, cut=1)                   # the black ribbed stalk
    m.round_box(bd, 0, 0, 12.5, 9, 11, 13, solid("grey"), cut=4)         # the round platform
    m.round_box(bd, 0, 0, 10.5, 7.5, 10, 11, solid("grey_dark"), cut=3)
    for sx in (-1, 1):
        ellipsoid(m, bd, sx * 15.5, 33.5, 0, 4.5, 4.5, 4.5, shoulderf, step=1)   # the shoulder spheres
    for nm, sx in (("arm_left", -1), ("arm_right", 1)):
        arm = m.bone(nm, bd, (sx * 16, 29.5, 0))
        rod(m, arm, (sx * 16, 30, 0), (sx * 19, 20, -1), 2.4, solid("black"), extend=0.6)       # upper arm
        rod(m, arm, (sx * 19, 20, -1), (sx * 18.2, 25.5, -1.4), 2.2, solid("black"), extend=0.6)  # the hooked horn
        rod(m, arm, (sx * 18.2, 25.5, -1.4), (sx * 16.8, 28.6, -1.6), 1.2, solid("black"), extend=0.3)
        rod(m, arm, (sx * 19, 20, -1), (sx * 24, 16, -2), 2.4, solid("black"), extend=0.6)        # forearm
        rod(m, arm, (sx * 24, 16.5, -2), (sx * 26, 10.5, -2.5), 5, solid("black"), extend=0.8, t2=2.2)  # long hand
        for i, (dx, dz) in enumerate(((-2.2, 1.6), (0.4, 0.0), (3.0, -1.6))):
            a = (sx * (26 + dx * 0.3), 11.0, -2.5 + dz * 0.3)
            mid = (sx * (26 + dx * 0.8), 6.5, -2.5 + dz * 0.7)
            b = (sx * (26 + dx * 1.1), 2.0, -3.5 + dz)
            rod(m, arm, a, mid, 1.6, GLOW, extend=0.4)                    # three long glowing fingers, curling in
            rod(m, arm, mid, b, 1.4, GLOW, extend=0.4)
        for t in (0.25, 0.55, 0.85):                                      # red triangles on the back of the hand
            cx, cy = sx * (24 + 2 * t), 16.5 - 6 * t
            rod(m, arm, (cx, cy, -3.3), (cx + sx * 0.25, cy - 1.4, -3.3), 1.0, GLOW, extend=0.2, t2=0.6)
    for nm, sx in (("leg_left", -1), ("leg_right", 1)):
        lg = m.bone(nm, bd, (sx * 5, 11, 0))
        m.round_box(lg, sx * 5, 0, 2.5, 2.5, 4, 11, solid("grey"), cut=1)       # short legs
        m.round_box(lg, sx * 5, -0.5, 3.5, 3.5, 0, 5, footf(sx), cut=1)          # flared feet
    return m
