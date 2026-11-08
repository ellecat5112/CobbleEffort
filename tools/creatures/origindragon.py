"""
Origin Dragon: the fusion of Kyurem, Reshiram and Zekrom (a fan-made Pokémon). Built from scratch.

Design (after the reference): a towering bipedal dragon. Black, Zekrom-like chest with a gold gem, a pale
Reshiram-white belly and legs, big black wings fringed with white feathers, and three necks rising from the
shoulders: Reshiram's white head (blue eyes, swept-back feather crest) on its right, Kyurem's grey head
(yellow eyes, icy crest) in the middle, and Zekrom's black head (red eyes, gold crest) on its left.
The tail ends in Kyurem's pale-blue ice crystals.
"""
from __future__ import annotations

from modelkit import Model, Paint, hexc, sine

BLACK = hexc("26252b")
BLACK_HI = hexc("3b3a43")
WHITE = hexc("e9ecef")
WHITE_SH = hexc("b9c0c8")
GREY = hexc("6f7b88")
GREY_DK = hexc("4b5560")
GOLD = (240, 196, 60, 255)
GOLD_DIM = hexc("c79a2a")
ICE = (150, 214, 236, 255)
EYE_BLUE = (90, 190, 255, 255)
EYE_YELLOW = (255, 220, 60, 255)
EYE_RED = (240, 40, 40, 255)
CLAW = hexc("cfd5da")

SPECIES = "origindragon"
DEX_FOLDER = "2001_origindragon"
GROUP = "ce_origindragon"
FLIES = True
WALK = "q.biped_walk(0.6, 0.9, 'leg_left', 'leg_right')"


def plates(base, line, every=4):
    def pat(face, u, v, fw, fh):
        if face in ("front", "back", "left", "right") and v % every == every - 1:
            return line
        return None
    return Paint(base, noise=0.05, pattern=pat)


def chest():
    """Black chest with the gold diamond gem on the front."""
    def pat(face, u, v, fw, fh):
        if face == "front":
            cx, cy = (fw - 1) / 2, fh * 0.45
            if abs(u - cx) + abs(v - cy) * 0.9 <= 4:
                return GOLD if abs(u - cx) + abs(v - cy) * 0.9 <= 3 else GOLD_DIM
            if v == fh - 1:
                return BLACK_HI
        return None
    return Paint(BLACK, noise=0.06, pattern=pat)


def build_head(m, name, parent, pivot, skin, eye, crest):
    """A dragon head on a neck tip: skull, snout, jaw, two glowing eyes and a crest."""
    x, y, z = pivot
    m.bone(name, parent, pivot)
    m.box(name, (x, y + 3, z - 3), (7, 6, 9), Paint(skin, noise=0.05))          # skull
    m.box(name, (x, y + 1.5, z - 9.5), (5, 3, 6), Paint(skin, noise=0.05))       # snout
    m.box(name, (x, y - 0.5, z - 7), (5, 2, 8), Paint(GREY_DK, noise=0.05))      # jaw
    for side in (-1, 1):                                                            # eyes, glowing
        m.box(name, (x + side * 3.6, y + 4, z - 6), (1, 1, 2), Paint(eye[:3], pattern=lambda *a: eye))
    crest(m, name, x, y, z)
    return name


def crest_reshiram(m, bone, x, y, z):
    """Swept-back white feather crest, like Reshiram's head feathers."""
    for side in (-1, 1):
        m.cube(bone, (x + side * 3.5 - 0.5, y + 4, z), (1, 4, 12), Paint(WHITE, noise=0.04,
               pattern=lambda f, u, v, fw, fh: WHITE_SH if v % 4 == 3 else None),
               rotation=(-15, side * 20, 0), pivot=(x + side * 3.5, y + 5, z))
    m.cube(bone, (x - 1, y + 6, z - 1), (2, 3, 10), Paint(WHITE, noise=0.04), rotation=(-20, 0, 0), pivot=(x, y + 6, z))


def crest_kyurem(m, bone, x, y, z):
    """Icy crest: pale-blue crystals along the top of the head."""
    for i, dz in enumerate((-4, -1, 2)):
        m.cube(bone, (x - 1, y + 6, z + dz), (2, 3 + i, 2), Paint(ICE[:3], pattern=lambda *a: ICE, emissive=True),
               rotation=(-25, 0, 0), pivot=(x, y + 6, z + dz))


def crest_zekrom(m, bone, x, y, z):
    """Zekrom's head: a gold ring round the crown and a backswept black horn."""
    m.box(bone, (x, y + 6.5, z - 2), (8, 1, 6), Paint(GOLD[:3], pattern=lambda *a: GOLD))
    m.cube(bone, (x - 1.5, y + 6, z + 1), (3, 3, 10), Paint(BLACK, noise=0.05), rotation=(-25, 0, 0), pivot=(x, y + 6, z + 1))


def build():
    m = Model("origindragon", tex_width=256, seed=2001)
    m.bone("origindragon")
    m.locator("root", "origindragon", (0, 0, 0))
    m.bone("body", "origindragon", (0, 30, 0))
    m.locator("middle", "body", (0, 34, 0))
    m.locator("target", "body", (0, 38, -8))

    # torso
    m.box("body", (0, 44, 0), (18, 14, 12), chest())                                  # black chest
    m.box("body", (0, 32, 0.5), (14, 10, 10), plates(WHITE, WHITE_SH, 3))              # white belly
    m.box("body", (0, 25, 1), (16, 5, 11), Paint(GREY, noise=0.05))                    # hips
    m.box("body", (0, 51.5, 1), (14, 2, 10), Paint(BLACK_HI, noise=0.05))              # shoulder line

    # legs
    for side, name in ((-1, "leg_right"), (1, "leg_left")):
        m.bone(name, "body", (side * 6, 24, 1))
        m.box(name, (side * 6.5, 18, 1), (7, 11, 8), Paint(BLACK, noise=0.06))
        m.box(name, (side * 6.5, 8, 2), (5, 10, 6), plates(WHITE, WHITE_SH, 3))
        m.box(name, (side * 6.5, 1.5, 0), (7, 3, 10), Paint(GREY_DK, noise=0.05))
        for cx in (-2, 0, 2):
            m.box(name, (side * 6.5 + cx, 1, -5.5), (1, 2, 2), Paint(CLAW, noise=0.03))

    # arms: small, Zekrom-like, with pale claws
    for side, name in ((-1, "arm_right"), (1, "arm_left")):
        bones = m.chain(name, "body", (side * 9.5, 48, -2), [(9, 4, 4, (0, 0, side * 160)), (8, 4, 4, (-40, 0, 0))],
                        Paint(BLACK, noise=0.06))
        m.box(bones[-1], (side * 9, 63, -2), (5, 3, 5), Paint(CLAW, noise=0.04))

    # tail: black to grey, ending in Kyurem's ice crystals
    tail = m.chain("tail", "body", (0, 26, 6), [(10, 8, 7, (-70, 0, 0)), (10, 7, 6, (-15, 0, 0)),
                                                 (9, 6, 5, (-10, 0, 0)), (8, 5, 4, (-5, 0, 0))], plates(BLACK, GREY, 3))
    for i, (dx, rx, rz) in enumerate(((-2, 10, -25), (0, 0, 0), (2, 10, 25))):
        m.cube(tail[-1], (dx - 1, 63, 5), (2, 6 + i % 2 * 2, 2), Paint(ICE[:3], pattern=lambda *a: ICE, emissive=True),
               rotation=(rx, 0, rz), pivot=(dx, 63, 6))

    # wings: big black panels with a white feather fringe, folded half-open
    def wing_paint():
        def pat(face, u, v, fw, fh):
            if face in ("front", "back") and v >= fh - 4:
                return WHITE if (u // 2) % 2 == 0 or v >= fh - 2 else WHITE_SH
            if face in ("front", "back") and u % 6 == 0:
                return BLACK_HI
            return None
        return Paint(BLACK, noise=0.05, pattern=pat)
    for side, name in ((-1, "wing_right"), (1, "wing_left")):
        m.bone(name, "body", (side * 6, 48, 5), rotation=(-10, side * -15, -side * 22))
        m.box(name, (side * 16, 52, 5.5), (20, 22, 1), wing_paint())
        m.box(name, (side * 6.5, 54, 5.5), (3, 14, 3), Paint(BLACK_HI, noise=0.05))

    # three necks and heads
    neck_paint = {"reshiram": plates(WHITE, WHITE_SH, 3), "kyurem": plates(GREY, GREY_DK, 3), "zekrom": plates(BLACK, BLACK_HI, 3)}
    for key, x, lean, head_name, skin, eye, crest in (
            ("reshiram", -7, -42, "head_reshiram", WHITE, EYE_BLUE, crest_reshiram),
            ("kyurem", 0, 0, "head", GREY, EYE_YELLOW, crest_kyurem),
            ("zekrom", 7, 42, "head_zekrom", BLACK, EYE_RED, crest_zekrom)):
        # outer necks fan out (rotation z = side * angle leans a +y chain outward), then curve back up
        segs = [(7, 5, 5, (-10, 0, lean)), (6, 5, 5, (-5, 0, -lean * 0.3)), (5, 4, 4, (10, 0, -lean * 0.35))]
        bones = m.chain(f"neck_{key}", "body", (x, 51, -1), segs, neck_paint[key])
        tip_y = 51 + sum(s[0] for s in segs)
        build_head(m, head_name, bones[-1], (x, tip_y, -1), skin, eye, crest)
    m.locator("head", "head", (0, 78, -12))
    m.locator("top", "head", (0, 86, -2))
    return m


def shiny_recolour(rgb):
    """Shiny palette (my take): the black parts turn deep navy, the gold turns silver."""
    r, g, b = rgb
    if max(r, g, b) < 80:                            # blacks -> deep navy
        return (int(r * 0.6), int(g * 0.8), min(255, int(b * 1.9) + 20))
    if r > 180 and g > 140 and b < 100:              # gold -> silver
        return (220, 226, 236)
    return rgb


def animations():
    return {
        "ground_idle": {
            "body": {"position": [0, sine(0.4, 90), 0]},
            "neck_reshiram": {"rotation": [sine(2, 60), 0, sine(3, 60)]},
            "neck_kyurem": {"rotation": [sine(2, 60, 60), sine(3, 45), 0]},
            "neck_zekrom": {"rotation": [sine(2, 60, 120), 0, sine(-3, 60)]},
            "wing_left": {"rotation": [0, 0, sine(4, 90)]},
            "wing_right": {"rotation": [0, 0, sine(-4, 90)]},
            "tail": {"rotation": [0, sine(6, 60), 0]},
        },
        "air_idle": {
            "body": {"position": [0, sine(1.0, 120), 0]},
            "wing_left": {"rotation": [0, 0, sine(18, 180)]},
            "wing_right": {"rotation": [0, 0, sine(-18, 180)]},
            "neck_reshiram": {"rotation": [sine(2, 60), 0, 0]},
            "neck_zekrom": {"rotation": [sine(2, 60, 120), 0, 0]},
            "tail": {"rotation": [sine(4, 120), 0, 0]},
        },
        "air_fly": {
            "body": {"rotation": [15, 0, 0], "position": [0, sine(0.8, 240), 0]},
            "wing_left": {"rotation": [0, 0, sine(30, 240)]},
            "wing_right": {"rotation": [0, 0, sine(-30, 240)]},
            "leg_left": {"rotation": [30, 0, 0]},
            "leg_right": {"rotation": [30, 0, 0]},
            "tail": {"rotation": [sine(5, 240), 0, 0]},
        },
    }
