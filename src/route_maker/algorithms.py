from random import Random
from typing import Final, NamedTuple
import random

DEFAULT_RNG_SEED: Final[int] = 2007

MIN_WALL_HEIGHT: Final[int] = 200
MAX_WALL_HEIGHT: Final[int] = 2000

MIN_WALL_WIDTH: Final[int] = 100
MAX_WALL_WIDTH: Final[int] = 2000

MIN_WEST_ANGLE: Final[int] = 15
MAX_WEST_ANGLE: Final[int] = 75
DEFAULT_WEST_ANGLE: Final[int] = 45

MIN_EAST_ANGLE: Final[int] = 105
MAX_EAST_ANGLE: Final[int] = 165
DEFAULT_EAST_ANGLE: Final[int] = 135

MIN_MIN_HOLD_DISTANCE: Final[int] = 20
MAX_MIN_HOLD_DISTANCE: Final[int] = 50
DEFAULT_MIN_HOLD_DISTANCE: Final[int] = 25

MIN_MAX_HOLD_DISTANCE: Final[int] = 50
MAX_MAX_HOLD_DISTANCE: Final[int] = 120
DEFAULT_MAX_HOLD_DISTANCE: Final[int] = 75

DEFAULT_START_DISTANCE: Final[int] = 50
DEFAULT_END_DISTANCE: Final[int] = 50

class Hold(NamedTuple):
    x: int
    y: int
    type: int

def generate_route(height, width, west_angle, east_angle, min_hold_distance, max_hold_distance):
    holds: list[Hold] = []

    # For testing, use an explicit seed value in order to make the run reproducible.
    # rng = random.Random(DEFAULT_RNG_SEED)
    rng = random.Random(None)

    while True:
        if len(holds) == 0:
            holds.append(Hold(x=rng.randint(0, width), y=rng.randint(0, DEFAULT_START_DISTANCE), type=rng.randint(0, 4)))
        else:
            last_hold = holds[-1]

            if height - last_hold.y < DEFAULT_END_DISTANCE:
                break

            holds.append(Hold(x=rng.randint(0, width), y=rng.randint(last_hold.y, last_hold.y + 50), type=rng.randint(0, 4)))

    return holds

def generate_svg_preview(height, width, west_angle, east_angle, min_hold_distance, max_hold_distance):
    sizeA = 200
    sizeB = 200
    canvas_w = width
    canvas_h = height

    rA = sizeA / 2
    rB = sizeB / 2
    cxA = canvas_w * 0.35
    cxB = canvas_w * 0.65
    cy = canvas_h * 0.5

    colorA = '#FF0000'
    colorB = '#00FF00'
    opacityA = 66
    opacityB = 66

    holds = generate_route(height, width, west_angle, east_angle, min_hold_distance, max_hold_distance)
    print(f"[DEBUG] holds: {holds}")

    svg = f"""<svg viewBox="0 0 {canvas_w} {canvas_h}" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" style="max-width:100%; max-height:100%;">
      <rect x="0" y="0" width="{canvas_w}" height="{canvas_h}" rx="12" fill="white" stroke="#e5e7eb" stroke-width="2"/>
      <rect x="0" y="0" width="{canvas_w}" height="{canvas_h}" rx="12" fill="#f8fafc" />
      <line x1="{canvas_w / 2}" y1="0" x2="{canvas_w / 2}" y2="{canvas_h}" stroke="#e5e7eb" stroke-dasharray="8 8" />
      <line x1="0" y1="{canvas_h / 2}" x2="{canvas_w}" y2="{canvas_h / 2}" stroke="#e5e7eb" stroke-dasharray="8 8" />
      <circle cx="{cxA}" cy="{cy}" r="{rA}" fill="{colorA}" fill-opacity="{opacityA / 100}" stroke="{colorA}" stroke-width="3" />
      <text x="{cxA}" y="{cy + 5}" text-anchor="middle" font-family="sans-serif" font-size="{max(12, rA / 3)}" font-weight="700" fill="black" opacity="0.7">A</text>
      <circle cx="{cxB}" cy="{cy}" r="{rB}" fill="{colorB}" fill-opacity="{opacityB / 100}" stroke="{colorB}" stroke-width="3" />
      <text x="{cxB}" y="{cy + 5}" text-anchor="middle" font-family="sans-serif" font-size="{max(12, rB / 3)}" font-weight="700" fill="black" opacity="0.7">B</text>
      <text x="12" y="20" font-family="monospace" font-size="12" fill="#64748b">{canvas_w} x {canvas_h}</text>
    </svg>"""
    return svg