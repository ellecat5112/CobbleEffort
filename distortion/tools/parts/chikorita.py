"""Chikorita line (Grass -> Fire): natural disaster, a volcanic eruption. Chikorita's leaf is a plume of fire, Bayleef's
neck buds are glowing magma bombs, Meganium's petals are cooled lava cracked with glowing seams and its antennae burn."""
from __future__ import annotations

from _materials import Flame, Glow, LavaRock

LINE = ["chikorita", "bayleef", "meganium"]
RECOLOUR = {"dst": 22, "dst_shiny": 48, "width": 60}       # leaf green -> ember orange


def build(kit):
    kit.layer("flames", frames=4, fps=8)
    if kit.model == "chikorita":
        kit.reskin(Flame("flames"), *kit.named("leaf"))
    elif kit.model == "bayleef":
        kit.reskin(Glow("flames"), *kit.named("leaf"))
        kit.reskin(Flame("flames"), *kit.named("head_leaf"))
    else:
        kit.reskin(LavaRock("flames", crack=0.22), *kit.named("leaf"))
        kit.reskin(Flame("flames"), *kit.named("antenna"))
        lo, hi = kit.bbox("neck")                          # the eruption: flames burst up round the neck from the lava petals
        cx, cz = (lo[0] + hi[0]) / 2, (lo[2] + hi[2]) / 2
        for dx, dz, h, turn in ((-7, -2, 12, 20), (7, -3, 11, -25), (-5, 6, 10, 50), (5, 6, 13, -40), (0, -9, 10, 0)):
            kit.cross("torso", (cx + dx, 24.5, cz + dz), h * 0.6, h, Flame("flames", tongues=1.2), turn=turn)
