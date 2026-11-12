"""
Pinkan Island collection: Pokemon turned pink by the island's Pinkan Berries (the anime's Pinkan Island).

Looks (one per line, three lines each):
  classic    the original recoloured in Pinkan pinks, light and dark kept
  berry      Pinkan pink with clusters of darker Pinkan Berries
  bubblegum  soft pastel bubblegum pink with white highlights
  hotpink    vivid magenta-pink
  coral      warm flamingo-coral pink
  jungle     pink with a print of Pinkan jungle leaves
Every look: the eyes keep their colour; tiny pink sparkles twinkle (GLEAM).
Shiny: lavender-pink instead of rose.
"""
from __future__ import annotations

import numpy as np

from ._cosmic import even, hue_turn_fast, noise, ramp
from ._fx import make as _make

GLEAM = {"name": "gleam", "emissive": True, "translucent": True, "frames": 4, "fps": 4}

PALETTES = {
    "classic": [(96, 16, 52), (200, 70, 130), (246, 150, 196), (255, 226, 240)],
    "berry": [(100, 18, 56), (206, 76, 136), (248, 156, 200), (255, 228, 242)],
    "bubblegum": [(170, 96, 140), (240, 160, 200), (255, 206, 230), (255, 244, 250)],
    "hotpink": [(90, 0, 50), (210, 16, 120), (255, 90, 176), (255, 200, 230)],
    "coral": [(120, 40, 44), (230, 100, 104), (255, 160, 150), (255, 226, 216)],
    "jungle": [(96, 20, 60), (196, 72, 132), (244, 146, 192), (255, 224, 240)],
}


def leaf_mask(c, rng):
    """Scattered pointed leaves (rotated ellipses with a midrib gap)."""
    m = np.zeros_like(c.alpha)
    ys, xs = np.nonzero(c.alpha & ~c.eye)
    for _ in range(max(3, int(c.alpha.sum() / float(c.u * c.u) / 70))):
        if len(xs) == 0:
            break
        k = rng.integers(len(xs))
        a = rng.uniform(0, np.pi)
        dx, dy = c.xx - xs[k], c.yy - ys[k]
        along = dx * np.cos(a) + dy * np.sin(a)
        across = -dx * np.sin(a) + dy * np.cos(a)
        L, W = 2.6 * c.u, 1.0 * c.u
        leaf = (along / L) ** 2 + (across / W) ** 2 <= 1
        rib = np.abs(across) < max(0.35, 0.15 * c.u)
        m |= leaf & ~rib
    return m


def paint(look, c):
    rng, u = c.rng, c.u
    body = c.alpha & ~c.eye
    turn = -0.1 if c.shiny else 0.0
    stops = [hue_turn_fast(np.array(p, np.float32)[None, None], turn)[0, 0] if turn else p for p in PALETTES[look]]
    lum = np.clip((c.lum - 0.5) * 1.25 + 0.5, 0, 1)                                 # a little more contrast
    rgb = ramp(even(stops), lum)
    if look == "berry":
        ys, xs = np.nonzero(body)
        for _ in range(max(3, int(c.alpha.sum() / float(u * u) / 120))):
            if len(xs) == 0:
                break
            k = rng.integers(len(xs))
            for dx, dy in ((0, 0), (1.3, 0.6), (-0.4, 1.4)):
                bx, by = xs[k] + dx * u, ys[k] + dy * u
                d = np.hypot(c.xx - bx, c.yy - by)
                berry = (d <= 0.9 * u) & body
                rgb = np.where(berry[..., None], np.array(stops[0], np.float32) * 1.4, rgb)
                hi = (np.hypot(c.xx - bx + 0.3 * u, c.yy - by + 0.3 * u) <= 0.3 * u) & berry
                rgb = np.where(hi[..., None], np.array([255, 230, 245], np.float32), rgb)
    elif look == "bubblegum":
        shine = (noise(c.h, c.w, 4 * u, rng, 2) > 0.75) & body
        rgb = np.where(shine[..., None], rgb * 0.6 + 255 * 0.4, rgb)
    elif look == "jungle":
        leaf = leaf_mask(c, rng) & body
        rgb = np.where(leaf[..., None], np.array(stops[1], np.float32) * 0.8, rgb)
    rgb = np.where(c.eye[..., None], c.a[..., :3], rgb)
    c.extra["body"] = body
    return rgb


def animate(glow, frame, c):
    rng = np.random.default_rng((c.seed * 911 + frame * 37) % (2 ** 32))
    spark = c.extra["body"] & (rng.random(glow.shape) < 0.008)
    c.glow_rgb = np.where(spark[..., None], np.array([255, 200, 235], np.float32), c.glow_rgb)
    return np.where(spark, 0.85, glow)


def make(look):
    return _make(paint, look, animate, paint_layers=True)
