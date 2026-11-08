"""
Iron Boulder (#1022), the futuristic paradox of Terrakion. A built-from-scratch model in Cobblemon's style.

Design (after the official art): a sturdy, horse-like quadruped. Pale-grey armoured body and legs,
a big black head block with a white face plate and a glowing orange visor, two glowing orange crescent
blades sweeping up from the sides of the head, black spiky "mane" tufts on top, orange bands round the
legs above black hooves, and an orange blade for a tail.
"""
from __future__ import annotations

from modelkit import Model, Paint, hexc, mix, shade

GREY = hexc("b9b7ba")
GREY_DARK = hexc("8e8b90")
GREY_UNDER = hexc("6c696e")
BLACK = hexc("2a2427")
BLACK_HI = hexc("3e3539")
WHITE = hexc("eeedef")
ORANGE = hexc("f38b1f")
ORANGE_HI = hexc("ffc94d")
ORANGE_LO = hexc("c2560f")
HOOF = hexc("1c1a1d")
GLOW = (255, 196, 80, 255)   # RGBA patterns are drawn unshaded and also go into the glow layer


def panel_lines(base, line):
    """Armour panelling: a darker seam every few pixels."""
    def pat(face, u, v, fw, fh):
        if face in ("front", "back", "left", "right") and (u % 6 == 5 or v == fh - 1):
            return line
        if face == "top" and (u % 6 == 5 or v % 7 == 6):
            return line
        if face == "bottom":
            return GREY_UNDER
        return None
    return Paint(base, noise=0.04, pattern=pat)


def face_plate():
    """White face, orange visor band with dark eye slits, dark mouth line."""
    def pat(face, u, v, fw, fh):
        if face != "front":
            return BLACK if face == "top" else WHITE
        if v in (1, 2) and 1 <= u <= fw - 2:
            # visor: a shallow V, glowing
            eye = (u in (2, 3) or u in (fw - 4, fw - 3)) and v == 2
            return (40, 20, 10, 255) if eye else GLOW
        if v == fh - 2 and 3 <= u <= fw - 4:
            return hexc("8a8890")
        return None
    return Paint(WHITE, noise=0.03, pattern=pat)


def blade():
    """Orange crescent blade with a hot yellow inner edge; all of it glows."""
    def pat(face, u, v, fw, fh):
        if face in ("front", "back"):
            return (255, 214, 96, 255) if u == 0 else (243, 139, 31, 255)   # hot inner edge
        return (226, 112, 24, 255)
    return Paint(ORANGE, noise=0.04, pattern=pat, emissive=True)


def leg_band():
    def pat(face, u, v, fw, fh):
        return (255, 170, 60, 255) if v == 0 else None
    return Paint(ORANGE, noise=0.04, pattern=pat, emissive=True)


def build():
    m = Model("ironboulder", tex_width=128, seed=1022)
    m.bone("ironboulder")
    m.locator("root", "ironboulder", (0, 0, 0))
    m.bone("body", "ironboulder", (0, 15, 2))
    m.locator("middle", "body", (0, 16, 2))
    m.locator("target", "body", (0, 17, -6))

    # torso: chest block at the front, longer back section, raised withers behind the head
    m.box("body", (0, 16.5, -3), (13, 10, 10), panel_lines(GREY, GREY_DARK))
    m.box("body", (0, 16, 7), (12, 9, 10), panel_lines(GREY, GREY_DARK))
    m.box("body", (0, 21.5, 1), (10, 2, 8), Paint(GREY_DARK, noise=0.05))
    # belly plate
    m.box("body", (0, 11.5, 2), (10, 1, 16), Paint(GREY_UNDER, noise=0.05))

    # back blade (a swept orange fin on the rump) and the tail blade
    m.chain("tail", "body", (0, 19, 11.5), [(4, 1, 3, (-55, 0, 0)), (4, 1, 3, (-15, 0, 0)), (3, 1, 2, (-10, 0, 0)),
                                            (2, 1, 1, (-5, 0, 0))], blade())

    # head: the big black block, face plate, mane tufts and crescent blades
    m.bone("neck", "body", (0, 20, -6))
    m.box("neck", (0, 21, -7), (9, 6, 5), Paint(BLACK, noise=0.06))
    m.bone("head", "neck", (0, 22, -9))
    m.locator("head", "head", (0, 27, -15))
    m.box("head", (0, 24.5, -12), (13, 11, 11), Paint(BLACK, noise=0.07,
          pattern=lambda f, u, v, fw, fh: BLACK_HI if (f == "top" and (u + v) % 5 == 0) else None))
    m.box("head", (0, 22.5, -17.75), (11, 7, 1), face_plate())
    m.box("head", (0, 19.5, -16), (7, 2, 4), Paint(WHITE, noise=0.03))      # muzzle
    m.box("head", (0, 30.5, -11), (7, 1, 7), Paint(BLACK_HI, noise=0.05))   # brow ridge
    # spiky "ear" tufts: two black spiky clusters on top of the head, plus a small one between
    for side in (-1, 1):
        m.chain(f"tuft_{'right' if side < 0 else 'left'}", "head", (side * 4.5, 29.5, -12),
                [(4, 4, 4, (-10, 0, side * 20)), (3, 3, 3, (-15, 0, side * 15)), (3, 2, 2, (-20, 0, side * 10))],
                Paint(BLACK, noise=0.09, pattern=lambda f, u, v, fw, fh: BLACK_HI if (u + v) % 3 == 0 else None))
    m.chain("tuft_mid", "head", (0, 29.5, -8), [(3, 3, 3, (-40, 0, 0)), (2, 2, 2, (-20, 0, 0))], Paint(BLACK, noise=0.08))
    # crescent blades: one flowing blade per side, sweeping out from the cheek and curling up and back
    for side in (-1, 1):
        name = "horn_right" if side < 0 else "horn_left"
        m.chain(name, "head", (side * 6.5, 21, -13),
                [(4, 4, 1, (0, 0, side * 60)), (4, 4, 1, (6, 0, -side * 22)), (4, 3, 1, (8, 0, -side * 22)),
                 (3, 3, 1, (10, 0, -side * 18)), (3, 2, 1, (10, 0, -side * 12))], blade())

    # legs: grey upper, orange band, grey lower, black hoof
    for name, x, z in (("leg_front_right", -4, -5), ("leg_front_left", 4, -5),
                       ("leg_back_right", -4, 9), ("leg_back_left", 4, 9)):
        m.bone(name, "body", (x, 12, z))
        m.box(name, (x, 8.5, z), (4, 7, 4), panel_lines(GREY, GREY_DARK))
        m.box(name, (x, 5, z), (5, 2, 5), leg_band())
        m.box(name, (x, 3.0, z), (4, 2, 4), Paint(GREY, noise=0.04))
        m.box(name, (x, 1, z), (5, 2, 5), Paint(HOOF, noise=0.06))
    m.locator("top", "head", (0, 38, -12))
    return m


def shiny_recolour(rgb):
    """Shiny palette (my take): gunmetal body and glowing cyan blades instead of orange."""
    r, g, b = rgb
    if r > 180 and g < 200 and b < 120:          # orange / yellow -> cyan
        return (min(255, b + 40), min(255, g + 30), min(255, r))
    if abs(r - g) < 20 and abs(g - b) < 20 and r > 90:   # pale greys -> gunmetal
        return (int(r * 0.62), int(g * 0.66), int(b * 0.72))
    return rgb


SPECIES = "ironboulder"
DEX_FOLDER = "1022_ironboulder"
GROUP = "ce_ironboulder"


def animations():
    from modelkit import sine
    return {
        "ground_idle": {
            "body": {"position": [0, sine(0.25, 120), 0]},
            "head": {"rotation": [sine(2, 120, 30), 0, 0]},
            "tail": {"rotation": [sine(3, 90), sine(8, 60), 0]},
            "horn_left1": {"rotation": [0, 0, sine(2, 120)]},
            "horn_right1": {"rotation": [0, 0, sine(-2, 120)]},
        },
    }
