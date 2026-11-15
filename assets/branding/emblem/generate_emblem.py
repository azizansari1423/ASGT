import math
import os

W, H = 1000, 1000
CX, CY = 500, 500

NAVY = "#0F2747"
GOLD = "#D4A24A"
WHITE = "#FFFFFF"
NAVY_DARK = "#0a1d33"

def pt(r, angle_deg, cx=CX, cy=CY):
    """Convert polar coords to SVG x,y"""
    a = math.radians(angle_deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)

def svg_line(x1, y1, x2, y2, color, width):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'

def svg_path(d, fill="none", stroke="none", sw=1):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'

parts = []
parts.append(f'<?xml version="1.0" encoding="UTF-8"?>')
parts.append(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" width="1000" height="1000">')

# ── 1. OUTER GOLD RING ──────────────────────────────────────────────
# Plain gold filled annulus (outer ring)
parts.append(f'<g id="outer-border">')
parts.append(f'<circle cx="{CX}" cy="{CY}" r="480" fill="{GOLD}"/>')
parts.append(f'<circle cx="{CX}" cy="{CY}" r="455" fill="{NAVY}"/>')
parts.append(f'</g>')

# ── 2. ORNAMENTAL PATTERN (diamonds around ring) ───────────────────
parts.append(f'<g id="ornamental-pattern">')
N_DIAMONDS = 72
for i in range(N_DIAMONDS):
    angle = (i / N_DIAMONDS) * 360
    # Diamond center at radius 467
    dx, dy = pt(467, angle)
    # Diamond: 4 points (up, right, down, left relative to center, then rotated)
    # Size: 11x11 diamond
    half = 7
    # Points in local coords rotated by angle
    a_rad = math.radians(angle)
    cos_a, sin_a = math.cos(a_rad), math.sin(a_rad)
    # 4 diamond corners in local: top(0,-h), right(h,0), bottom(0,h), left(-h,0)
    pts_local = [(0, -half), (half*0.65, 0), (0, half), (-half*0.65, 0)]
    pts_world = []
    for lx, ly in pts_local:
        wx = dx + lx * cos_a - ly * sin_a
        wy = dy + lx * sin_a + ly * cos_a
        pts_world.append(f"{wx:.1f},{wy:.1f}")
    pts_str = " ".join(pts_world)
    parts.append(f'  <polygon points="{pts_str}" fill="{NAVY}"/>')
parts.append(f'</g>')

# ── 3. MAIN NAVY CIRCLE ─────────────────────────────────────────────
parts.append(f'<circle cx="{CX}" cy="{CY}" r="445" fill="{NAVY}" id="navy-bg"/>')

# ── 4. INNER GOLD RING ──────────────────────────────────────────────
parts.append(f'<circle cx="{CX}" cy="{CY}" r="445" fill="none" stroke="{GOLD}" stroke-width="6" id="inner-ring-outer"/>')
parts.append(f'<circle cx="{CX}" cy="{CY}" r="420" fill="none" stroke="{GOLD}" stroke-width="3" id="inner-ring-inner"/>')

# ── 5. WHEAT BRANCHES (left and right, symmetrical) ─────────────────
# Each branch: curved stem + 7 pointed alternating leaves
# Right branch: stem from ~(530,440) curving to ~(390,210) along right side
# Left branch: mirror

def wheat_branch_right():
    lines = []
    # Stem: Bezier curve along right side of inner circle
    # From bottom-right area to top-right area
    sx, sy = 540, 440  # start
    ex, ey = 400, 190  # end
    cx1, cy1 = 620, 310  # control point
    stem_path = f"M {sx} {sy} Q {cx1} {cy1} {ex} {ey}"
    lines.append(svg_path(stem_path, stroke=GOLD, sw=5))

    # 7 leaves along the stem at t = 0.1, 0.2, ... 0.8
    # Approximate positions on the quadratic bezier
    # B(t) = (1-t)^2 * P0 + 2t(1-t) * P1 + t^2 * P2
    leaf_data = [
        # (t, leaf_angle_offset, leaf_size)
        (0.1, 25, 50, 15),   # t, outward_angle_offset, length, width
        (0.2, 30, 55, 16),
        (0.35, 35, 58, 17),
        (0.5, 40, 55, 16),
        (0.65, 42, 50, 15),
        (0.78, 38, 44, 13),
        (0.9, 32, 36, 11),
    ]

    for t, angle_off, llen, lwid in leaf_data:
        # Position on bezier
        bx = (1-t)**2 * sx + 2*t*(1-t)*cx1 + t**2 * ex
        by = (1-t)**2 * sy + 2*t*(1-t)*cy1 + t**2 * ey

        # Tangent direction of curve at t
        tx = 2*(1-t)*(cx1-sx) + 2*t*(ex-cx1)
        ty = 2*(1-t)*(cy1-sy) + 2*t*(ey-cy1)
        tangent_angle = math.degrees(math.atan2(ty, tx))

        # Leaf points outward (perpendicular to tangent + offset)
        leaf_angle = tangent_angle + 90 + angle_off
        leaf_a = math.radians(leaf_angle)

        # Leaf is a pointed ellipse shape (like a flame/almond)
        # Tip of leaf
        tip_x = bx + llen * math.cos(leaf_a)
        tip_y = by + llen * math.sin(leaf_a)

        # Leaf width control points (perpendicular to leaf direction)
        perp_a = leaf_a + math.pi/2
        ctrl_off = lwid * 0.4

        # Base of leaf (at stem)
        base_a = leaf_a + math.pi
        base_x = bx + 8 * math.cos(base_a)
        base_y = by + 8 * math.sin(base_a)

        # Side bulge points
        mid_x = bx + llen * 0.5 * math.cos(leaf_a)
        mid_y = by + llen * 0.5 * math.sin(leaf_a)
        lx = mid_x + lwid * 0.5 * math.cos(perp_a)
        ly = mid_y + lwid * 0.5 * math.sin(perp_a)
        rx = mid_x - lwid * 0.5 * math.cos(perp_a)
        ry = mid_y - lwid * 0.5 * math.sin(perp_a)

        leaf_path = (f"M {base_x:.1f} {base_y:.1f} "
                     f"Q {lx:.1f} {ly:.1f} {tip_x:.1f} {tip_y:.1f} "
                     f"Q {rx:.1f} {ry:.1f} {base_x:.1f} {base_y:.1f} Z")
        lines.append(svg_path(leaf_path, fill=GOLD))

    return "\n".join(lines)

def mirror_svg_horizontal(svg_content, cx=CX):
    """Mirror SVG content horizontally around cx"""
    return f'<g transform="scale(-1,1) translate({-2*cx},0)">{svg_content}</g>'

right_branch = wheat_branch_right()
left_branch = mirror_svg_horizontal(right_branch)

parts.append(f'<g id="agricultural-leaves">')
parts.append(right_branch)
parts.append(left_branch)
parts.append(f'</g>')

# ── 6. BOTTOM CROP MOTIF (lotus / wheat base) ──────────────────────
parts.append(f'<g id="bottom-crop-motif">')

# Central upright leaf
center_leaf = (f"M 500 650 "
               f"Q 520 590 500 530 "
               f"Q 480 590 500 650 Z")
parts.append(svg_path(center_leaf, fill=GOLD))

# Left leaf
left_leaf = (f"M 480 650 "
             f"Q 445 610 440 560 "
             f"Q 465 590 490 640 Z")
parts.append(svg_path(left_leaf, fill=GOLD))
# Mirror right
parts.append(f'<g transform="scale(-1,1) translate(-1000,0)">')
parts.append(svg_path(left_leaf, fill=GOLD))
parts.append(f'</g>')

# Outer left leaf
outer_left = (f"M 460 650 "
              f"Q 415 605 418 548 "
              f"Q 448 580 468 638 Z")
parts.append(svg_path(outer_left, fill=GOLD))
# Mirror right
parts.append(f'<g transform="scale(-1,1) translate(-1000,0)">')
parts.append(svg_path(outer_left, fill=GOLD))
parts.append(f'</g>')

parts.append(f'</g>')

# ── 7. ASHOKA CHAKRA ────────────────────────────────────────────────
CHAKRA_CX, CHAKRA_CY = 500, 490  # slightly above center
CHAKRA_R = 185  # outer rim
HUB_R = 32
SPOKE_INNER = HUB_R + 2
SPOKE_OUTER = CHAKRA_R - 2

parts.append(f'<g id="ashoka-chakra">')
# White disc background
parts.append(f'<circle cx="{CHAKRA_CX}" cy="{CHAKRA_CY}" r="{CHAKRA_R}" fill="{WHITE}"/>')
# Gold outer rim
parts.append(f'<circle cx="{CHAKRA_CX}" cy="{CHAKRA_CY}" r="{CHAKRA_R}" fill="none" stroke="{GOLD}" stroke-width="8"/>')
# Navy fill (ring area between spokes)
parts.append(f'<circle cx="{CHAKRA_CX}" cy="{CHAKRA_CY}" r="{CHAKRA_R-10}" fill="{NAVY}"/>')
# White inner disc (rim of chakra)
parts.append(f'<circle cx="{CHAKRA_CX}" cy="{CHAKRA_CY}" r="{CHAKRA_R-10}" fill="none" stroke="{WHITE}" stroke-width="3"/>')

# 24 spokes
for i in range(24):
    angle = i * 15  # 360/24 = 15 degrees
    x1, y1 = pt(SPOKE_INNER, angle, CHAKRA_CX, CHAKRA_CY)
    x2, y2 = pt(SPOKE_OUTER - 10, angle, CHAKRA_CX, CHAKRA_CY)
    parts.append(svg_line(x1, y1, x2, y2, WHITE, 4))

# Hub
parts.append(f'<circle cx="{CHAKRA_CX}" cy="{CHAKRA_CY}" r="{HUB_R}" fill="{NAVY}"/>')
parts.append(f'<circle cx="{CHAKRA_CX}" cy="{CHAKRA_CY}" r="{HUB_R}" fill="none" stroke="{WHITE}" stroke-width="4"/>')
parts.append(f'<circle cx="{CHAKRA_CX}" cy="{CHAKRA_CY}" r="10" fill="{WHITE}"/>')
parts.append(f'</g>')

# ── 8. GROWTH ARROW ─────────────────────────────────────────────────
# Large prominent gold arrow: starts lower-left of chakra center, curves to upper-right
# Reference shows arrow pointing ~1:30-2 o'clock (upper right)
# Base: circle at ~(380, 560), tip at ~(600, 310)
ARROW_BASE_X, ARROW_BASE_Y = 370, 570
ARROW_TIP_X, ARROW_TIP_Y = 610, 300

# Bezier control for slight curve
ARROW_CX1, ARROW_CY1 = 450, 320

# Arrow shaft width
SHAFT_W = 22

# Calculate shaft as a thick path with rounded base
# Direction vector
dx = ARROW_TIP_X - ARROW_BASE_X
dy = ARROW_TIP_Y - ARROW_BASE_Y
length = math.sqrt(dx**2 + dy**2)
# Unit vector
ux, uy = dx/length, dy/length
# Perpendicular
px, py = -uy, ux

# Arrowhead: 70px long, 50px wide
HEAD_LEN = 80
HEAD_WIDTH = 55
head_base_x = ARROW_TIP_X - ux * HEAD_LEN
head_base_y = ARROW_TIP_Y - uy * HEAD_LEN

# Shaft (curved using bezier for the visual)
# Simple approach: use a wide stroke on a curved path
arrow_path = (f"M {ARROW_BASE_X} {ARROW_BASE_Y} "
              f"Q {ARROW_CX1} {ARROW_CY1} {head_base_x:.1f} {head_base_y:.1f}")

parts.append(f'<g id="growth-arrow">')
# Shaft
parts.append(f'<path d="{arrow_path}" fill="none" stroke="{GOLD}" stroke-width="{SHAFT_W}" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')
# Arrowhead triangle
# Left wing, tip, right wing (of arrowhead)
lx = head_base_x + px * HEAD_WIDTH * 0.5
ly = head_base_y + py * HEAD_WIDTH * 0.5
rx = head_base_x - px * HEAD_WIDTH * 0.5
ry = head_base_y - py * HEAD_WIDTH * 0.5
parts.append(f'<polygon points="{ARROW_TIP_X:.1f},{ARROW_TIP_Y:.1f} {lx:.1f},{ly:.1f} {rx:.1f},{ry:.1f}" '
             f'fill="{GOLD}"/>')
# Circle at base of arrow
parts.append(f'<circle cx="{ARROW_BASE_X}" cy="{ARROW_BASE_Y}" r="22" fill="{GOLD}"/>')
parts.append(f'</g>')

# ── CLOSE SVG ───────────────────────────────────────────────────────
parts.append('</svg>')

svg_content = "\n".join(parts)

# Write SVG
os.makedirs(r"f:\EXIM\assets\branding\emblem", exist_ok=True)
svg_path_out = r"f:\EXIM\assets\branding\emblem\asgt-premium-emblem.svg"
with open(svg_path_out, "w", encoding="utf-8") as f:
    f.write(svg_content)
print(f"SVG written to {svg_path_out}")
print(f"SVG size: {len(svg_content)} bytes")

# Try to convert to PNG
try:
    import cairosvg
    png_path = r"f:\EXIM\assets\branding\emblem\asgt-premium-emblem.png"
    cairosvg.svg2png(url=svg_path_out, write_to=png_path, output_width=1000, output_height=1000)
    print(f"PNG written to {png_path}")
except ImportError:
    print("cairosvg not available, trying Pillow...")
    try:
        from PIL import Image
        # At minimum, note the limitation
        print("Pillow available but cannot convert SVG directly. Install cairosvg: pip install cairosvg")
    except ImportError:
        print("Neither cairosvg nor Pillow available.")
        print("Install with: pip install cairosvg")

print("Done.")
