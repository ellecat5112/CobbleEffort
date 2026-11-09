"""Fuecoco line (Fire -> Water, Skeledirge Water/Dark): sea life, deep-sea bioluminescence. The flames keep glowing,
but cold cyan, like an anglerfish's lure; Skeledirge's flame bird glows the same."""
from __future__ import annotations

LINE = ["fuecoco", "crocalor", "skeledirge"]
RECOLOUR = {"dst": 205, "dst_shiny": 250, "width": 50}
GLOW_DST = 186                    # the emissive layers' colours turn to this hue


def build(kit):
    kit.used = True               # recoloured glow only, on Cobblemon's own models
