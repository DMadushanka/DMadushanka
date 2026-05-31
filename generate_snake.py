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

    # ── Timing ──────────────────────────────────────────────
    MS_PER_CELL = 100          # ms to traverse one cell
    BODY_LENGTH = 12           # number of body segments (excluding head)
    total_ms    = total_cells * MS_PER_CELL

    path_d = build_path_d(snake_path)

    # position index of each cell on the path
    path_index = {pos: i for i, pos in enumerate(snake_path)}
    cell_map   = {(c, r): (cnt, col) for c, r, cnt, col in cells}

    # ── Colours ─────────────────────────────────────────────
    HEAD_COLOR = "#3fb950"
    HEAD_SHEEN = "#57e265"
    BODY_A     = "#2ea043"
    BODY_B     = "#238636"
    TONGUE_COL = "#f85149"
    EYE_WHITE  = "#ffffff"
    EYE_PUPIL  = "#0d1117" if dark else "#24292f"

    lines = []
    L = lines.append   # shorthand

    L(f'<svg xmlns="http://www.w3.org/2000/svg" '
      f'width="{svg_w}" height="{svg_h}" '
      f'viewBox="0 0 {svg_w} {svg_h}">')

    # ── Defs ────────────────────────────────────────────────
    L("<defs>")
    L(f'  <path id="sp" d="{path_d}" fill="none"/>')
    L("""  <style>
    @keyframes tongue-flick {
      0%,50%,100% { transform: scaleX(0); opacity: 0; }
      60%,88%     { transform: scaleX(1); opacity: 1; }
    }
    .tongue {
      animation: tongue-flick 2.5s ease-in-out infinite;
      transform-box: fill-box;
      transform-origin: left center;
    }
    @keyframes blink {
      0%,93%,100% { transform: scaleY(1); }
      96%         { transform: scaleY(0.08); }
    }
    .eye { animation: blink 4s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
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

    # ── Helper: wrap an SVG element with animateMotion ──────
    #
    # CRITICAL: We do NOT use transform="translate(-half,-half)" as a static
    # attribute because animateMotion REPLACES the element's position (it sets
    # the supplemental transformation matrix). Instead, we apply the centering
    # offset through a child animateTransform with additive="sum".
    #
    half = CELL // 2

    def motion_elem(tag_open, tag_close, lag):
        """Wrap an element so it travels along the snake path, centered on each cell."""
        am = anim_motion_segment(lag, total_cells, total_ms)
        # additive="sum" centering offset so element is centred on the path point
        at = (f'<animateTransform attributeName="transform" type="translate" '
              f'additive="sum" from="-{half} -{half}" to="-{half} -{half}" dur="1s"/>')
        return f"{tag_open}{am}{at}{tag_close}"

    def motion_elem_offset(tag_open, tag_close, lag, dx, dy):
        """Like motion_elem but with an additional local offset (for eyes, tongue)."""
        am = anim_motion_segment(lag, total_cells, total_ms)
        # Combine centering + local offset in one animateTransform
        ox, oy = -half + dx, -half + dy
        at = (f'<animateTransform attributeName="transform" type="translate" '
              f'additive="sum" from="{ox} {oy}" to="{ox} {oy}" dur="1s"/>')
        return f"{tag_open}{am}{at}{tag_close}"

    # ── Body segments (tail first → head on top) ─────────────
    for seg in range(BODY_LENGTH, 0, -1):
        t      = seg / BODY_LENGTH
        scale  = 1.0 - t * 0.36
        rx_    = round((CELL / 2 + 0.5) * scale, 2)
        ry_    = round((CELL / 2 - 0.5) * scale, 2)
        fill   = BODY_A if seg % 2 == 0 else BODY_B
        opac   = round(1.0 - t * 0.22, 2)

        L(f'<g opacity="{opac}">')
        L(motion_elem(
            f'<ellipse rx="{rx_}" ry="{ry_}" fill="{fill}">',
            '</ellipse>',
            seg
        ))

        # Scale-pattern dots every 3rd segment
        if seg % 3 == 0 and scale > 0.68:
            srx = round(rx_ * 0.50, 2)
            sry = round(ry_ * 0.34, 2)
            alt = BODY_B if seg % 2 == 0 else BODY_A
            L(motion_elem(
                f'<ellipse rx="{srx}" ry="{sry}" fill="{alt}" opacity="0.42">',
                '</ellipse>',
                seg
            ))

        L('</g>')

    # ── Head (two-layer for 3-D dome look) ───────────────────
    hd = CELL / 2
    L(motion_elem(
        f'<ellipse rx="{hd + 1.5}" ry="{hd + 0.5}" fill="{HEAD_COLOR}">',
        '</ellipse>', 0
    ))
    L(motion_elem(
        f'<ellipse rx="{hd + 0.7}" ry="{hd - 0.6}" fill="{HEAD_SHEEN}" opacity="0.5">',
        '</ellipse>', 0
    ))

    # ── Eyes ─────────────────────────────────────────────────
    # Eyes sit forward on the head (+3 px along motion direction)
    # and to each side (±2.6 px lateral)
    EFX = 3.0    # forward offset along direction of travel
    ESY = 2.6    # lateral offset

    for side in (-1, 1):
        # white sclera with blink animation
        L(f'<g class="eye">')
        L(motion_elem_offset(
            f'<circle r="2.0" fill="{EYE_WHITE}">',
            '</circle>', 0, EFX, side * ESY
        ))
        L('</g>')
        # pupil (slightly more forward so it looks like it's looking ahead)
        L(motion_elem_offset(
            f'<circle r="1.0" fill="{EYE_PUPIL}">',
            '</circle>', 0, EFX + 0.5, side * ESY
        ))

    # ── Tongue ───────────────────────────────────────────────
    # Tongue root is ahead of the head nose, forked at the tip.
    # The whole group has CSS tongue-flick animation (scaleX 0→1→0).
    # transform-origin is left center of the group so it flicks outward.
    tx0 = half + 2.0    # root x in local (head-centered) space
    L(f'<g class="tongue">')
    L(motion_elem_offset(
        f'<line x1="{tx0:.1f}" y1="0" x2="{tx0 + 4:.1f}" y2="0" '
        f'stroke="{TONGUE_COL}" stroke-width="1.3" stroke-linecap="round">',
        '</line>', 0, 0, 0
    ))
    L(motion_elem_offset(
        f'<line x1="{tx0 + 4:.1f}" y1="0" x2="{tx0 + 7:.1f}" y2="-2.2" '
        f'stroke="{TONGUE_COL}" stroke-width="1.2" stroke-linecap="round">',
        '</line>', 0, 0, 0
    ))
    L(motion_elem_offset(
        f'<line x1="{tx0 + 4:.1f}" y1="0" x2="{tx0 + 7:.1f}" y2="2.2" '
        f'stroke="{TONGUE_COL}" stroke-width="1.2" stroke-linecap="round">',
        '</line>', 0, 0, 0
    ))
    L('</g>')

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
