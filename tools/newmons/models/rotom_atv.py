"""ATV Rotom (Electric/Rock), after the Joseon Region fakemon art: Rotom inside an all-terrain quad bike. Four big
chunky black tyres with orange hubs, an orange body whose front fender is Rotom's face (two lens eyes, a wide grin
full of teeth) under a grey cone horn, black handlebars with grips, a black bumper frame, orange rear fenders and a
black seat. Sandy brown plasma crackles round it.

Front is -z, y is up. 16 units tall; about 1.1 blocks.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _rotomform import bolt_plane, cone, face_on, palette, solid, tyre, wheel

P = palette({"aura": (200, 160, 112), "aura_light": (246, 226, 196), "iris": (110, 196, 236)})
HEIGHT = 16
SCALE = round(1.1 * 16 / HEIGHT, 3)
HITBOX = [1.3, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "an all-terrain quad bike with chunky tyres and a grinning face on its front fender"


def build() -> Model:
    m = Model("rotom_atv")
    top = m.bone("rotom_atv", None, (0, 0, 0))
    body = m.bone("body", top, (0, 6, 0))
    for sx in (-1, 1):
        for zc in (-6.5, 6.5):                              # the four chunky tyres
            x0, x1 = (5, 9.5) if sx > 0 else (-9.5, -5)
            tyre(m, body, x0, x1, 4.5, zc, 4.5, wheel(P, centre=(0, 4.5, zc), r=4.5))
    m.box(body, -5, 5, -9, 5, 11, 9, solid(P, "orange"))                              # the body
    m.box(body, -6, 6, -12.5, 6, 13.5, -8.5,
          face_on(P, (0, 9.5, -12.5), eyes=[(-2.7, 1.8, 1.6), (2.7, 1.8, 1.6)], mouth=(0, -1.4, 8.5, 2.6, 7)))
    m.box(body, -9.6, 9, -11, 9.6, 10.5, -2.5, solid(P, "orange_light"))              # front fender over the tyres
    m.box(body, -9.6, 9, 2.5, 9.6, 10.5, 11, solid(P, "orange"))                      # rear fenders
    m.box(body, -3.5, 11, 1, 3.5, 12.5, 8, solid(P, "black"))                         # seat
    m.box(body, -5, 2.5, -13.6, 5, 4, -12.4, solid(P, "black"))                       # bumper frame
    for sx in (-1, 1):
        m.box(body, 4 * sx - 0.6, 2.5, -13.6, 4 * sx + 0.6, 7, -12.4, solid(P, "black"))
    cone(m, body, (0, 13.2, -10.5), (0, 1, -0.3), 3.0, 5.0, solid(P, "grey_light"))                # the cone horn
    hd = m.bone("head", body, (0, 12, -6))
    rod(m, hd, (0, 11, -6), (0, 15, -5), 1.2, solid(P, "black"), extend=0.5)
    m.box(hd, -7, 14.6, -5.8, 7, 15.8, -4.6, solid(P, "black"))                       # handlebars
    for sx in (-1, 1):
        m.box(hd, 6 * sx - 1, 14.3, -6, 6 * sx + 1, 16.1, -4.4, solid(P, "charcoal"))
    for x, y, z, w, h, pl, fl in [(-11, 6, -2, 6, 9, "zy", False), (11, 7, 1, 6, 8, "zy", True), (-6, 12, 10, 5, 8, "xy", False)]:
        bolt_plane(m, body, x, y, z, w, h, P, plane=pl, flip=fl)
    return m
