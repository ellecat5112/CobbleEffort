"""validateData for the CobbleEffort: Digital tree (the core's Gradle task only reads src/main/resources): every JSON
parses, and every model, poser and texture its resolvers name is there (Cobblemon hangs at the loading screen on a
missing model)."""
from __future__ import annotations

import json
from pathlib import Path


def run(res: Path, mod: str):
    n = 0
    for f in res.rglob("*.json"):
        json.loads(f.read_text())
        n += 1
    bedrock = res / "assets" / mod / "bedrock" / "pokemon"
    models = {f.name.removesuffix(".json") for f in (bedrock / "models").rglob("*.json")}
    posers = {f.name.removesuffix(".json") for f in (bedrock / "posers").rglob("*.json")}
    refs = 0
    for f in (bedrock / "resolvers").rglob("*.json"):
        for v in json.loads(f.read_text())["variations"]:
            for key, have in (("model", models), ("poser", posers)):
                if v.get(key):
                    ns, name = v[key].split(":", 1)
                    if ns not in (mod, "cobblemon"):
                        raise SystemExit(f"{f.name} names another mod's {key} {v[key]}")
                    if ns == mod and name not in have:
                        raise SystemExit(f"{f.name} references missing {key} {v[key]}")
            texes = [v.get("texture")] + [l.get("texture") for l in v.get("layers", [])]
            for t in texes:
                for tex in ([t] if isinstance(t, str) else (t or {}).get("frames", [])):
                    ns, path = tex.split(":", 1)
                    if ns == mod and not (res / "assets" / ns / path).is_file():
                        raise SystemExit(f"{f.name} references missing texture {tex}")
                    refs += 1
    print(f"digital_check: {n} JSON files OK, {refs} texture references present, {len(models)} models")
