"""Shared pieces for the jellyfish Digimon girls Tesla Jellymon and Thetismon (CobbleEffort: Digital): ribbon
tentacles (`ribbon`) as chains of thin plates that fade into a coloured tip, and lightning sparks (`spark`)."""
from __future__ import annotations

import math

from _route import tone


def ribbon(m, bone, pts, width, shader):
    for p0, p1 in zip(pts, pts[1:]):
        dx, dy, dz = (p1[i] - p0[i] for i in range(3))
        L = math.sqrt(dx * dx + dy * dy + dz * dz)
        cx, cy, cz = ((p0[i] + p1[i]) / 2 for i in range(3))
        yaw = math.degrees(math.atan2(dx, dz))
        pitch = math.degrees(math.atan2(-dy, math.hypot(dx, dz)))
        m.box(bone, cx - width / 2, cy - 0.4, cz - L / 2 - 0.3, cx + width / 2, cy + 0.4, cz + L / 2 + 0.3, shader,
              rotation=(pitch, yaw, 0), pivot=(cx, cy, cz))


def spark(m, bone, c, size, shader, seed=0):
    x, y, z = c
    for j in range(4):
        a = seed * 1.7 + j * 1.3
        nx, ny = x + size * math.cos(a), y + size * math.sin(a)
        m.box(bone, min(x, nx) - 0.4, min(y, ny) - 0.4, z - 0.4, max(x, nx) + 0.4, max(y, ny) + 0.4, z + 0.4, shader)
        x, y = nx, ny
