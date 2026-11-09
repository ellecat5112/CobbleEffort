"""Mew (Psychic -> Normal/Fighting, a specialised distortion by the user's design): the unborn. Mew floats curled in a
translucent orb, the placenta, veined and pulsing like a heartbeat; its tail turns to the front as the umbilical cord,
joined to the orb's wall by the placenta's disc."""
from __future__ import annotations

from _materials import Cord, Membrane, Placenta

LINE = ["mew"]
RECOLOUR = "keep"


def build(kit):
    if kit.model != "mew":
        raise KeyError(kit.model)
    kit.layer("womb", emissive=False, translucent=True, frames=4, fps=3)
    # the cord: the first three tail segments, turned to the front and a little down; the rest of the tail is gone
    kit.hide(*[f"tail{i}" for i in range(4, 12)])
    kit.rotate_bone("tail", [-12, 180, 0])
    kit.reskin(Cord(), "tail", "tail2", "tail3")
    kit.bulk(0.35, "tail", "tail2", "tail3")
    lo, hi = kit.bbox("tail3")
    y = (lo[1] + hi[1]) / 2
    kit.plane("tail3", (0, y - 4, hi[2]), 8, 8, Placenta(), facing="z")
    # the orb: six membranes round the body (each painted as a disc, so together they read as a bubble)
    cx, cy, cz, r = 0.0, 9.5, 0.0, 16.0
    womb = Membrane("womb")
    kit.plane("body", (cx, cy - r, cz - r), 2 * r, 2 * r, womb, facing="z")
    kit.plane("body", (cx, cy - r, cz + r), 2 * r, 2 * r, womb, facing="z")
    kit.plane("body", (cx - r, cy - r, cz), 2 * r, 2 * r, womb, facing="x")
    kit.plane("body", (cx + r, cy - r, cz), 2 * r, 2 * r, womb, facing="x")
    kit.flat("body", (cx, cy + r, cz), 2 * r, 2 * r, womb)
    kit.flat("body", (cx, cy - r, cz), 2 * r, 2 * r, womb)
