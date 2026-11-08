"""
Celesteela (#797), the Launch Ultra Beast. A built-from-scratch model in Cobblemon's style.

Design (after the official art): a tall A-frame. The central body is a stepped pyramid of pale green and
white panels on a wide base with four short dark legs, topped by a tall banded antenna spire. Two huge
bamboo-like arm tubes rise to meet near the top and splay down and out to the ground, ringed with white
bands, ending in mint-green "thruster" puffs with dark claws.
"""
from __future__ import annotations

from modelkit import Model, Paint, hexc, sine

ARM = hexc("4e8f7b")
ARM_DARK = hexc("356a5a")
BAND = hexc("e3e9e6")
PUFF = (150, 240, 214, 255)       # glowing mint thrusters (RGBA = drawn unshaded, into the glow layer)
CLAW = hexc("2c3536")
BODY_GREEN = hexc("a6d69c")
BODY_WHITE = hexc("d9e3df")
TRIM = hexc("e6e2a2")
SPIRE = hexc("9aa7a6")
LEG = hexc("2b3333")
EYE = (250, 236, 120, 255)

SPECIES = "celesteela"
DEX_FOLDER = "0797_celesteela"
GROUP = "ce_celesteela"
FLIES = True


def tube(length):
    """Bamboo tube: green with white bands and a darker seam down the side."""
    def pat(face, u, v, fw, fh):
        if face in ("top", "bottom"):
            return ARM_DARK
        if v % 9 in (0, 1):
            return BAND
        if u == fw // 2 and face in ("left", "right"):
            return ARM_DARK
        return None
    return Paint(ARM, noise=0.05, pattern=pat, gradient=0.0)


def tier(colour, trim=False):
    def pat(face, u, v, fw, fh):
        if trim and v == fh - 1 and face in ("front", "back", "left", "right"):
            return TRIM
        if face in ("front", "back", "left", "right") and u in (0, fw - 1):
            return BODY_WHITE if colour == BODY_GREEN else BODY_GREEN
        return None
    return Paint(colour, noise=0.04, pattern=pat)


def face_tier():
    """The tier with Celesteela's small glowing eyes on the front."""
    def pat(face, u, v, fw, fh):
        if face == "front" and v == 2 and u in (2, fw - 3):
            return EYE
        if face == "front" and v == 3 and u in (2, fw - 3):
            return (60, 70, 70)
        return None
    return Paint(BODY_WHITE, noise=0.04, pattern=pat)


def build():
    m = Model("celesteela", tex_width=128, seed=797)
    m.bone("celesteela")
    m.locator("root", "celesteela", (0, 0, 0))
    m.bone("body", "celesteela", (0, 12, 0))
    m.locator("middle", "body", (0, 20, 0))
    m.locator("target", "body", (0, 20, -6))

    # stepped pyramid body on a wide base
    m.box("body", (0, 9, 0), (14, 5, 14), tier(BODY_WHITE, trim=True))
    m.box("body", (0, 14, 0), (12, 5, 12), tier(BODY_GREEN, trim=True))
    m.box("body", (0, 19, 0), (10, 5, 10), face_tier())
    m.box("body", (0, 23.5, 0), (8, 4, 8), tier(BODY_GREEN))
    m.box("body", (0, 27, 0), (6, 3, 6), tier(BODY_WHITE))
    m.box("body", (0, 6, 0), (10, 1, 10), Paint(LEG, noise=0.05))
    for name, x, z in (("leg_front_right", -4, -4), ("leg_front_left", 4, -4),
                       ("leg_back_right", -4, 4), ("leg_back_left", 4, 4)):
        m.bone(name, "body", (x, 6, z))
        m.box(name, (x, 3.5, z), (2, 5, 2), Paint(LEG, noise=0.06))

    # head = the spire top (looked-at bone); tall banded antenna
    m.bone("head", "body", (0, 28.5, 0))
    m.locator("head", "head", (0, 31, -3))
    m.box("head", (0, 30.5, 0), (4, 3, 4), Paint(SPIRE, noise=0.05))
    m.box("head", (0, 42, 0), (2, 20, 2), Paint(SPIRE, noise=0.05,
          pattern=lambda f, u, v, fw, fh: BAND if v % 5 == 0 else None))
    m.box("head", (0, 52.5, 0), (1, 3, 1), Paint(BAND, noise=0.03))
    for y in (36, 44):
        m.box("head", (0, y, 0), (4, 1, 4), Paint(BAND, noise=0.03))
    m.locator("top", "head", (0, 54, 0))

    # the two great arm tubes: from the shoulders near the top, splaying down and out, thruster at the end
    for side in (-1, 1):
        name = "arm_right" if side < 0 else "arm_left"
        bones = m.chain(name, "body", (side * 3, 30, 0),
                        [(20, 8, 8, (0, 0, side * 145)), (20, 8, 8, (0, 0, -side * 12))], tube(20))
        tip = bones[-1]
        # the chain's second segment starts at y=50 in its own (unrotated) frame and is 20 long: tip at y=70
        m.box(tip, (side * 3, 72, 0), (11, 4, 11), Paint(PUFF[:3], noise=0.08,
              pattern=lambda f, u, v, fw, fh: PUFF if (u + v) % 3 else None, emissive=True))
        m.box(tip, (side * 3, 70.5, 0), (9, 1, 9), Paint(BAND, noise=0.03))
        for cx, cz in ((-3, -3), (3, -3), (0, 3)):
            m.cube(tip, (side * 3 + cx - 1, 74, cz - 1), (2, 5, 2), Paint(CLAW, noise=0.06),
                   rotation=(cz * 6, 0, cx * 6), pivot=(side * 3 + cx, 74, cz))
    return m


def shiny_recolour(rgb):
    """Shiny palette (my take): white-silver tubes with pale-rose bands and a rose-gold body."""
    r, g, b = rgb
    if g > r + 15 and g > b - 10:        # greens -> silver / rose
        lum = (r + g + b) / 3
        return (min(255, int(lum * 1.25)), int(lum * 1.05), int(lum * 1.1))
    return rgb


def animations():
    hover = {
        "body": {"position": [0, sine(1.2, 90), 0]},
        "arm_left": {"rotation": [0, 0, sine(1.5, 90, 40)]},
        "arm_right": {"rotation": [0, 0, sine(-1.5, 90, 40)]},
        "head": {"rotation": [0, sine(4, 45), 0]},
    }
    return {
        "ground_idle": hover,
        "air_idle": hover,
        "air_fly": {
            "body": {"rotation": [10, 0, 0], "position": [0, sine(0.6, 180), 0]},
            "arm_left": {"rotation": [0, 0, sine(1, 180)]},
            "arm_right": {"rotation": [0, 0, sine(-1, 180)]},
        },
    }
