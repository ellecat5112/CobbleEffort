"""PNG reading/writing and texture tricks (auto shiny, palette swaps).

Uses Pillow when it is installed; otherwise falls back to a small pure-Python
PNG codec so the tool works with a stock Python install.
"""

from __future__ import annotations

import base64
import colorsys
import struct
import zlib
from pathlib import Path

from .util import CobbleEffortError

try:  # optional
    from PIL import Image  # type: ignore
except Exception:  # pragma: no cover - depends on environment
    Image = None


class RGBAImage:
    """Minimal RGBA image: width, height, flat list of (r,g,b,a) tuples."""

    def __init__(self, width: int, height: int, pixels: list[tuple[int, int, int, int]]):
        self.width = width
        self.height = height
        self.pixels = pixels

    # ------------------------------------------------------------------ IO
    @classmethod
    def from_bytes(cls, data: bytes) -> "RGBAImage":
        if Image is not None:
            import io

            im = Image.open(io.BytesIO(data)).convert("RGBA")
            getter = getattr(im, "get_flattened_data", None) or im.getdata
            return cls(im.width, im.height, [tuple(p) for p in getter()])
        return _decode_png(data)

    @classmethod
    def load(cls, path: Path) -> "RGBAImage":
        try:
            return cls.from_bytes(Path(path).read_bytes())
        except CobbleEffortError:
            raise
        except Exception as e:
            raise CobbleEffortError(f"Could not read image {path}: {e}") from e

    def to_png_bytes(self) -> bytes:
        if Image is not None:
            import io

            im = Image.new("RGBA", (self.width, self.height))
            im.putdata(self.pixels)
            buf = io.BytesIO()
            im.save(buf, format="PNG")
            return buf.getvalue()
        return _encode_png(self)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(self.to_png_bytes())

    # ------------------------------------------------------------ effects
    def hue_shift(self, degrees: float, saturation: float = 1.0, brightness: float = 1.0) -> "RGBAImage":
        shift = (degrees % 360) / 360.0
        cache: dict[tuple[int, int, int], tuple[int, int, int]] = {}
        out = []
        for r, g, b, a in self.pixels:
            if a == 0:
                out.append((r, g, b, a))
                continue
            key = (r, g, b)
            res = cache.get(key)
            if res is None:
                h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
                h = (h + shift) % 1.0
                s = max(0.0, min(1.0, s * saturation))
                l = max(0.0, min(1.0, l * brightness))
                rr, gg, bb = colorsys.hls_to_rgb(h, l, s)
                res = (round(rr * 255), round(gg * 255), round(bb * 255))
                cache[key] = res
            out.append((*res, a))
        return RGBAImage(self.width, self.height, out)

    def palette_swap(self, mapping: dict[str, str], tolerance: int = 0) -> "RGBAImage":
        pairs = [(_hex(k), _hex(v)) for k, v in mapping.items()]
        out = []
        for r, g, b, a in self.pixels:
            for (fr, fg, fb), (tr, tg, tb) in pairs:
                if abs(r - fr) <= tolerance and abs(g - fg) <= tolerance and abs(b - fb) <= tolerance:
                    r, g, b = tr, tg, tb
                    break
            out.append((r, g, b, a))
        return RGBAImage(self.width, self.height, out)


def _hex(s: str) -> tuple[int, int, int]:
    s = s.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        raise CobbleEffortError(f"Bad colour {s!r}; use #RRGGBB")
    return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)


def decode_data_uri(uri: str) -> bytes | None:
    if not uri or not uri.startswith("data:"):
        return None
    try:
        _, payload = uri.split(",", 1)
        return base64.b64decode(payload)
    except Exception:
        return None


# ---------------------------------------------------------------- pure PNG

_PNG_SIG = b"\x89PNG\r\n\x1a\n"


def _decode_png(data: bytes) -> RGBAImage:
    if not data.startswith(_PNG_SIG):
        raise CobbleEffortError("Not a PNG file (install Pillow for other formats)")
    pos = 8
    width = height = bit_depth = color_type = interlace = 0
    palette: list[tuple[int, int, int]] = []
    trns: bytes = b""
    idat = bytearray()
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos : pos + 4])
        ctype = data[pos + 4 : pos + 8]
        chunk = data[pos + 8 : pos + 8 + length]
        pos += 12 + length
        if ctype == b"IHDR":
            width, height, bit_depth, color_type, _, _, interlace = struct.unpack(">IIBBBBB", chunk)
        elif ctype == b"PLTE":
            palette = [tuple(chunk[i : i + 3]) for i in range(0, len(chunk), 3)]  # type: ignore
        elif ctype == b"tRNS":
            trns = chunk
        elif ctype == b"IDAT":
            idat += chunk
        elif ctype == b"IEND":
            break
    if interlace:
        raise CobbleEffortError("Interlaced PNGs are not supported without Pillow; re-save without interlacing")
    if bit_depth not in (1, 2, 4, 8, 16):
        raise CobbleEffortError(f"Unsupported PNG bit depth {bit_depth}")
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[color_type]
    bits_pp = channels * bit_depth
    bpp = max(1, bits_pp // 8)
    stride = (width * bits_pp + 7) // 8
    raw = zlib.decompress(bytes(idat))
    rows: list[bytearray] = []
    prev = bytearray(stride)
    p = 0
    for _ in range(height):
        f = raw[p]
        line = bytearray(raw[p + 1 : p + 1 + stride])
        p += 1 + stride
        for i in range(stride):
            a = line[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if f == 1:
                line[i] = (line[i] + a) & 0xFF
            elif f == 2:
                line[i] = (line[i] + b) & 0xFF
            elif f == 3:
                line[i] = (line[i] + ((a + b) >> 1)) & 0xFF
            elif f == 4:
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pred = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pred) & 0xFF
        rows.append(line)
        prev = line

    def samples(line: bytearray) -> list[int]:
        if bit_depth == 8:
            return list(line)
        if bit_depth == 16:
            return [line[i] for i in range(0, len(line), 2)]
        out = []
        mask = (1 << bit_depth) - 1
        for byte in line:
            for shift in range(8 - bit_depth, -1, -bit_depth):
                out.append((byte >> shift) & mask)
        return out

    scale = 255 // ((1 << bit_depth) - 1) if bit_depth < 8 else 1
    pixels: list[tuple[int, int, int, int]] = []
    for line in rows:
        s = samples(line)
        for x in range(width):
            if color_type == 0:
                v = s[x] * (scale if bit_depth < 8 else 1)
                pixels.append((v, v, v, 255))
            elif color_type == 2:
                r, g, b = s[x * 3 : x * 3 + 3]
                pixels.append((r, g, b, 255))
            elif color_type == 3:
                idx = s[x]
                r, g, b = palette[idx] if idx < len(palette) else (0, 0, 0)
                a = trns[idx] if idx < len(trns) else 255
                pixels.append((r, g, b, a))
            elif color_type == 4:
                v, a = s[x * 2 : x * 2 + 2]
                pixels.append((v, v, v, a))
            else:
                r, g, b, a = s[x * 4 : x * 4 + 4]
                pixels.append((r, g, b, a))
    return RGBAImage(width, height, pixels)


def _encode_png(img: RGBAImage) -> bytes:
    raw = bytearray()
    w = img.width
    for y in range(img.height):
        raw.append(0)
        for r, g, b, a in img.pixels[y * w : (y + 1) * w]:
            raw += bytes((r, g, b, a))

    def chunk(t: bytes, body: bytes) -> bytes:
        return struct.pack(">I", len(body)) + t + body + struct.pack(">I", zlib.crc32(t + body) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", img.width, img.height, 8, 6, 0, 0, 0)
    return _PNG_SIG + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")
