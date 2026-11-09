"""Sprigatito line (Grass -> Fire, Meowscarada Fire/Fairy): natural disaster, an ember storm. Floragato's flower bud and
vine are fire blossoms, Meowscarada's spiked cape tips burn."""
from __future__ import annotations

from _materials import Charred, Flame

LINE = ["sprigatito", "floragato", "meowscarada"]
RECOLOUR = {"dst": 15, "dst_shiny": 40, "width": 55}


def build(kit):
    kit.layer("flames", frames=4, fps=8)
    fire, burnt = Flame("flames"), Charred("flames")
    kit.reskin(fire, *kit.named("flower", "vine", "head_fur", "tail_fur"), *kit.named("fur_back", contains="spike"))
    kit.reskin(burnt, *kit.named("fur_coat", "head_ruff", "neck_ruff", "neck_fur"))
