"""
Pokemon Unite collection: Pokemon in holowear outfits in team colours (inspired by Pokemon Unite's holowear; original
patterns). Regular = purple team, shiny = orange team.

Looks (one per line, three lines each):
  jersey    a team jersey with white side bands and dark shorts
  holowear  dark navy with a glowing team-colour hex grid
  concert   a stage outfit glittering with team-colour sequins that sparkle
  formal    a black tuxedo with a white shirt front and a team-colour bow tie
  festival  a team-colour yukata printed with white waves and an obi
  beach     a team-colour Hawaiian shirt with white and yellow flowers
"""
from __future__ import annotations

import numpy as np

from ._cosmic import even, noise, ramp
from ._fx import make as _make
from ._sakura import flower

HOLO = {"name": "holo", "emissive": True, "translucent": True, "frames": 4, "fps": 5}


def fabric(c, colour, k=0.45):
    return np.asarray(colour, np.float32) * (1 - k / 2 + k * c.lum[..., None])


def paint(look, c):
    rng, u = c.rng, c.u
    body = c.alpha & ~c.eye
    team = np.array([250, 140, 30] if c.shiny else [120, 60, 210], np.float32)
    glow_m = np.zeros_like(c.alpha)
    if look == "jersey":
        rgb = np.where((c.hm > 0.3)[..., None], fabric(c, team), fabric(c, (34, 34, 44)))
        band = ((np.abs(c.hm - 0.62) < 0.025) | (np.abs(c.hm - 0.52) < 0.012)) & body
        rgb = np.where(band[..., None], fabric(c, (246, 246, 246)), rgb)
        if c.face.torso:
            x, y, w, h = c.face.torso
            num = (np.abs(c.xx - (x + w / 2)) <= max(0.6, 0.4 * u)) & (c.yy >= y + h * 0.25) & (c.yy <= y + h * 0.7) & body
            rgb = np.where(num[..., None], np.array([250, 250, 250], np.float32), rgb)
    elif look == "holowear":
        rgb = fabric(c, (16, 20, 44), 0.6)
        g = 4 * u
        row = c.yy // g
        lx = (c.xx + (row % 2) * g / 2) % g
        ly = c.yy % g
        hexl = ((lx < max(1, u // 2)) | (ly < max(1, u // 2))) & body
        rgb = np.where(hexl[..., None], team * 0.8 + 40, rgb)
        glow_m = hexl
    elif look == "concert":
        rgb = ramp(even([(14, 10, 20), (40, 30, 60), (80, 60, 110)]), c.lum * 0.5 + noise(c.h, c.w, 6 * u, rng, 2) * 0.4)
        seq = (((c.xx + c.yy) % 3) == 0) & (((c.xx - c.yy) % 3) == 0) & body
        rgb = np.where(seq[..., None], team * 1.1 + 20, rgb)
        glow_m = seq
    elif look == "formal":
        rgb = fabric(c, (20, 20, 24), 0.6)
        if c.face.torso:
            x, y, w, h = c.face.torso
            shirt = (np.abs(c.xx - (x + w / 2)) <= w * 0.22) & (c.yy >= y) & (c.yy <= y + h) & body
            rgb = np.where(shirt[..., None], fabric(c, (246, 246, 242), 0.3), rgb)
            by = y + max(1, u)
            bow = (np.abs(c.yy - by) <= max(0.6, 0.6 * u)) & (np.abs(c.xx - (x + w / 2)) <= max(1.5, 1.6 * u) *
                                                                 (0.4 + np.abs(c.xx - (x + w / 2)) / max(1.5, 1.6 * u))) & body
            rgb = np.where(bow[..., None], team, rgb)
    elif look == "festival":
        rgb = fabric(c, team)
        wave = (np.abs(np.sin(c.xx / (1.5 * u) + np.sin(c.yy / (2.0 * u)) * 1.5)) < 0.22) & body
        rgb = np.where(wave[..., None], fabric(c, (246, 246, 250), 0.3), rgb)
        obi = (np.abs(c.hm - 0.48) < 0.045) & body
        rgb = np.where(obi[..., None], fabric(c, (240, 200, 70)), rgb)
    elif look == "beach":
        rgb = fabric(c, team)
        ys, xs = np.nonzero(body)
        for i in range(max(3, int(c.alpha.sum() / float(u * u) / 90))):
            if len(xs) == 0:
                break
            k = rng.integers(len(xs))
            p, cc = flower(c, xs[k], ys[k], max(2.2, rng.uniform(1.2, 2.0) * u))
            rgb = np.where((p & body)[..., None], np.array([250, 250, 246] if i % 2 else [250, 220, 70], np.float32), rgb)
            rgb = np.where((cc & body)[..., None], np.array([240, 120, 40], np.float32), rgb)
    else:
        rgb = c.a[..., :3]
    rgb = np.where(c.eye[..., None], c.a[..., :3], rgb)
    c.extra["glow_m"], c.extra["team"] = glow_m & body, team
    c.extra["static"] = (c.glow.copy(), c.glow_rgb.copy())
    return rgb


def animate(glow, frame, c):
    g0, rgb0 = c.extra["static"]
    m = c.extra["glow_m"]
    rng = np.random.default_rng((c.seed * 3011 + frame * 53) % (2 ** 32))
    s = np.where(rng.random(m.shape) < 0.5, 0.8, 0.35)
    c.glow_rgb = np.where(m[..., None], c.extra["team"] * 0.7 + 76, rgb0)
    return np.where(m, s, g0)


def make(look):
    return _make(paint, look, animate, paint_layers=True)
