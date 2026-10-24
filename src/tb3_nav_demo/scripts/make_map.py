#!/usr/bin/env python3
"""Regenerate the occupancy image from the collision boxes in arena.sdf."""

from pathlib import Path


RESOLUTION = 0.05
SIZE = 160
OBSTACLES = [
    (-4.0, 4.0, -4.0, -3.8),
    (-4.0, 4.0, 3.8, 4.0),
    (-4.0, -3.8, -4.0, 4.0),
    (3.8, 4.0, -4.0, 4.0),
    (-0.85, -0.15, -1.0, 1.0),
    (0.7, 1.7, 0.65, 1.35),
]


def main():
    # PGM rows start at the top; map coordinates start at the lower left.
    pixels = bytearray()
    for row in range(SIZE - 1, -1, -1):
        y = -4.0 + (row + 0.5) * RESOLUTION
        for col in range(SIZE):
            x = -4.0 + (col + 0.5) * RESOLUTION
            occupied = any(x0 <= x <= x1 and y0 <= y <= y1 for x0, x1, y0, y1 in OBSTACLES)
            pixels.append(0 if occupied else 254)
    target = Path(__file__).resolve().parents[1] / 'maps' / 'arena.pgm'
    target.write_bytes(f'P5\n{SIZE} {SIZE}\n255\n'.encode() + pixels)


if __name__ == '__main__':
    main()
