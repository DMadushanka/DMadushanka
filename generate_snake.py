import os
import requests

USERNAME   = "DMadushanka"
OUTPUT_DIR = "dist"
DARK_FILE  = f"{OUTPUT_DIR}/github-contribution-grid-snake-dark.svg"
LIGHT_FILE = f"{OUTPUT_DIR}/github-contribution-grid-snake.svg"

CELL  = 11
GAP   = 3
STEP  = CELL + GAP   # 14
RADIUS = 2
PAD_X = 16
PAD_Y = 20

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Fetch contributions ───────────────────────────────────
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
        raise RuntimeError(f"GraphQL {r.status_code}: {r.text}")
    data = r.json()
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]

# ── Grid helpers ──────────────────────────────────────────
def build_grid(weeks):
    cells = []
    for col, week in enumerate(weeks):
        for row, day in enumerate(week["contributionDays"]):
            cells.append((col, row, day["contributionCount"], day["color"]))
    return cells

def build_snake_path(num_cols, num_rows=7):
    path = []
    for col in range(num_cols):
        rows = range(num_rows) if col % 2 == 0 else range(num_rows - 1, -1, -1)
        for row in rows:
            path.append((col, row))
    return path

def cx(col): return PAD_X + col * STEP + CELL // 2
def cy(row): return PAD_Y + row * STEP + CELL // 2

# ── Build animateMotion path (must be <path>, NOT <polyline>) ──
def build_path_d(snake_path):
    pts = [(cx(c), cy(r)) for c, r in snake_path]
    d = f"M {pts[0][0]},{pts[0][1]}"
    for x, y in pts[1:]:
        d += f" L {x},{y}"
    return d

# ── SVG generator ─────────────────────────────────────────
def make_svg(weeks, dark=True):
    cells     = build_grid(weeks)
    num_cols  = max(c for c, *_ in cells) + 1
    num_rows  = 7
    path      = build_snake_path(num_cols, num_rows)
    path_len  = len(path)

    svg_w = PAD_X * 2 + num_cols * STEP
    svg_h = PAD_Y * 2 + num_rows * STEP

    if dark:
        bg_col    = "#0d1117"
        empty_col = "#161b22"
    else:
        bg_col    = "#ffffff"
        empty_col = "#ebedf0"

    path_d   = build_path_d(path)

    # Animation timing: 80ms per cell → full loop in path_len * 80 ms
    FRAME_MS = 80
    total_ms = path_len * FRAME_MS

    # Body segments: 14 total, fading/shrinking toward tail
    BODY_LEN = 14
    HEAD_COLOR      = "#3fb950"
    HEAD_TOP_COLOR  = "#2ea043"
    BODY_COLORS_ALT = ["#2ea043", "#238636"]  # alternating skin

    # ── Helper: animateMotion that lags N steps behind head ──
    def anim_motion(lag_steps):
        delay = -lag_steps * FRAME_MS
        return (
            f'<animateMotion dur="{total_ms}ms" begin="{delay}ms" '
            f'repeatCount="indefinite" rotate="auto" calcMode="linear">'
            f'<mpath href="#sp"/>'
            f'</animateMotion>'
        )

    lines = []
    lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{svg_w}" height="{svg_h}" '
        f'viewBox="0 0 {svg_w} {svg_h}">'
    )

    # ── Defs ──────────────────────────────────────────────
    lines.append('<defs>')
    lines.append(f'  <path id="sp" d="{path_d}" fill="none"/>')

    # Tongue animation
    lines.append('''  <style>
    @keyframes tongue-flick {
      0%,55%,100% { transform: scaleX(0); opacity: 0; }
      65%,90%     { transform: scaleX(1); opacity: 1; }
    }
    .tongue { animation: tongue-flick 2.4s ease-in-out infinite;
               transform-origin: 0 0; }
  </style>''')
    lines.append('</defs>')

    # ── Background ────────────────────────────────────────
    lines.append(f'<rect width="{svg_w}" height="{svg_h}" fill="{bg_col}"/>')

    # ── Contribution grid ─────────────────────────────────
    cell_map = {(c, r): (cnt, col) for c, r, cnt, col in cells}
    for (col, row), (cnt, color) in cell_map.items():
        x = PAD_X + col * STEP
        y = PAD_Y + row * STEP
        fill = color if cnt > 0 else empty_col
        lines.append(
            f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
            f'rx="{RADIUS}" fill="{fill}"/>'
        )

    # ── Snake body segments (tail → neck, drawn first so head is on top) ──
    for seg in range(BODY_LEN - 1, 0, -1):
        scale  = 1.0 - (seg / BODY_LEN) * 0.38
        rx     = round((CELL / 2 + 0.5) * scale, 2)
        ry     = round((CELL / 2 - 0.5) * scale, 2)
        color  = BODY_COLORS_ALT[seg % 2]
        opacity = round(1.0 - (seg / BODY_LEN) * 0.30, 2)
        off_x  = round(rx, 2)
        off_y  = round(ry, 2)

        lines.append(
            f'<g opacity="{opacity}">'
            # Outer body ellipse
            f'  <ellipse rx="{rx}" ry="{ry}" fill="{color}" '
            f'  transform="translate(-{CELL//2},{-CELL//2})">'
            f'  {anim_motion(seg)}</ellipse>'
        )
        # Scale marking every 3rd segment
        if seg % 3 == 0:
            sc_rx = round(rx * 0.55, 2)
            sc_ry = round(ry * 0.38, 2)
            alt   = BODY_COLORS_ALT[(seg + 1) % 2]
            lines.append(
                f'  <ellipse rx="{sc_rx}" ry="{sc_ry}" fill="{alt}" opacity="0.55" '
                f'  transform="translate(-{CELL//2},{-CELL//2})">'
                f'  {anim_motion(seg)}</ellipse>'
            )
        lines.append('</g>')

    # ── Snake head ────────────────────────────────────────
    half = CELL // 2
    hd   = CELL / 2

    # Base head shape (slightly larger than body)
    lines.append(
        f'<ellipse rx="{hd+1.5}" ry="{hd+0.5}" fill="{HEAD_COLOR}" '
        f'transform="translate(-{half},-{half})">'
        f'{anim_motion(0)}</ellipse>'
    )
    # Darker top of head
    lines.append(
        f'<ellipse rx="{hd+0.8}" ry="{hd-0.5}" fill="{HEAD_TOP_COLOR}" '
        f'transform="translate(-{half},-{half})">'
        f'{anim_motion(0)}</ellipse>'
    )

    # Eyes (white + dark pupil), offset from center
    for (ey_sign, eid) in [(−1, "L"), (1, "R")]:
        ex_local = 3.2
        ey_local = ey_sign * 2.8
        # White
        lines.append(
            f'<circle r="2.2" fill="white" '
            f'transform="translate(-{half},-{half})">'
            f'<animateMotion dur="{total_ms}ms" begin="0ms" '
            f'repeatCount="indefinite" rotate="auto" calcMode="linear">'
            f'<mpath href="#sp"/></animateMotion>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'additive="sum" from="{ex_local} {ey_local}" to="{ex_local} {ey_local}" dur="1s"/>'
            f'</circle>'
        )
        # Pupil
        lines.append(
            f'<circle r="1.1" fill="#0d1117" '
            f'transform="translate(-{half},-{half})">'
            f'<animateMotion dur="{total_ms}ms" begin="0ms" '
            f'repeatCount="indefinite" rotate="auto" calcMode="linear">'
            f'<mpath href="#sp"/></animateMotion>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'additive="sum" from="{ex_local+0.5} {ey_local}" to="{ex_local+0.5} {ey_local}" dur="1s"/>'
            f'</circle>'
        )

    # Tongue (two-fork, animated)
    # Base of tongue at front of head, forks split up/down
    tx0 = half + 1  # start x in head-local coords (forward direction = +x after rotate)
    lines.append(
        f'<g class="tongue" transform="translate(-{half},-{half})">'
        # Stem
        f'  <line x1="{tx0}" y1="0" x2="{tx0+5}" y2="0" '
        f'        stroke="#f85149" stroke-width="1.3" stroke-linecap="round"/>'
        # Fork up
        f'  <line x1="{tx0+5}" y1="0" x2="{tx0+8}" y2="-2" '
        f'        stroke="#f85149" stroke-width="1.3" stroke-linecap="round"/>'
        # Fork down
        f'  <line x1="{tx0+5}" y1="0" x2="{tx0+8}" y2="2" '
        f'        stroke="#f85149" stroke-width="1.3" stroke-linecap="round"/>'
        f'  <animateMotion dur="{total_ms}ms" begin="0ms" '
        f'  repeatCount="indefinite" rotate="auto" calcMode="linear">'
        f'  <mpath href="#sp"/>'
        f'  </animateMotion>'
        f'</g>'
    )

    lines.append('</svg>')
    return "\n".join(lines)

# ── Main ──────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Fetching contributions for @{USERNAME}...")
    try:
        weeks = fetch_weeks(USERNAME)
        print(f"  → {len(weeks)} weeks")
    except Exception as e:
        print(f"  ⚠ Fallback ({e})")
        weeks = [
            {"contributionDays": [
                {"contributionCount": 0, "color": "#ebedf0", "date": ""}
                for _ in range(7)
            ]}
            for _ in range(52)
        ]

    for dark, fpath in [(True, DARK_FILE), (False, LIGHT_FILE)]:
        label = "dark" if dark else "light"
        print(f"Generating {label} SVG...")
        svg = make_svg(weeks, dark=dark)
        with open(fpath, "w") as f:
            f.write(svg)
        print(f"  → {fpath}")

    print("✅ Done!")
