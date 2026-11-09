"""Scorbunny line (Fire -> Water): sea life, the sea bunny (Jorunna parva, a fluffy white sea slug): dark speckles over
the white fur and a frilly gill tuft on the back; Cinderace's flames are anemone tentacles and the glow goes."""
from __future__ import annotations

from _materials import ANEMONE, Cutout, sealife_from_layers, speckles, tentacles

LINE = ["scorbunny", "raboot", "cinderace"]
RECOLOUR = {"dst": 205, "dst_shiny": 250, "width": 50}


GILLS = Cutout(tentacles(5), [(200, 170, 70), (246, 226, 140), (255, 252, 226)], [(140, 170, 220), (200, 220, 250), (250, 252, 255)])


def build(kit):
    kit.op(sealife_from_layers(ramp=ANEMONE))
    kit.op(speckles())
    kit.drop_layers.add("emissive")
    lo, hi = kit.bbox("torso")
    size = (hi[1] - lo[1]) * 0.55
    kit.cross("torso", (0, lo[1] + (hi[1] - lo[1]) * 0.35, hi[2] - 0.3), size, size, GILLS)
