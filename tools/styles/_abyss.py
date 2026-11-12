"""
Bioluminescent Deep Sea collection: dark abyssal bodies with living light.

Looks (one per line, three lines each):
  anglerfish     near-black and warty, a glowing lure above the head, pale teeth-glow round the mouth line
  jellyfish      pale violet bell with glowing radial canals spreading from the chest and a glowing rim
  lanternfish    dark silver-blue with rows of cyan photophores along the belly and flanks
  comb_jelly     glassy pale blue with eight comb rows of rainbow light that ripple along the body
  firefly_squid  deep blue speckled all over with tiny bright blue lights that twinkle
  dragonfish     velvet black with a red light under each eye and red-glowing spots in a line down the body
Every look: glowing eyes, and an emissive animated layer (LIGHT) where its lights pulse in the dark.
Shiny: the lights' colours turned round the colour wheel.
"""
from __future__ import annotations

import numpy as np

from ._cosmic import centre_of, even, hue_turn_fast, noise, outline, ramp
from ._fx import make as _make

LIGHT = {"name": "light", "emissive": True, "translucent": True, "frames": 4, "fps": 4}
ABYSS = even([(2, 4, 10), (8, 18, 34), (20, 40, 64), (50, 80, 110)])


def paint(look, c):
    rng, u = c.rng, c.u
    mottle = noise(c.h, c.w, 6 * u, rng, 2)
    turn = 0.45 if c.shiny else 0.0
    col = lambda rgb: hue_turn_fast(np.array(rgb, np.float32)[None, None], turn)[0, 0] if turn else np.array(rgb, np.float32)
    eye_col = col((200, 240, 255))
    if look == "anglerfish":
        rgb = ramp(even([(4, 3, 3), (24, 16, 14), (52, 38, 32)]), c.lum * 0.7 + mottle * 0.3)
        warts = (rng.random((c.h, c.w)) < 0.02) & c.alpha
        rgb = np.where(warts[..., None], rgb * 1.8 + 10, rgb)
        lure = np.zeros_like(c.alpha)
        if c.face.ok and c.face.front:                          # the lure hangs over the forehead
            x, y, w, h = c.face.front
            cx, cy = x + w / 2, y + max(1.5 * u, h * 0.18)
        else:
            cx, cy, _ = centre_of(c.face, c.alpha)
        d = np.sqrt((c.xx - cx) ** 2 + (c.yy - cy) ** 2)
        lure = (d <= 2.0 * u) & c.alpha & ~c.eye
        halo = (d <= 4.0 * u) & c.alpha & ~c.eye
        rgb = np.where(lure[..., None], col((255, 250, 200)), rgb)
        c.shine(halo, col((255, 220, 120)), 0.6)
        c.shine(lure, col((255, 250, 200)), 1.0)
        eye_col = col((255, 230, 150))
    elif look == "jellyfish":
        rgb = ramp(even([(30, 16, 60), (110, 70, 160), (210, 170, 240), (250, 230, 255)]), c.lum * 0.5 + 0.35 + mottle * 0.2)
        cx, cy, r = centre_of(c.face, c.alpha)
        th = np.arctan2(c.yy - cy, c.xx - cx)
        canal = (np.abs(np.sin(th * 4)) < 0.12) & c.alpha
        rim = outline(c.alpha, u, 30 * u * u)
        rgb = np.where((canal | rim)[..., None], col((255, 180, 240)), rgb)
        c.shine(canal, col((255, 150, 240)), 0.85)
        c.shine(rim, col((180, 230, 255)), 0.9)
    elif look == "lanternfish":
        rgb = ramp(even([(6, 10, 20), (30, 44, 66), (90, 110, 140), (170, 190, 210)]), c.lum * 0.75 + mottle * 0.25)
        rows = ((c.yy // (3 * u)) % 2 == 0) & ((c.xx % (3 * u)) < u) & ((c.yy % (3 * u)) < u)
        dots = rows & (c.hm < 0.55) & c.alpha & ~c.eye
        rgb = np.where(dots[..., None], col((140, 250, 255)), rgb)
        c.shine(dots, col((120, 240, 255)), 1.0)
    elif look == "comb_jelly":
        rgb = ramp(even([(10, 30, 60), (40, 100, 150), (120, 190, 225), (210, 240, 255)]), c.lum * 0.4 + 0.2 + mottle * 0.25)
        stripe = ((c.xx // u) % 8 == 0) & c.alpha & ~c.eye
        rgb = np.where(stripe[..., None], np.array([250, 250, 255], np.float32), rgb)
        c.shine(stripe, (255, 255, 255), 1.0)
        c.extra["rainbow"] = True
    elif look == "firefly_squid":
        rgb = ramp(even([(4, 8, 30), (14, 30, 80), (40, 70, 140)]), c.lum * 0.7 + mottle * 0.3)
        dots = (rng.random((c.h, c.w)) < 0.05) & c.alpha & ~c.eye
        rgb = np.where(dots[..., None], col((120, 180, 255)), rgb)
        c.shine(dots, col((100, 170, 255)), 1.0)
        c.extra["twinkle"] = True
    elif look == "dragonfish":
        rgb = ramp(even([(0, 0, 2), (10, 8, 14), (28, 24, 34)]), c.lum * 0.6 + mottle * 0.2)
        spots = np.zeros_like(c.alpha)
        if c.face.ok and c.face.front:
            x, y, w, h = c.face.front
            for sx in (x + w // 4, x + 3 * w // 4):
                d = np.sqrt((c.xx - sx) ** 2 + (c.yy - (y + h * 0.65)) ** 2)
                spots |= (d <= 1.2 * u) & c.alpha
        line = (np.abs(c.hm - 0.45) < 0.02) & ((c.xx // u) % 3 == 0) & c.alpha
        rgb = np.where((spots | line)[..., None], col((255, 60, 50)), rgb)
        c.shine(spots, col((255, 50, 40)), 1.0)
        c.shine(line, col((255, 70, 60)), 0.8)
        eye_col = col((255, 120, 100))
    else:
        rgb = c.a[..., :3]
    rgb = np.where(c.eye[..., None], eye_col, rgb)
    c.shine(c.eye, eye_col, 1.0)
    return rgb


def animate(glow, frame, c):
    if c.extra.get("rainbow"):                                 # the comb rows' rainbow ripples along
        hue = ((c.yy / (6.0 * c.u)) + frame / 4.0) % 1.0
        r = 0.5 + 0.5 * np.cos(2 * np.pi * (hue + 0.0))
        g = 0.5 + 0.5 * np.cos(2 * np.pi * (hue + 0.33))
        b = 0.5 + 0.5 * np.cos(2 * np.pi * (hue + 0.67))
        c.glow_rgb = np.where((glow > 0)[..., None] & ~c.eye[..., None], np.stack([r, g, b], -1) * 255, c.glow_rgb)
        return glow
    if c.extra.get("twinkle"):
        rng = np.random.default_rng(c.seed + frame)
        return np.where(c.eye, glow, glow * (rng.random(glow.shape) < 0.6))
    return np.where(c.eye, glow, glow * [1.0, 0.8, 0.6, 0.8][frame % 4])


def make(look):
    return _make(paint, look, animate)
