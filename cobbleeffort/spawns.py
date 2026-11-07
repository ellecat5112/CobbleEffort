"""Spawn pool generation with friendly shorthands."""

from __future__ import annotations

from typing import Any

from .util import CobbleEffortError, as_list

BUCKETS = {"common": "common", "uncommon": "uncommon", "rare": "rare", "ultra-rare": "ultra-rare",
           "ultra_rare": "ultra-rare", "ultrarare": "ultra-rare", "legendary": "ultra-rare"}
POSITIONS = {"grounded": "grounded", "ground": "grounded", "land": "grounded",
             "submerged": "submerged", "underwater": "submerged", "water": "submerged",
             "surface": "surface", "water_surface": "surface", "seafloor": "seafloor",
             "lavafloor": "lavafloor", "fishing": "fishing"}
PRESETS = {"grounded": ["natural"], "submerged": ["underwater"], "surface": ["water_surface"],
           "seafloor": ["underwater"], "lavafloor": [], "fishing": []}


def biome_ref(b: str) -> str:
    b = b.strip()
    if b.startswith("#") or ":" in b:
        return b
    return f"#cobblemon:is_{b.lower().replace(' ', '_')}"


def build_spawns(spawn_cfg: Any, sid: str, species_ref: str, archetype: str, stage: int) -> dict | None:
    """Returns a spawn_pool_world file, or None if this Pokemon should not spawn."""
    if spawn_cfg is False or spawn_cfg == "none":
        return None
    if spawn_cfg in (None, True, "auto"):
        if stage > 0 and spawn_cfg is not True:
            return None  # evolved forms don't spawn unless asked
        spawn_cfg = {}
    elif isinstance(spawn_cfg, dict) and spawn_cfg.get("auto") and stage > 0:
        return None  # template block marked auto: only base forms spawn
    entries_cfg = spawn_cfg if isinstance(spawn_cfg, list) else [spawn_cfg]
    spawns = []
    for i, sc in enumerate(entries_cfg, start=1):
        if not isinstance(sc, dict):
            raise CobbleEffortError(f"spawn entries must be objects, got {sc!r}")
        default_pos = "submerged" if archetype == "swimmer" else "grounded"
        pos_raw = str(sc.get("where", sc.get("position", default_pos))).lower()
        pos = POSITIONS.get(pos_raw)
        if not pos:
            raise CobbleEffortError(f"Unknown spawn position '{pos_raw}'. Use: {', '.join(sorted(set(POSITIONS.values())))}")
        bucket_raw = str(sc.get("rarity", sc.get("bucket", "uncommon"))).lower()
        bucket = BUCKETS.get(bucket_raw)
        if not bucket:
            raise CobbleEffortError(f"Unknown spawn rarity '{bucket_raw}'. Use common/uncommon/rare/ultra-rare")
        biomes = [biome_ref(b) for b in as_list(sc.get("biomes", ["overworld"]))]
        cond: dict[str, Any] = {"biomes": biomes}
        time = str(sc.get("time", "any")).lower()
        if time not in ("any", "all", ""):
            cond["timeRange"] = time
        if sc.get("sky") or sc.get("needs_sky"):
            cond["canSeeSky"] = True
        weather = str(sc.get("weather", "")).lower()
        if weather in ("rain", "raining"):
            cond["isRaining"] = True
        elif weather in ("thunder", "storm"):
            cond["isThundering"] = True
        elif weather in ("clear",):
            cond["isRaining"] = False
        if "min_y" in sc:
            cond["minY"] = int(sc["min_y"])
        if "max_y" in sc:
            cond["maxY"] = int(sc["max_y"])
        if isinstance(sc.get("condition"), dict):
            cond.update(sc["condition"])
        levels = str(sc.get("levels", sc.get("level", "5-30" if stage == 0 else "20-45"))).replace(" ", "")
        entry: dict[str, Any] = {
            "id": f"{sid}-{i}",
            "pokemon": f"{species_ref} {sc['properties']}" if sc.get("properties") else species_ref,
            "presets": sc.get("presets", PRESETS[pos]),
            "type": "pokemon",
            "spawnablePositionType": pos,   # Cobblemon 1.7+
            "context": pos,                 # Cobblemon 1.6 (ignored by newer versions)
            "bucket": bucket,
            "level": levels,
            "weight": float(sc.get("weight", 6.0)),
            "condition": cond,
        }
        if isinstance(sc.get("anticondition"), dict):
            entry["anticondition"] = sc["anticondition"]
        spawns.append(entry)
    return {"enabled": True, "neededInstalledMods": [], "neededUninstalledMods": [], "spawns": spawns}
