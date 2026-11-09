"""Ho-Oh (Fire/Flying -> Water/Electric): an aurora over the sea. Its red and gold turn sea blue, and its glowing
flames are the cold green and teal of an aurora."""
from __future__ import annotations

LINE = ["hooh"]
RECOLOUR = {"dst": 214, "dst_shiny": 250, "width": 60}
GLOW_DST = 160                    # the emissive glow turns aurora green-teal


def build(kit):
    if kit.model != "ho_oh":
        raise KeyError(kit.model)
    kit.used = True
