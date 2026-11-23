# ASGT India Premium Emblem

Mathematically generated SVG emblem for ASGT India brand identity.

## Files

- `generate_emblem.py` — Python script that produces the SVG
- `asgt-premium-emblem.svg` — Generated master SVG (1000×1000 px)

The SVG is also deployed to `docs/asgt-emblem.svg` for the live website.

## How to edit and regenerate

Modify `generate_emblem.py`, then run:

```
python f:\EXIM\assets\branding\emblem\generate_emblem.py
```

After regenerating, copy to docs/:

```
copy f:\EXIM\assets\branding\emblem\asgt-premium-emblem.svg f:\EXIM\docs\asgt-emblem.svg
```

## Key dimensions (1000×1000 viewBox)

| Element              | Value                              |
|----------------------|------------------------------------|
| Canvas               | 1000 × 1000 px                     |
| Center               | CX=500, CY=500                     |
| Outer gold ring      | r=480 (gold) / r=455 (navy cutout) |
| Ornamental diamonds  | 72 diamonds at r=467, 7px half     |
| Main navy circle     | r=445                              |
| Inner gold rings     | r=445 (stroke 6px), r=420 (3px)    |
| Wheat stem start     | (540, 440) → (400, 190)            |
| Wheat control point  | (620, 310)                         |
| Ashoka Chakra center | (500, 490)                         |
| Chakra outer radius  | r=185 (gold rim)                   |
| Chakra spokes        | 24 × 15° spacing, r=34→173         |
| Hub                  | r=32 (navy), r=10 (white dot)      |
| Arrow base           | (370, 570) — gold circle r=22      |
| Arrow tip            | (610, 300)                         |
| Arrow control pt     | (450, 320)                         |
| Arrow shaft width    | 22px stroke                        |
| Arrowhead            | 80px long, 55px wide               |

## Colors

| Token      | Hex       |
|------------|-----------|
| Navy       | `#0F2747` |
| Gold       | `#D4A24A` |
| White      | `#FFFFFF` |
| Navy dark  | `#0a1d33` |

## Design layers (bottom to top)

1. Outer gold ring (annulus r=455–480)
2. 72 navy ornamental diamonds at r=467
3. Navy filled circle r=445
4. Inner gold ring strokes
5. Right wheat branch (curved stem + 7 leaves) + mirrored left
6. Bottom lotus motif (5 upward petals)
7. Ashoka Chakra (white disc, navy ring, 24 white spokes, navy hub)
8. Gold growth arrow (curved, lower-left to upper-right, ~1:30 direction)
