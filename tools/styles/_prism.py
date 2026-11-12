"""
Prismatic collection: Pokemon that split light into every colour.

Looks (one per line, three lines each):
  holo         silver holographic foil with rainbow sheen bands that slide across it
  spectrum     the full spectrum from head to toe, red at the feet to violet at the top
  facets       a cut crystal: facets each tinted a different hue, bright white facet edges
  opal         milky opal with flashes of play-of-colour that shift
  oil_slick    dark graphite with a swirling thin-film rainbow sheen
  prism_light  white glass with spectral beams of refracted light crossing it
Every look: rainbow-bright eyes and an emissive animated layer (SPECTRUM) where the colours shift round the wheel.
Shiny: black opal: a darker body that makes the colours blaze.
"""
from __future__ import annotations

import numpy as np

from ._cosmic import even, noise, ramp
from ._fx import make as _make


def rainbow(h):
    """Hue array (0..1) -> RGB array 0..255."""
    return np.stack([0.5 + 0.5 * np.cos(2 * np.pi * (h + o)) for o in (0.0, 0.67, 0.33)], -1) * 255


SPECTRUM = {"name": "spectrum", "emissive": True, "translucent": True, "frames": 4, "fps": 4}


def paint(look, c):
    rng, u = c.rng, c.u
    body = c.alpha & ~c.eye
    mottle = noise(c.h, c.w, 6 * u, rng, 3)
    dark = c.shiny
    lit = (0.7 + 0.45 * c.lum)[..., None]
    hue = None
    if look == "holo":
        base = ramp(even([(60, 62, 70), (150, 154, 166), (214, 218, 228), (250, 250, 255)]), c.lum * 0.6 + mottle * 0.3)
        hue = ((c.xx + c.yy) / (14.0 * u) + mottle * 0.5) % 1.0
        rgb = base * 0.78 + rainbow(hue) * 0.22
        strength = 0.15
    elif look == "spectrum":
        hue = (1 - c.hm) * 0.82
        rgb = rainbow(hue) * lit
        strength = 0.3
    elif look == "facets":
        from ._void import voronoi_cracks
        cells = noise(c.h, c.w, 7 * u, rng, 1)
        hue = (np.floor(cells * 6) / 6.0) % 1.0
        rgb = rainbow(hue) * 0.45 + 255 * 0.35 * c.lum[..., None] + 40
        edge = voronoi_cracks(c, rng, 7 * u) & body
        rgb = np.where(edge[..., None], np.array([255, 255, 255], np.float32), rgb)
        c.shine(edge, (255, 255, 255), 0.6)
        strength = 0.3
    elif look == "opal":
        base = ramp(even([(170, 186, 200), (214, 226, 236), (244, 248, 252)]), c.lum * 0.5 + mottle * 0.4)
        flecks = noise(c.h, c.w, 2 * u, rng, 1)
        hue = (flecks * 3) % 1.0
        play = (flecks > 0.6)[..., None]
        rgb = np.where(play, base * 0.45 + rainbow(hue) * 0.55, base)
        strength = 0.4
        body = body & (flecks > 0.6)
    elif look == "oil_slick":
        base = ramp(even([(10, 10, 14), (30, 30, 38), (60, 60, 70)]), c.lum * 0.6 + mottle * 0.3)
        film = noise(c.h, c.w, 8 * u, rng, 3)
        hue = (film * 4) % 1.0
        sheen = np.clip(np.sin(film * 18) * 0.5 + 0.5, 0, 1)[..., None]
        rgb = base * (1 - 0.5 * sheen) + rainbow(hue) * 0.5 * sheen
        strength = 0.3
    elif look == "prism_light":
        base = ramp(even([(186, 190, 200), (228, 232, 240), (252, 252, 255)]), c.lum * 0.6 + mottle * 0.25)
        beam = ((c.xx - c.yy * 0.6) / (10.0 * u)) % 1.0
        on = beam < 0.35
        hue = beam / 0.35
        rgb = np.where(on[..., None], base * 0.55 + rainbow(hue) * 0.45, base)
        strength = 0.45
        body = body & on
    else:
        rgb, strength = c.a[..., :3], 0.0
    if dark:                                                                        # black opal
        rgb = rgb * 0.5
        mean = rgb.mean(-1, keepdims=True)
        rgb = np.clip(mean + (rgb - mean) * 1.7, 0, 255)
    eye_h = (c.xx / (3.0 * u)) % 1.0
    rgb = np.where(c.eye[..., None], rainbow(eye_h) * 0.6 + 100, rgb)
    c.shine(c.eye, (255, 255, 255), 0.8)
    c.extra["hue"], c.extra["strength"], c.extra["body"] = hue, strength, body
    c.extra["static"] = (c.glow.copy(), c.glow_rgb.copy())
    return rgb


def animate(glow, frame, c):
    g0, rgb0 = c.extra["static"]
    g, grgb = g0.copy(), rgb0.copy()
    if c.extra["hue"] is not None and c.extra["strength"] > 0:
        h = (c.extra["hue"] + frame / 4.0) % 1.0
        m = c.extra["body"]
        g = np.where(m & (c.extra["strength"] > g), c.extra["strength"], g)
        grgb = np.where(m[..., None], rainbow(h), grgb)
    eye_h = (c.xx / (3.0 * c.u) + frame / 4.0) % 1.0
    grgb = np.where(c.eye[..., None], rainbow(eye_h), grgb)
    c.glow_rgb = grgb
    return g


def make(look):
    return _make(paint, look, animate, layer_alpha=190, paint_layers=True)
