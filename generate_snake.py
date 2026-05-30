import os
import requests
import math

# ── Config ────────────────────────────────────────────────
USERNAME   = "DMadushanka"
OUTPUT_DIR = "dist"
DARK_FILE  = f"{OUTPUT_DIR}/github-contribution-grid-snake-dark.svg"
LIGHT_FILE = f"{OUTPUT_DIR}/github-contribution-grid-snake.svg"

CELL   = 11   # cell size px
GAP    = 3    # gap between cells
STEP   = CELL + GAP  # 14px per grid unit
RADIUS = 2    # cell corner radius
PAD_X  = 16  # left padding
PAD_Y  = 20  # top padding

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Fetch real contribution data ──────────────────────────
def fetch_weeks(username):
    token = os.getenv("GITHUB_TOKEN", "")
    headers = {"Authorization": f"bearer {token}"} if token else {}
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays {
                contributionCount
                color
                date
              }
            }
          }
        }
      }
    }
    """
    r = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": {"login": username}},
        headers=headers,
        timeout=15,
    )
    if r.status_code != 200:
        raise RuntimeError(f"GraphQL request failed: {r.status_code} {r.text}")
    data = r.json()
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]

# ── Build grid: list of (col, row, count, color) ─────────
def build_grid(weeks):
    cells = []
    for col, week in enumerate(weeks):
        for row, day in enumerate(week["contributionDays"]):
            cells.append((col, row, day["contributionCount"], day["color"]))
    return cells

# ── Build a boustrophedon (snake-path) through ALL cells ──
# The snake visits every column, alternating up/down direction.
def build_snake_path(num_cols, num_rows=7):
    path = []
    for col in range(num_cols):
        rows = range(num_rows) if col % 2 == 0 else range(num_rows - 1, -1, -1)
        for row in rows:
            path.append((col, row))
    return path

# ── Convert grid coord → pixel centre ────────────────────
def cx(col): return PAD_X + col * STEP + CELL // 2
def cy(row): return PAD_Y + row * STEP + CELL // 2

# ── Build SVG polyline points string ─────────────────────
def path_points(snake_path):
    return " ".join(f"{cx(c)},{cy(r)}" for c, r in snake_path)

# ── Snake body segments (head + N-1 body segments) ───────
SNAKE_LEN   = 8   # number of visible segments
SNAKE_COLOR = "#38bdf8"   # cyan head
BODY_COLORS = ["#60c8f5", "#82d4f7", "#a4dff9", "#c0eafb",
               "#d5f0fc", "#e5f6fd", "#f0faff"]  # fading tail

# ── Total animation duration ──────────────────────────────
# Each cell takes FRAME_MS ms, total = len(path) * FRAME_MS
FRAME_MS = 80  # ms per cell step → smooth but not too fast

def segment_animation(seg_idx, path_len, frame_ms, points_str):
    """
    Returns a <animateMotion> element that makes a segment follow
    the polyline path, but offset by seg_idx steps behind the head.
    """
    total_ms   = path_len * frame_ms
    delay_ms   = -seg_idx * frame_ms          # negative = pre-offset
    return (
        f'<animateMotion dur="{total_ms}ms" begin="{delay_ms}ms" '
        f'repeatCount="indefinite" rotate="auto" calcMode="linear">'
        f'<mpath href="#snake-path"/>'
        f'</animateMotion>'
    )

# ── Generate full SVG ─────────────────────────────────────
def make_svg(weeks, dark=True):
    cells      = build_grid(weeks)
    num_cols   = max(c for c, *_ in cells) + 1
    num_rows   = 7
    snake_path = build_snake_path(num_cols, num_rows)
    path_len   = len(snake_path)
    total_ms   = path_len * FRAME_MS

    svg_w = PAD_X * 2 + num_cols * STEP
    svg_h = PAD_Y * 2 + num_rows * STEP

    # Colour theme
    if dark:
        bg_col   = "#0d1117"
        empty_col= "#161b22"
    else:
        bg_col   = "#ffffff"
        empty_col= "#ebedf0"

    lines = []
    lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{svg_w}" height="{svg_h}" '
        f'viewBox="0 0 {svg_w} {svg_h}">'
    )

    # ── Defs: snake motion path + glow filter ──────────────
    pts = path_points(snake_path)
    lines.append('<defs>')
    lines.append(f'  <polyline id="snake-path" points="{pts}"/>')
    # Glow filter for head
    lines.append(
        '  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">'
        '<feGaussianBlur stdDeviation="2.5" result="blur"/>'
        '<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>'
        '</filter>'
    )
    lines.append('</defs>')

    # ── Background ──────────────────────────────────────────
    lines.append(f'<rect width="{svg_w}" height="{svg_h}" fill="{bg_col}"/>')

    # ── Contribution grid cells ─────────────────────────────
    # Build a lookup: (col, row) → color
    cell_map = {(c, r): (cnt, col) for c, r, cnt, col in cells}

    for (col, row), (cnt, color) in cell_map.items():
        x = PAD_X + col * STEP
        y = PAD_Y + row * STEP
        fill = color if cnt > 0 else empty_col
        lines.append(
            f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
            f'rx="{RADIUS}" fill="{fill}"/>'
        )

    # ── Snake segments (tail → head order so head renders on top) ──
    # Tail segments
    for seg in range(SNAKE_LEN - 1, 0, -1):
        alpha = 1.0 - seg / SNAKE_LEN
        idx   = min(seg - 1, len(BODY_COLORS) - 1)
        color = BODY_COLORS[idx]
        size  = max(4, CELL - seg)
        off   = (CELL - size) // 2
        anim  = segment_animation(seg, path_len, FRAME_MS, pts)
        lines.append(
            f'<rect width="{size}" height="{size}" rx="{RADIUS}" '
            f'fill="{color}" opacity="{alpha:.2f}" '
            f'transform="translate(-{off},-{off})">'
            f'{anim}</rect>'
        )

    # Head (with glow)
    head_anim = segment_animation(0, path_len, FRAME_MS, pts)
    lines.append(
        f'<rect width="{CELL}" height="{CELL}" rx="{RADIUS}" '
        f'fill="{SNAKE_COLOR}" filter="url(#glow)" '
        f'transform="translate(-{CELL//2},-{CELL//2})">'
        f'{head_anim}</rect>'
    )

    # Snake eyes (two tiny white dots, follow head)
    eye_anim = segment_animation(0, path_len, FRAME_MS, pts)
    lines.append(
        f'<g transform="translate(-{CELL//2},-{CELL//2})">'
        f'<circle cx="3" cy="3" r="1.5" fill="white" opacity="0.9"/>'
        f'<circle cx="8" cy="3" r="1.5" fill="white" opacity="0.9"/>'
        f'<animateMotion dur="{total_ms}ms" begin="0ms" '
        f'repeatCount="indefinite" rotate="auto" calcMode="linear">'
        f'<mpath href="#snake-path"/>'
        f'</animateMotion>'
        f'</g>'
    )

    lines.append('</svg>')
    return "\n".join(lines)

# ── Main ──────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Fetching contributions for @{USERNAME}...")
    try:
        weeks = fetch_weeks(USERNAME)
        print(f"  → Got {len(weeks)} weeks of data")
    except Exception as e:
        print(f"  ⚠ API fetch failed ({e}), using empty 52-week grid as fallback")
        # Fallback: empty 52-week grid so the snake still renders
        weeks = [
            {"contributionDays": [
                {"contributionCount": 0, "color": "#ebedf0", "date": ""}
                for _ in range(7)
            ]}
            for _ in range(52)
        ]

    print("Generating dark SVG...")
    dark_svg = make_svg(weeks, dark=True)
    with open(DARK_FILE, "w") as f:
        f.write(dark_svg)
    print(f"  → {DARK_FILE}")

    print("Generating light SVG...")
    light_svg = make_svg(weeks, dark=False)
    with open(LIGHT_FILE, "w") as f:
        f.write(light_svg)
    print(f"  → {LIGHT_FILE}")

    print("✅ Done! Both snake SVGs generated.")
