"""
Sunburst collection: Pokemon blazing with sunlight.

Looks (one per line, three lines each):
  rays         gold and orange sun rays bursting outward from the chest
  sunrise      a sunrise from toe to head: rose, orange, gold and pale morning yellow
  solar_flare  molten gold with a corona of flares licking off the top and edges
  sunflower    sunflower gold: petals radiating round a brown seed head on the chest
  art_deco     black lacquer with gold art-deco sunburst fans and arcs
  tropical     hot tropical orange and yellow, sun-bleached highlights and little sun motifs
Every look: warm glowing eyes and an emissive animated layer (SUNLIGHT) where the light shimmers.
Shiny: a white-gold midnight sun (cool silvery light).
"""
from __future__ import annotations

import math

import numpy as np

from ._cosmic import centre_of, edges, even, hue_turn_fast, noise, ramp
from ._fx import make as _make

SUNLIGHT = {"name": "sunlight", "emissive": True, "translucent": True, "frames": 4, "fps": 4}


def warm(c, colour, k=0.5):
    return np.asarray(colour, np.float32) * (1 - k / 2 + k * c.lum[..., None])


def paint(look, c):
    rng, u = c.rng, c.u
    body = c.alpha & ~c.eye
    cx, cy, r = centre_of(c.face, c.alpha)
    th = np.arctan2(c.yy - cy, c.xx - cx)
    d = np.hypot(c.xx - cx, c.yy - cy)
    mottle = noise(c.h, c.w, 6 * u, rng, 2)
    glow_m = np.zeros_like(c.alpha)
    gcol = (255, 220, 120)
    if look == "rays":
        band = (np.floor((th + math.pi) / (2 * math.pi) * 16) % 2) == 0
        rgb = np.where(band[..., None], warm(c, (255, 204, 60)), warm(c, (238, 134, 30)))
        core = (d <= max(2 * u, min(r, 4 * u))) & body
        rgb = np.where(core[..., None], np.array([255, 246, 200], np.float32), rgb)
        glow_m = core | (band & body & (d < 8 * u))
    elif look == "sunrise":
        rgb = ramp([(0, (190, 50, 90)), (0.35, (240, 110, 50)), (0.7, (255, 196, 60)), (1, (255, 244, 190))], c.hm)
        rgb = rgb * (0.75 + 0.35 * c.lum[..., None])
        glow_m = (c.hm > 0.8) & body
    elif look == "solar_flare":
        rgb = ramp(even([(150, 50, 10), (236, 120, 20), (255, 200, 60), (255, 246, 200)]), c.lum * 0.5 + mottle * 0.4)
        glow_m = (edges(c.alpha, max(1, u)) | (c.hm > 0.78)) & body
        gcol = (255, 160, 40)
        c.extra["flare"] = True
    elif look == "sunflower":
        rgb = warm(c, (246, 196, 30))
        R1 = max(2 * u, min(r * 0.55, 4 * u))
        petals = (d > R1) & (d <= R1 * (1.9 + 0.5 * np.cos(12 * th))) & body
        rgb = np.where(petals[..., None], warm(c, (255, 220, 60), 0.3), rgb)
        seed = (d <= R1) & body
        dots = seed & (((c.xx + c.yy) % 2) == 0)
        rgb = np.where(seed[..., None], np.array([96, 56, 24], np.float32), rgb)
        rgb = np.where(dots[..., None], np.array([60, 34, 14], np.float32), rgb)
        glow_m = petals
    elif look == "art_deco":
        rgb = warm(c, (16, 14, 12), 0.6)
        cell = 8 * u
        lx, ly = (c.xx % cell) - cell / 2, (c.yy % cell) - cell                       # fans rise from each cell's foot
        a = np.arctan2(-ly, lx)
        rr = np.hypot(lx, ly)
        fan = (np.abs(((a / math.pi) * 9) % 1 - 0.5) > 0.42) & (rr < cell * 0.95)
        arcs = np.abs(rr - cell * 0.95) < max(0.6, 0.4 * u)
        gold = (fan | arcs) & body
        rgb = np.where(gold[..., None], warm(c, (226, 180, 70), 0.3), rgb)
        glow_m = gold
        gcol = (255, 210, 110)
    elif look == "tropical":
        rgb = ramp(even([(220, 80, 20), (250, 150, 30), (255, 214, 70)]), c.lum * 0.5 + mottle * 0.4)
        bleach = (mottle > 0.7) & body
        rgb = np.where(bleach[..., None], rgb * 0.7 + 255 * 0.3, rgb)
        suns = np.zeros_like(c.alpha)
        ys, xs = np.nonzero(body)
        for _ in range(max(2, int(c.alpha.sum() / float(u * u) / 150))):
            if len(xs) == 0:
                break
            k = rng.integers(len(xs))
            dd = np.hypot(c.xx - xs[k], c.yy - ys[k])
            tt = np.arctan2(c.yy - ys[k], c.xx - xs[k])
            suns |= (dd <= 0.9 * u) | ((dd <= 1.8 * u) & (np.cos(8 * tt) > 0.6))
        suns &= body
        rgb = np.where(suns[..., None], np.array([255, 250, 200], np.float32), rgb)
        glow_m = suns
    else:
        rgb = c.a[..., :3]
    if c.shiny:                                                                     # midnight sun: white gold
        lum = rgb.mean(-1, keepdims=True)
        rgb = lum * np.array([1.0, 1.0, 1.05], np.float32) * 0.85 + rgb * 0.15
        gcol = (230, 236, 255)
    eye = np.asarray(gcol, np.float32)
    rgb = np.where(c.eye[..., None], eye, rgb)
    c.shine(c.eye, eye, 1.0)
    c.shine(glow_m & body, gcol, 0.35)
    c.extra["glow_m"] = glow_m & body
    c.extra["gcol"] = np.asarray(gcol, np.float32)
    c.extra["static"] = (c.glow.copy(), c.glow_rgb.copy())
    return rgb


def animate(glow, frame, c):
    g0, rgb0 = c.extra["static"]
    g, grgb = g0.copy(), rgb0.copy()
    rng = np.random.default_rng((c.seed * 977 + frame * 61) % (2 ** 32))
    m = c.extra["glow_m"]
    shimmer = noise(c.h, c.w, max(1, c.u * 2), rng, 1)
    s = (0.4 + 0.5 * shimmer) if c.extra.get("flare") else (0.25 + 0.2 * shimmer)
    g = np.where(m, s, g)
    grgb = np.where(m[..., None], c.extra["gcol"], grgb)
    c.glow_rgb = grgb
    return g


def make(look):
    return _make(paint, look, animate, paint_layers=True)
