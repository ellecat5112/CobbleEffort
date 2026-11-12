"""
Pajama collection: Pokemon ready for bed in soft printed sleepwear.

Looks (one per line, three lines each):
  stripes  classic sky-blue and white pinstripe pajamas
  polka    pink pajamas with white polka dots
  plaid    red flannel tartan
  moons    navy pajamas printed with yellow moons and glow-in-the-dark stars
  footie   a mint fleece footie onesie with a cream belly and grippy soles
  gingham  sunny yellow-and-white gingham check
Every look: soft flannel shading, a button placket down the chest and cuffs at the ankles.
Shiny: the fabric's colours turned round the colour wheel.
"""
from __future__ import annotations

import numpy as np

from ._cosmic import even, hue_turn_fast, noise, ramp
from ._fx import make as _make

GLOW = {"name": "glow", "emissive": True, "translucent": True, "frames": 4, "fps": 2}


def fabric(c, colour):
    """A fabric colour with soft shading from the original and a faint weave."""
    weave = (((c.xx + c.yy) % 2) == 0)[..., None] * 0.03
    return np.asarray(colour, np.float32) * (0.72 + 0.4 * c.lum[..., None] + weave)


def paint(look, c):
    rng, u = c.rng, c.u
    turn = 0.45 if c.shiny else 0.0
    col = lambda rgb: hue_turn_fast(np.array(rgb, np.float32)[None, None], turn)[0, 0] if turn else np.array(rgb, np.float32)
    body = c.alpha & ~c.eye
    if look == "stripes":
        st = ((c.xx // max(1, u)) % 4) < 2
        rgb = np.where(st[..., None], fabric(c, col((130, 186, 236))), fabric(c, (244, 246, 250)))
    elif look == "polka":
        g = 4 * u
        dot = np.hypot((c.xx % g) - g / 2, (c.yy % g) - g / 2) <= max(0.8, 0.9 * u)
        rgb = np.where(dot[..., None], fabric(c, (250, 248, 248)), fabric(c, col((240, 140, 180))))
    elif look == "plaid":
        a = ((c.xx // (2 * u)) % 4 == 0)
        b = ((c.yy // (2 * u)) % 4 == 0)
        base = fabric(c, col((190, 30, 36)))
        rgb = np.where((a | b)[..., None], base * 0.55, base)
        rgb = np.where((a & b)[..., None], base * 0.3, rgb)
        thin = ((c.xx % (8 * u)) == 4 * u) | ((c.yy % (8 * u)) == 4 * u)
        rgb = np.where(thin[..., None], fabric(c, (240, 200, 90)), rgb)
    elif look == "moons":
        rgb = fabric(c, col((30, 40, 96)))
        g = 7 * u
        lx, ly = (c.xx % g) - g / 2, (c.yy % g) - g / 2
        flip = ((c.xx // g + c.yy // g) % 2) == 0
        moon = (np.hypot(lx, ly) <= 1.6 * u) & ~(np.hypot(lx - 0.7 * u, ly - 0.4 * u) <= 1.3 * u) & flip
        star = ((np.abs(lx) <= max(0.5, 0.4 * u)) & (np.abs(ly) <= 1.0 * u) |
                (np.abs(ly) <= max(0.5, 0.4 * u)) & (np.abs(lx) <= 1.0 * u)) & ~flip
        rgb = np.where(moon[..., None], fabric(c, (250, 222, 110)), rgb)
        rgb = np.where(star[..., None], fabric(c, (236, 250, 210)), rgb)
        c.shine(star & body, (190, 255, 170), 0.9)                                 # glow-in-the-dark print
        c.shine(moon & body, (255, 230, 140), 0.35)
        c.extra["stars"] = star & body
    elif look == "footie":
        rgb = fabric(c, col((150, 222, 196)))
        if c.face.torso:
            x, y, w, h = c.face.torso
            belly = ((((c.xx - (x + w / 2)) / (w * 0.42)) ** 2 + ((c.yy - (y + h * 0.55)) / (h * 0.45)) ** 2) <= 1)
            rgb = np.where((belly & body)[..., None], fabric(c, (246, 238, 220)), rgb)
        sole = (c.hm < 0.06) & body
        grip = sole & (((c.xx % (2 * u)) == 0) & ((c.yy % (2 * u)) == 0))
        rgb = np.where(sole[..., None], fabric(c, (150, 150, 160)), rgb)
        rgb = np.where(grip[..., None], fabric(c, (90, 90, 100)), rgb)
    elif look == "gingham":
        a = ((c.xx // (2 * u)) % 2 == 0)
        b = ((c.yy // (2 * u)) % 2 == 0)
        y = col((246, 206, 60))
        rgb = np.where((a & b)[..., None], fabric(c, y),
                       np.where((a ^ b)[..., None], fabric(c, y * 0.5 + 125), fabric(c, (250, 250, 246))))
    else:
        rgb = c.a[..., :3]
    cuff = (c.hm < 0.1) & (c.hm >= 0.07) & body
    rgb = np.where(cuff[..., None], rgb * 0.82, rgb)
    if c.face.torso:                                                                # button placket down the chest
        x, y, w, h = c.face.torso
        mid = x + w / 2
        plk = (np.abs(c.xx - mid) <= max(0.5, 0.45 * u)) & (c.yy >= y) & (c.yy < y + h) & body
        rgb = np.where(plk[..., None], rgb * 0.85, rgb)
        step = max(2, int(h // 4))
        btn = plk & (((c.yy - y) % step) == step // 2) & (np.abs(c.xx - mid) <= max(0.5, 0.3 * u))
        rgb = np.where(btn[..., None], np.array([250, 248, 240], np.float32), rgb)
    rgb = np.where(c.eye[..., None], c.a[..., :3], rgb)
    c.extra["static"] = (c.glow.copy(), c.glow_rgb.copy())
    return rgb


def animate(glow, frame, c):
    if "stars" in c.extra:
        return np.where(c.extra["stars"], glow * [1.0, 0.85, 0.7, 0.85][frame % 4], glow)
    return glow


def make(look):
    return _make(paint, look, animate, paint_layers=True)
