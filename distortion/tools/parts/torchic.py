"""Torchic line (Fire -> Water, Combusken/Blaziken Water/Psychic): sea life, a coral reef. The head feathers are
branching coral, the fluff is sea foam, Blaziken's wrist and ankle flames are fins and its long crest is kelp."""
from __future__ import annotations

from _materials import Remap

LINE = ["torchic", "combusken", "blaziken"]
RECOLOUR = {"dst": 205, "dst_shiny": 240, "width": 50}      # orange -> sea blue
CORAL = Remap([(150, 50, 76), (246, 126, 120), (255, 214, 196)], [(80, 60, 160), (170, 140, 240), (236, 226, 255)])
FOAM = Remap([(110, 170, 196), (196, 236, 248), (255, 255, 255)], [(150, 140, 200), (220, 214, 248), (255, 255, 255)])
FIN = Remap([(20, 86, 150), (70, 186, 220), (190, 248, 255)], [(70, 40, 140), (150, 110, 230), (230, 210, 255)])
KELP = Remap([(40, 72, 38), (92, 132, 60), (176, 194, 104)], [(40, 70, 90), (80, 130, 150), (160, 200, 200)])


def build(kit):
    kit.reskin(CORAL, *kit.named("comb"))
    kit.reskin(FOAM, *kit.named("fluff", "body_fluff"))
    if kit.model.startswith("blaziken"):
        kit.reskin(FIN, *kit.named("hand_fire", "foot_fire"))
        kit.reskin(KELP, *kit.named("hair"))
