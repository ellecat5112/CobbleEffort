"""Sobble line (Water -> Grass): plant inspiration, leaves. The fins and Drizzile's hair are leaves, and Inteleon's head
fin and long tail fins are a trail of leaves."""
from __future__ import annotations

from _materials import LEAF_RAMP, Remap

LINE = ["sobble", "drizzile", "inteleon"]
RECOLOUR = {"dst": 110, "dst_shiny": 80, "width": 55}


def build(kit):
    kit.reskin(Remap(*LEAF_RAMP), *kit.named("fin", "hair", "head_fin", "tail_fin", "neck_fin"))
