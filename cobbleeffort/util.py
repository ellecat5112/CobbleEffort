"""Small shared helpers: lenient JSON loading, ids, number formatting."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class CobbleEffortError(Exception):
    """A user-facing error (bad config, unreadable model, ...)."""


def strip_json_comments(text: str) -> str:
    """Remove // and /* */ comments and trailing commas, respecting strings."""
    out = []
    i = 0
    n = len(text)
    in_str = False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append(c)
            i += 1
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "*":
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
            continue
        out.append(c)
        i += 1
    cleaned = "".join(out)
    # trailing commas before } or ]
    return re.sub(r",(\s*[}\]])", r"\1", cleaned)


def load_jsonc(path: Path) -> Any:
    """Load JSON that may contain comments / trailing commas."""
    try:
        text = Path(path).read_text(encoding="utf-8-sig")
    except OSError as e:
        raise CobbleEffortError(f"Cannot read {path}: {e}") from e
    try:
        return json.loads(strip_json_comments(text))
    except json.JSONDecodeError as e:
        raise CobbleEffortError(f"{path} is not valid JSON: {e}") from e


def write_json(path: Path, data: Any, indent: int = 2) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=indent, ensure_ascii=False) + "\n", encoding="utf-8")


def species_id(name: str) -> str:
    """Cobblemon species ids are lowercase alphanumerics (showdown style)."""
    sid = re.sub(r"[^a-z0-9]", "", name.lower())
    if not sid:
        raise CobbleEffortError(f"Cannot build a species id from name {name!r}")
    return sid


def namespace_id(text: str) -> str:
    """Resource namespaces: lowercase a-z0-9_ (we avoid '-' and '.' to be safe for mod ids)."""
    ns = re.sub(r"[^a-z0-9_]", "_", text.lower()).strip("_")
    ns = re.sub(r"_+", "_", ns)
    if not ns:
        ns = "custommons"
    if ns[0].isdigit():
        ns = "p" + ns
    return ns[:63]


def move_id(name: str) -> str:
    """'Flame Wheel' / 'flame-wheel' / "King's Shield" -> showdown id."""
    return re.sub(r"[^a-z0-9]", "", name.lower())


def qualify(ident: str, default_ns: str = "cobblemon") -> str:
    ident = ident.strip()
    if ident.startswith("#"):
        body = ident[1:]
        return ident if ":" in body else f"#{default_ns}:{body}"
    return ident if ":" in ident else f"{default_ns}:{ident}"


def num(v: float, places: int = 3) -> float | int:
    """Round for pretty JSON output (ints stay ints)."""
    r = round(float(v), places)
    if r == int(r):
        return int(r)
    return r


def fmt(v: float, places: int = 3) -> str:
    r = num(v, places)
    return str(r)


def as_list(v: Any) -> list:
    if v is None:
        return []
    if isinstance(v, (list, tuple)):
        return list(v)
    if isinstance(v, str):
        parts = [p.strip() for p in re.split(r"[,\n]", v)]
        return [p for p in parts if p]
    return [v]


def tokens(name: str) -> list[str]:
    """Split bone names into lowercase tokens: 'LeftLeg_front2' -> ['left','leg','front']."""
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", name)
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", s)
    parts = re.split(r"[^A-Za-z]+", s)
    return [p.lower() for p in parts if p]
