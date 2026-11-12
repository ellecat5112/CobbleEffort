"""
Undertale collection: Pokemon in the monochrome style of an underground RPG, each carrying a human SOUL (inspired by
Undertale; no game art copied).

Looks (one per line, three lines each), by the colour of the SOUL:
  determination  red: a red SOUL heart and save-point sparkles
  bravery        orange: orange pellets
  justice        yellow: little yellow stars
  kindness       green: green plus-sign heals
  patience       cyan: cyan rope bands
  integrity      blue: blue diamonds
Every look: the body in dithered black, grey and white like the game's sprites, a white battle-box outline round the
main parts, a SOUL heart on the chest that glows and beats, and white eyes.
Shiny: the SOUL colours turned round the colour wheel.
"""
from __future__ import annotations

import numpy as np

from ._cosmic import centre_of, hue_turn_fast, outline
from ._fx import make as _make

SOUL = {"name": "soul", "emissive": True, "translucent": True, "frames": 4, "fps": 4}
COLOURS = {"determination": (255, 20, 30), "bravery": (255, 150, 20), "justice": (255, 236, 40),
           "kindness": (40, 230, 60), "patience": (60, 230, 255), "integrity": (40, 80, 255)}
BAYER = np.array([[0, 2], [3, 1]], np.float32) / 4.0


def heart(c, x, y, R):
    """A heart shape of half-width R centred at (x, y)."""
    X = (c.xx - x) / R
    Y = -(c.yy - y) / R + 0.25
    return (X * X + Y * Y - 1) ** 3 - X * X * Y ** 3 <= 0


def paint(look, c):
    rng, u = c.rng, c.u
    body = c.alpha & ~c.eye
    soul = np.array(COLOURS[look], np.float32)
    if c.shiny:
        soul = hue_turn_fast(soul[None, None], 0.45)[0, 0]
    # dithered three-tone monochrome
    th = BAYER[(c.yy.astype(int) // max(1, u // 2)) % 2, (c.xx.astype(int) // max(1, u // 2)) % 2]
    v = np.clip(c.lum * 1.15, 0, 1) * 2 + th - 0.5
    tone = np.clip(np.floor(v + 0.5), 0, 2)
    rgb = np.array([16, 16, 16], np.float32)[None, None] + tone[..., None] * np.array([100, 100, 100], np.float32)
    box = outline(c.alpha, max(1, u // 2), 40 * u * u) & body
    rgb = np.where(box[..., None], np.array([250, 250, 250], np.float32), rgb)
    marks = np.zeros_like(c.alpha)
    g = 6 * u
    lx, ly = (c.xx % g) - g / 2, (c.yy % g) - g / 2
    shift = ((c.xx // g + c.yy // g) % 2) == 0
    if look == "determination":
        marks = ((np.abs(lx) <= max(0.5, 0.3 * u)) & (np.abs(ly) <= 1.0 * u) |
                 (np.abs(ly) <= max(0.5, 0.3 * u)) & (np.abs(lx) <= 1.0 * u)) & shift
    elif look == "bravery":
        marks = (np.hypot(lx, ly) <= max(0.8, 0.8 * u)) & shift
    elif look == "justice":
        r, a = np.hypot(lx, ly), np.arctan2(ly, lx) + np.pi / 2
        marks = (r <= 1.4 * u * (0.5 + 0.5 * np.abs(np.cos(2.5 * a)) ** 2)) & shift
    elif look == "kindness":
        marks = ((np.abs(lx) <= max(0.5, 0.35 * u)) & (np.abs(ly) <= 1.2 * u) |
                 (np.abs(ly) <= max(0.5, 0.35 * u)) & (np.abs(lx) <= 1.2 * u)) & shift
    elif look == "patience":
        marks = (np.abs(((c.hm * 10) % 1) - 0.5) < 0.06) & (((c.xx // max(1, u)) % 3) != 0)
    elif look == "integrity":
        marks = ((np.abs(lx) + np.abs(ly)) <= 1.3 * u) & shift
    marks &= body & ~box
    rgb = np.where(marks[..., None], soul, rgb)
    cx, cy, r = centre_of(c.face, c.alpha)
    sh = heart(c, cx, cy, max(2.0, min(r * 0.6, 3.0 * u))) & body
    rgb = np.where(sh[..., None], soul, rgb)
    c.shine(sh, soul, 1.0)
    c.shine(marks, soul, 0.45)
    rgb = np.where(c.eye[..., None], np.array([250, 250, 250], np.float32), rgb)
    c.shine(c.eye, (255, 255, 255), 0.7)
    c.extra["soul"] = sh
    return rgb


def animate(glow, frame, c):
    return np.where(c.extra["soul"], glow * [1.0, 0.55, 1.0, 0.75][frame % 4], glow)       # a heartbeat


def make(look):
    return _make(paint, look, animate, paint_layers=True)
