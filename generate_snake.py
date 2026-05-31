import os
import requests

USERNAME   = "DMadushanka"
OUTPUT_DIR = "dist"
DARK_FILE  = f"{OUTPUT_DIR}/github-contribution-grid-snake-dark.svg"
LIGHT_FILE = f"{OUTPUT_DIR}/github-contribution-grid-snake.svg"

CELL   = 11
GAP    = 3
STEP   = CELL + GAP
RADIUS = 2
PAD_X  = 16
PAD_Y  = 20

os.makedirs(OUTPUT_DIR, exist_ok=True)


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
        raise RuntimeError(str(data["errors"]))
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]


def build_grid(weeks):
    cells = []
    for col, week in enumerate(weeks):
        for row, day in enumerate(week["contributionDays"]):
            cells.append((col, row, day["contributionCount"], day["color"]))
    return cells


def cx(col):
    return PAD_X + col * STEP + CELL // 2


def cy(row):
    return PAD_Y + row * STEP + CELL // 2


def build_snake_path(num_cols, num_rows=7):
    """
    Boustrophedon path: col 0 top→bottom, col 1 bottom→top, etc.
    This is the ORDER the head visits cells.
    """
    path = []
    for col in range(num_cols):
        rows = range(num_rows) if col % 2 == 0 else range(num_rows - 1, -1, -1)
        for row in rows:
            path.append((col, row))
    return path


def build_path_d(snake_path):
    """
    SVG path for animateMotion.
    Straight lines within a column; smooth cubic-bezier U-turns between columns.
    The U-turn control points pull the curve outward so the snake visibly rounds the corner.
    """
    pts = [(cx(c), cy(r)) for c, r in snake_path]
    d = [f"M {pts[0][0]},{pts[0][1]}"]

    for i in range(1, len(pts)):
        pc, pr = snake_path[i - 1]
        cc, cr = snake_path[i]
        px, py = pts[i - 1]
        nx, ny = pts[i]

        if pc == cc:
            # Same column — straight vertical line
            d.append(f"L {nx},{ny}")
        else:
            # Column change — smooth horizontal S-curve
            # Pull control points horizontally toward the midpoint x
            mid_x = (px + nx) / 2
            d.append(f"C {mid_x},{py} {mid_x},{ny} {nx},{ny}")

    return " ".join(d)


def anim_motion_segment(lag_cells, total_cells, total_ms):
    """
    Correct body-segment animation using keyPoints/keyTimes.

    The head travels 0→1 along the path over total_ms.
    A segment that is `lag_cells` behind the head must trail by lag_cells/total_cells
    fraction of the path.

    At t=0:  head is at path position 0.
             this segment is at position  (1 - lag/N)  ... i.e. wrapping from end.
    At t=lag/N * total_ms:  this segment reaches position 1 (end of path),
                             then jumps to 0 and continues to (1 - lag/N).

    keyPoints: (1-frac) → 1  then  0 → (1-frac)
    keyTimes:       0   → frac then frac → 1
    """
    N    = total_cells
    frac = lag_cells / N
    sf   = round(1.0 - frac, 6)
    ft   = round(frac, 6)

    if lag_cells == 0:
        # Head: simple 0→1
        return (
            f'<animateMotion dur="{total_ms}ms" repeatCount="indefinite" '
            f'rotate="auto" calcMode="linear" '
            f'keyPoints="0;1" keyTimes="0;1">'
            f'<mpath href="#sp"/>'
            f'</animateMotion>'
        )

    return (
        f'<animateMotion dur="{total_ms}ms" repeatCount="indefinite" '
        f'rotate="auto" calcMode="linear" '
        f'keyPoints="{sf};1;0;{sf}" keyTimes="0;{ft};{ft};1">'
        f'<mpath href="#sp"/>'
        f'</animateMotion>'
    )


def make_svg(weeks, dark=True):
    cells    = build_grid(weeks)
    num_cols = max(c for c, *_ in cells) + 1
    num_rows = 7
    snake_path  = build_snake_path(num_cols, num_rows)
    total_cells = len(snake_path)

    svg_w = PAD_X * 2 + num_cols * STEP
    svg_h = PAD_Y * 2 + num_rows * STEP

    bg_col    = "#0d1117" if dark else "#ffffff"
    empty_col = "#161b22" if dark else "#ebedf0"

    # ── Timing & Slithering ─────────────────────────────────
    MS_PER_CELL = 100          # ms to traverse one cell
    BODY_LENGTH = 12           # number of body segments (excluding head)
    total_ms    = total_cells * MS_PER_CELL
    WAVELENGTH  = 10           # slither wavelength in grid cells
    SLITHER_DUR = WAVELENGTH * MS_PER_CELL  # 1000 ms wave period

    path_d = build_path_d(snake_path)

    # position index of each cell on the path
    path_index = {pos: i for i, pos in enumerate(snake_path)}
    cell_map   = {(c, r): (cnt, col) for c, r, cnt, col in cells}

    # ── Colors & Theme Definitions ──────────────────────────
    if dark:
        HEAD_GRAD_START = "#57e265"
        HEAD_GRAD_END   = "#2ea043"
        BODY_GRAD_A_START = "#39d353"
        BODY_GRAD_A_END   = "#26a641"
        BODY_GRAD_B_START = "#26a641"
        BODY_GRAD_B_END   = "#0e4429"
        DORSAL_SCALE    = "#a2e155"  # Neon lime-yellow
        EYE_PUPIL       = "#0d1117"
    else:
        HEAD_GRAD_START = "#40c463"
        HEAD_GRAD_END   = "#216e39"
        BODY_GRAD_A_START = "#40c463"
        BODY_GRAD_A_END   = "#30a14e"
        BODY_GRAD_B_START = "#30a14e"
        BODY_GRAD_B_END   = "#216e39"
        DORSAL_SCALE    = "#9be9a8"  # Soft mint green
        EYE_PUPIL       = "#24292f"

    TONGUE_COL = "#f85149"
    EYE_WHITE  = "#ffffff"

    lines = []
    L = lines.append   # shorthand

    L(f'<svg xmlns="http://www.w3.org/2000/svg" '
      f'width="{svg_w}" height="{svg_h}" '
      f'viewBox="0 0 {svg_w} {svg_h}">')

    # ── Defs ────────────────────────────────────────────────
    L("<defs>")
    L(f'  <path id="sp" d="{path_d}" fill="none"/>')
    L(f'  <linearGradient id="head-grad" x1="100%" y1="50%" x2="0%" y2="50%">')
    L(f'    <stop offset="0%" stop-color="{HEAD_GRAD_START}"/>')
    L(f'    <stop offset="100%" stop-color="{HEAD_GRAD_END}"/>')
    L(f'  </linearGradient>')
    L(f'  <linearGradient id="body-grad-a" x1="80%" y1="20%" x2="20%" y2="80%">')
    L(f'    <stop offset="0%" stop-color="{BODY_GRAD_A_START}"/>')
    L(f'    <stop offset="40%" stop-color="{BODY_GRAD_A_START}"/>')
    L(f'    <stop offset="100%" stop-color="{BODY_GRAD_A_END}"/>')
    L(f'  </linearGradient>')
    L(f'  <linearGradient id="body-grad-b" x1="80%" y1="20%" x2="20%" y2="80%">')
    L(f'    <stop offset="0%" stop-color="{BODY_GRAD_B_START}"/>')
    L(f'    <stop offset="40%" stop-color="{BODY_GRAD_B_START}"/>')
    L(f'    <stop offset="100%" stop-color="{BODY_GRAD_B_END}"/>')
    L(f'  </linearGradient>')
    L( '  <radialGradient id="gloss-grad" cx="35%" cy="35%" r="40%">')
    L( '    <stop offset="0%" stop-color="#ffffff" stop-opacity="0.5"/>')
    L( '    <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>')
    L( '  </radialGradient>')
    L(f"""  <style>
    @keyframes slither {{
      0% {{ transform: translateY(calc(-1 * var(--amp, 1.8px))) rotate(0deg); }}
      25% {{ transform: translateY(0px) rotate(var(--rot, 6deg)); }}
      50% {{ transform: translateY(var(--amp, 1.8px)) rotate(0deg); }}
      75% {{ transform: translateY(0px) rotate(calc(-1 * var(--rot, 6deg))); }}
      100% {{ transform: translateY(calc(-1 * var(--amp, 1.8px))) rotate(0deg); }}
    }}
    .slither-wrap {{
      animation: slither {SLITHER_DUR}ms ease-in-out infinite;
      transform-box: fill-box;
      transform-origin: center;
    }}
    @keyframes tongue-flick {{
      0%, 40%, 80%, 100% {{ transform: scaleX(0); opacity: 0; }}
      45%, 55%, 65%, 75% {{ transform: scaleX(1); opacity: 1; }}
      50%, 70% {{ transform: scaleX(0.8) rotate(6deg); }}
      60% {{ transform: scaleX(0.8) rotate(-6deg); }}
    }}
    .tongue {{
      animation: tongue-flick 2.5s ease-in-out infinite;
      transform-box: fill-box;
      transform-origin: left center;
    }}
    @keyframes blink {{
      0%,93%,100% {{ transform: scaleY(1); }}
      96%         {{ transform: scaleY(0.08); }}
    }}
    .eye {{ animation: blink 4s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
  </style>""")
    L("</defs>")

    # ── Background ──────────────────────────────────────────
    L(f'<rect width="{svg_w}" height="{svg_h}" fill="{bg_col}"/>')

    # ── Grid cells with "eat" animation ─────────────────────
    #
    # When the snake head arrives at a cell, the cell disappears (opacity→0).
    # After the tail clears, the cell reappears (opacity→1).
    # We use calcMode="discrete" so the change is instant (snapped, not faded).
    #
    for (col, row), (cnt, color) in cell_map.items():
        x = PAD_X + col * STEP
        y = PAD_Y + row * STEP
        fill = color if cnt > 0 else empty_col

        idx = path_index.get((col, row))

        if idx is not None and cnt > 0:
            # Normalized times
            eat_t   = idx / total_cells
            clear_t = (idx + BODY_LENGTH) / total_cells

            # Clamp to [0.0001, 0.9999] so keyTimes are strictly ordered
            t0 = max(0.0001, eat_t   - 0.0001)
            t1 = min(0.9999, eat_t   + 0.0001)
            t2 = min(0.9999, clear_t - 0.0001) if clear_t < 1.0 else 0.9999
            t3 = min(1.0,    clear_t)

            # Ensure strict ordering
            if t0 < t1 <= t2 < t3:
                kt = f"0;{t0:.5f};{t1:.5f};{t2:.5f};{t3:.5f};1"
                kv = "1;1;0;0;1;1"
                L(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                  f'rx="{RADIUS}" fill="{fill}">'
                  f'<animate attributeName="opacity" calcMode="discrete" '
                  f'values="{kv}" keyTimes="{kt}" '
                  f'dur="{total_ms}ms" repeatCount="indefinite"/>'
                  f'</rect>')
            else:
                L(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                  f'rx="{RADIUS}" fill="{fill}"/>')
        else:
            L(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
              f'rx="{RADIUS}" fill="{fill}"/>')

    # ── Helper: wrap an SVG element with slither and motion ─
    def draw_segment(content, lag):
        """
        Draw a segment by wrapping it in an outer group that follows the motion path,
        and an inner group that applies the slithering animation.
        """
        import math
        # Calculate lag-specific phase shift for slither wave
        delay_ms = -lag * MS_PER_CELL
        
        # Calculate t from 0 (head) to 1.0 (tail)
        t = lag / BODY_LENGTH if BODY_LENGTH > 0 else 0
        
        # Sinuous amplitude profile: head is 0.6px, midbody is 2.0px, tail is 0.6px
        amp = round(0.6 + 1.4 * math.sin(t * math.pi), 2)
        rot = round(amp * 3.5, 2)
        
        am = anim_motion_segment(lag, total_cells, total_ms)
        
        return (
            f'<g>\n'
            f'  {am}\n'
            f'  <g class="slither-wrap" style="--amp: {amp}px; --rot: {rot}deg; animation-delay: {delay_ms}ms;">\n'
            f'    {content}\n'
            f'  </g>\n'
            f'</g>'
        )

    # ── Body segments (tail first → head on top) ─────────────
    for seg in range(BODY_LENGTH, 0, -1):
        t      = seg / BODY_LENGTH
        scale  = 1.0 - t * 0.36
        rx_    = round((CELL / 2 + 1.2) * scale, 2)
        ry_    = round((CELL / 2 + 0.3) * scale, 2)
        fill   = "url(#body-grad-a)" if seg % 2 == 0 else "url(#body-grad-b)"
        opac   = round(1.0 - t * 0.22, 2)

        if seg == BODY_LENGTH:
            # Custom tapering pointy tail tip
            tx_start = round(rx_, 2)
            ty_start = round(ry_ * 0.8, 2)
            tip_x = round(-rx_ * 1.4, 2)
            tail_path = f"M {tx_start},-{ty_start} C {tx_start*0.4},-{ty_start} -{tx_start*0.4},-{ty_start*0.4} {tip_x},0 C -{tx_start*0.4},{ty_start*0.4} {tx_start*0.4},{ty_start} {tx_start},{ty_start} Z"
            content = f'<path d="{tail_path}" fill="{fill}"/>'
        else:
            # Regular segment shape
            content = f'<ellipse rx="{rx_}" ry="{ry_}" fill="{fill}"/>'

        # Add dorsal scale diamond (on non-tip segments, or if scale > 0.4)
        if seg < BODY_LENGTH and scale > 0.4:
            ds_rx = round(rx_ * 0.45, 2)
            ds_ry = round(ry_ * 0.28, 2)
            dorsal_path = f"M -{ds_rx},0 L 0,-{ds_ry} L {ds_rx},0 L 0,{ds_ry} Z"
            content += f'\n    <path d="{dorsal_path}" fill="{DORSAL_SCALE}" opacity="0.65"/>'
            
        # Add 3D radial gloss highlight
        sheen_rx = round(rx_ * 0.6, 2)
        sheen_ry = round(ry_ * 0.45, 2)
        content += f'\n    <ellipse cx="-{rx_*0.2:.1f}" cy="-{ry_*0.2:.1f}" rx="{sheen_rx}" ry="{sheen_ry}" fill="url(#gloss-grad)"/>'

        L(f'<g opacity="{opac}">')
        L(draw_segment(content, seg))
        L('</g>')

    # ── Head (Viper head & advanced details) ────────────────
    head_content = f"""<!-- Viper head shape -->
    <path d="M -6.5,-2.5 C -6.0,-4.8 -4.5,-6.0 -1.0,-6.2 C 3.2,-6.5 5.8,-3.5 7.8,-1.0 C 8.3,-0.5 8.3,0.5 7.8,1.0 C 5.8,3.5 3.2,6.5 -1.0,6.2 C -4.5,6.0 -6.0,4.8 -6.5,2.5 Z" fill="url(#head-grad)"/>
    <!-- Glossy dome highlight -->
    <ellipse cx="-2.0" cy="-2.0" rx="6.5" ry="4.5" fill="url(#gloss-grad)"/>
    <!-- Brow ridges -->
    <path d="M 1.0,4.2 C 2.2,4.6 3.8,4.2 4.4,3.2" stroke="{DORSAL_SCALE}" stroke-width="0.8" fill="none" opacity="0.8"/>
    <path d="M 1.0,-4.2 C 2.2,-4.6 3.8,-4.2 4.4,-3.2" stroke="{DORSAL_SCALE}" stroke-width="0.8" fill="none" opacity="0.8"/>
    <!-- Eyes with blink animation -->
    <g class="eye">
      <ellipse cx="2.5" cy="3.2" rx="2.0" ry="2.0" fill="{EYE_WHITE}"/>
      <ellipse cx="2.5" cy="-3.2" rx="2.0" ry="2.0" fill="{EYE_WHITE}"/>
    </g>
    <!-- Reptilian slit pupils -->
    <ellipse cx="2.8" cy="3.2" rx="0.5" ry="1.4" fill="{EYE_PUPIL}"/>
    <ellipse cx="2.8" cy="-3.2" rx="0.5" ry="1.4" fill="{EYE_PUPIL}"/>
    <!-- Nostrils -->
    <circle cx="6.5" cy="0.9" r="0.4" fill="{EYE_PUPIL}" opacity="0.6"/>
    <circle cx="6.5" cy="-0.9" r="0.4" fill="{EYE_PUPIL}" opacity="0.6"/>
    <!-- Tongue flick -->
    <g class="tongue">
      <line x1="7.8" y1="0" x2="12.3" y2="0" stroke="{TONGUE_COL}" stroke-width="1.3" stroke-linecap="round"/>
      <line x1="12.3" y1="0" x2="15.8" y2="-2.0" stroke="{TONGUE_COL}" stroke-width="1.2" stroke-linecap="round"/>
      <line x1="12.3" y1="0" x2="15.8" y2="2.0" stroke="{TONGUE_COL}" stroke-width="1.2" stroke-linecap="round"/>
    </g>"""

    L(draw_segment(head_content, 0))

    L('</svg>')
    return "\n".join(lines)


if __name__ == "__main__":
    print(f"Fetching contributions for @{USERNAME}...")
    try:
        weeks = fetch_weeks(USERNAME)
        print(f"  -> Got {len(weeks)} weeks of data")
    except Exception as e:
        print(f"  Warning: API fetch failed ({e}), using fallback demo grid")
        import random
        random.seed(42)
        dark_pal = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
        def make_day(n):
            idx = 0 if n == 0 else min(1 + n // 3, 4)
            return {"contributionCount": n, "color": dark_pal[idx], "date": ""}
        weeks = []
        for _ in range(52):
            days = []
            for _ in range(7):
                n = random.choices([0,1,3,5,8], weights=[35,20,22,14,9])[0]
                days.append(make_day(n))
            weeks.append({"contributionDays": days})

    for dark, fpath in [(True, DARK_FILE), (False, LIGHT_FILE)]:
        label = "dark" if dark else "light"
        print(f"Generating {label} SVG...")
        svg = make_svg(weeks, dark=dark)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"  -> {fpath}  ({len(svg.encode())//1024} KB)")

    print("Done!")
