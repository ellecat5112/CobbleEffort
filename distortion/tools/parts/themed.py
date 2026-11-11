"""Every Pokémon without a hand-made look (Gen 1 in 0.9.0, the rest of the Pokédex in 0.12.0): each Pokémon (and each regional / Gigantamax form) takes
the look of its NEW types (parts/_themes.py: a brawler for Fighting, sea life for Water, overgrowth for Grass, flames
for Fire, rock for Ground, a third eye for Psychic, lightning for Electric, shadow wisps for Dark, feathered wings for
Flying, petals for Fairy, steel plates for Steel), and its main colour moves to the new primary type's colour."""
from __future__ import annotations

import colorsys
import json
from pathlib import Path

import _themes

_LINES = json.loads((Path(__file__).parent / "themed_lines.json").read_text())
LINE = [sp for line in _LINES for sp in line]

TYPE_COLOUR = {"normal": (168, 167, 122), "fire": (238, 129, 48), "water": (99, 144, 240), "grass": (122, 199, 76),
               "electric": (247, 208, 44), "ice": (150, 217, 214), "fighting": (194, 46, 40), "poison": (163, 62, 161),
               "ground": (226, 191, 101), "flying": (169, 143, 243), "psychic": (249, 85, 135), "bug": (166, 185, 26),
               "rock": (182, 161, 54), "ghost": (115, 87, 151), "dragon": (111, 53, 252), "dark": (112, 87, 70),
               "steel": (183, 183, 206), "fairy": (214, 133, 173)}


def _hue(t):
    return round(colorsys.rgb_to_hsv(*(c / 255 for c in TYPE_COLOUR[t]))[0] * 360)


def RECOLOUR(kit):
    """The main colour (the old primary type's, or for a Normal type its most saturated) to the new primary type's."""
    new = kit.new_types[0]
    rc = {"dst": _hue(new), "dst_shiny": (_hue(new) + 40) % 360, "width": 55, "fallback": True}
    if new in ("dark", "steel", "ground"):
        rc.update(sat=0.6, val=0.85)                       # muted types: less saturated
    if kit.old_types[0] == "normal":
        rc["near"] = None
    return rc


def build(kit):
    try:
        _themes.apply(kit)
    except KeyError:
        raise
    except Exception as e:                                     # a model the motifs don't fit: recoloured only
        raise KeyError(f"{kit.model}: {e}")
