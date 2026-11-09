"""Shared helpers for new-Pokémon builders: JSON output and Bedrock animation keyframes."""
from __future__ import annotations

import json
import math
from pathlib import Path


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1) + "\n")


def track(length, fn, steps=None):
    """{time: [x, y, z]} keyframes of fn(t in 0..1) over `length` seconds."""
    steps = steps or max(4, int(round(length * 8)))
    out = {}
    for s in range(steps + 1):
        t = s / steps
        out[f"{round(t * length, 4)}"] = [round(float(v), 3) for v in fn(t)]
    return out


def keys(points):
    """{time: [x, y, z]} from [(time, [x, y, z]), ...] (linear between them)."""
    return {f"{round(t, 4)}": [round(float(v), 3) for v in xyz] for t, xyz in points}


def sin(t, cycles=1, phase=0.0):
    return math.sin(2 * math.pi * (cycles * t + phase))
