"""
LGBTQIA+ Pride collection: Pokemon wearing pride flags (the transgender flag has its own collection, #10).

Looks (one per line, three lines each), each flag's horizontal stripes running across the WHOLE body from head to toe
(WANTS_HEIGHTS), the original's light and shade kept inside each stripe, dark outlines kept dark:
  rainbow    the rainbow flag: red, orange, yellow, green, blue, violet
  bisexual   magenta, lavender and royal blue (2:1:2)
  pansexual  pink, yellow and cyan
  lesbian    dark orange, orange, white, pink and dark rose
  asexual    black, grey, white and purple
  nonbinary  yellow, white, purple and black
The eyes keep their own colours. Shiny: pastel glitter over the stripes, plus sparkles that twinkle in the dark.
"""
from __future__ import annotations

import numpy as np

from ._fx import make as _make

SPARKLE = {"name": "sparkle", "emissive": True, "translucent": True, "frames": 4, "fps": 4}
FLAGS = {
    "rainbow": [(228, 3, 3), (255, 140, 0), (255, 237, 0), (0, 128, 38), (36, 64, 142), (115, 41, 130)],
    "bisexual": [(214, 2, 112), (214, 2, 112), (155, 79, 150), (0, 56, 168), (0, 56, 168)],
    "pansexual": [(255, 33, 140), (255, 216, 0), (33, 177, 255)],
    "lesbian": [(213, 45, 0), (255, 154, 86), (255, 255, 255), (211, 98, 164), (163, 2, 98)],
    "asexual": [(20, 20, 20), (164, 164, 164), (255, 255, 255), (128, 0, 128)],
    "nonbinary": [(252, 244, 52), (255, 255, 255), (156, 89, 209), (44, 44, 44)],
}
OUTLINE = np.array([52, 40, 70], np.float32)


def paint(look, c):
    body = c.alpha & ~c.eye
    stripes = np.asarray(FLAGS[look], np.float32)
    n = len(stripes)
    idx = np.clip(((1 - c.hm) * n).astype(int), 0, n - 1)
    col = stripes[idx]
    dark = (c.lum < 0.12)[..., None]
    shade = (0.72 + 0.4 * c.lum)[..., None]
    lifted = np.where((col.max(-1, keepdims=True) < 60), col + 30 * c.lum[..., None], col * shade)   # black stripes keep detail
    rgb = np.where(dark, col * 0.3 + OUTLINE * 0.7, np.clip(lifted, 0, 255))
    if c.shiny:
        glit = (c.rng.random((c.h, c.w)) < 0.07)[..., None]
        rgb = np.where(glit, rgb * 0.4 + np.array([255, 240, 250], np.float32) * 0.6, rgb)
    rgb = np.where(c.eye[..., None], c.a[..., :3], rgb)
    c.extra["body"], c.extra["stripes"] = body, stripes
    return rgb


def animate(glow, frame, c):
    if not c.shiny:
        return glow
    rng = np.random.default_rng((c.seed * 131 + frame * 7) % (2 ** 32))
    m = c.extra["body"] & (rng.random(glow.shape) < 0.01)
    pick = c.extra["stripes"][rng.integers(len(c.extra["stripes"]), size=glow.shape)] * 0.5 + 127
    c.glow_rgb = np.where(m[..., None], pick, c.glow_rgb)
    return np.where(m, 0.9, glow)


def make(look):
    return _make(paint, look, animate, paint_layers=True)
