import os
import base64
import requests

OUTPUT_DIR = "dist"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_avatar_base64(username):
    url = f"https://github.com/{username}.png?size=200"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    b64 = base64.b64encode(r.content).decode("utf-8")
    mime = "image/png"
    return f"data:{mime};base64,{b64}"

def make_frame_svg(avatar_data_uri):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180" viewBox="0 0 180 180">
<defs>
  <clipPath id="cc">
    <circle cx="90" cy="90" r="68"/>
  </clipPath>
  <style>
    @keyframes sr  {{ to {{ stroke-dashoffset: -440; }} }}
    @keyframes sr2 {{ to {{ stroke-dashoffset: 440; }} }}
    @keyframes pd  {{ 0%,100%{{opacity:1}} 50%{{opacity:0.2}} }}
    @keyframes sc  {{ 0%{{transform:translateY(-75px)}} 100%{{transform:translateY(75px)}} }}
    @keyframes fl  {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-5px)}} }}
    @keyframes cb  {{ 0%,49%{{opacity:1}} 50%,100%{{opacity:0.2}} }}
    @keyframes bc  {{ 0%{{stroke-dashoffset:0}} 100%{{stroke-dashoffset:-600}} }}
    .fr {{ animation: fl 4s ease-in-out infinite; transform-origin: 90px 90px; }}
  </style>
</defs>

<g class="fr">
  <circle cx="90" cy="90" r="80" fill="none" stroke="rgba(79,195,247,0.08)" stroke-width="1"/>
  <circle cx="90" cy="90" r="78" fill="none" stroke="#4fc3f7" stroke-width="1.5"
    stroke-dasharray="55 18 8 18 38 18 75 18"
    style="animation:sr 8s linear infinite"/>
  <circle cx="90" cy="90" r="74" fill="none" stroke="#7c4dff" stroke-width="1"
    stroke-dasharray="28 14 48 14 18 14"
    style="animation:sr2 12s linear infinite"/>

  <rect x="8"   y="8"   width="26" height="26" rx="4" fill="none" stroke="#4fc3f7" stroke-width="1.5" style="animation:cb 1.2s ease-in-out infinite 0s"/>
  <line x1="8"  y1="18" x2="13" y2="18" stroke="#4fc3f7" stroke-width="1"/>
  <line x1="18" y1="8"  x2="18" y2="13" stroke="#4fc3f7" stroke-width="1"/>

  <rect x="146" y="8"   width="26" height="26" rx="4" fill="none" stroke="#4fc3f7" stroke-width="1.5" style="animation:cb 1.2s ease-in-out infinite 0.3s"/>
  <line x1="159" y1="18" x2="164" y2="18" stroke="#4fc3f7" stroke-width="1"/>
  <line x1="159" y1="8"  x2="159" y2="13" stroke="#4fc3f7" stroke-width="1"/>

  <rect x="8"   y="146" width="26" height="26" rx="4" fill="none" stroke="#4fc3f7" stroke-width="1.5" style="animation:cb 1.2s ease-in-out infinite 0.6s"/>
  <line x1="8"  y1="159" x2="13"  y2="159" stroke="#4fc3f7" stroke-width="1"/>
  <line x1="18" y1="168" x2="18"  y2="163" stroke="#4fc3f7" stroke-width="1"/>

  <rect x="146" y="146" width="26" height="26" rx="4" fill="none" stroke="#4fc3f7" stroke-width="1.5" style="animation:cb 1.2s ease-in-out infinite 0.9s"/>
  <line x1="159" y1="159" x2="164" y2="159" stroke="#4fc3f7" stroke-width="1"/>
  <line x1="159" y1="168" x2="159" y2="163" stroke="#4fc3f7" stroke-width="1"/>

  <!-- Profile photo embedded as base64 — works in GitHub SVG renderer -->
  <image href="{avatar_data_uri}"
    x="22" y="22" width="136" height="136"
    clip-path="url(#cc)"
    preserveAspectRatio="xMidYMid slice"/>

  <circle cx="90" cy="90" r="68" fill="none" stroke="#4fc3f7" stroke-width="2"
    stroke-dasharray="440"
    style="animation:bc 3s linear infinite"/>

  <rect x="22" y="84" width="136" height="1.5" fill="rgba(79,195,247,0.5)"
    style="animation:sc 2.5s linear infinite;transform-origin:90px 90px"/>

  <circle cx="90" cy="90" r="68" fill="rgba(79,195,247,0.02)"/>

  <circle cx="10"  cy="90"  r="3" fill="#4fc3f7" style="animation:pd 2s ease-in-out infinite 0s"/>
  <circle cx="170" cy="90"  r="3" fill="#7c4dff" style="animation:pd 2s ease-in-out infinite 1s"/>
  <circle cx="90"  cy="10"  r="3" fill="#4fc3f7" style="animation:pd 2s ease-in-out infinite 0.5s"/>
  <circle cx="90"  cy="170" r="3" fill="#7c4dff" style="animation:pd 2s ease-in-out infinite 1.5s"/>

  <text x="90" y="178" text-anchor="middle" font-family="monospace" font-size="7" fill="#4fc3f7" opacity="0.8">[ ONLINE ]</text>
</g>
</svg>'''

if __name__ == "__main__":
    username = "DMadushanka"
    print(f"Fetching avatar for @{username}...")
    try:
        avatar = fetch_avatar_base64(username)
        print(f"  -> Avatar fetched ({len(avatar)//1024}KB base64)")
    except Exception as e:
        print(f"  Warning: Could not fetch avatar ({e}), using placeholder")
        avatar = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

    print("Generating profile-frame.svg...")
    svg = make_frame_svg(avatar)
    path = os.path.join(OUTPUT_DIR, "profile-frame.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  -> {path} ({len(svg)//1024}KB)")
    print("Done!")
