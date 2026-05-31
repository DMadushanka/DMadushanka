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
  <!-- Clipping circular window for avatar -->
  <clipPath id="avatar-clip">
    <circle cx="90" cy="90" r="64"/>
  </clipPath>

  <!-- High-fidelity cyberpunk linear and radial gradients -->
  <linearGradient id="ring-grad-1" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#00f2fe"/>
    <stop offset="100%" stop-color="#4facfe"/>
  </linearGradient>
  
  <linearGradient id="ring-grad-2" x1="100%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#ff00de"/>
    <stop offset="50%" stop-color="#7f00ff"/>
    <stop offset="100%" stop-color="#00f2fe"/>
  </linearGradient>

  <linearGradient id="laser-grad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#00f2fe" stop-opacity="0"/>
    <stop offset="15%" stop-color="#00f2fe" stop-opacity="0.25"/>
    <stop offset="50%" stop-color="#00f2fe" stop-opacity="1"/>
    <stop offset="85%" stop-color="#00f2fe" stop-opacity="0.25"/>
    <stop offset="100%" stop-color="#00f2fe" stop-opacity="0"/>
  </linearGradient>

  <!-- Ambient volumetric power-source background glow -->
  <radialGradient id="holo-glow" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#00f2fe" stop-opacity="0.32"/>
    <stop offset="65%" stop-color="#7f00ff" stop-opacity="0.08"/>
    <stop offset="100%" stop-color="#0d1117" stop-opacity="0"/>
  </radialGradient>

  <!-- SVG Gaussian blur filter for neon volumetric light emission -->
  <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="3.2" result="blur"/>
    <feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>

  <!-- Cybernetic CSS Keyframes & Animations -->
  <style>
    @keyframes spin-cw {{
      to {{ transform: rotate(360deg); }}
    }}
    @keyframes spin-ccw {{
      to {{ transform: rotate(-360deg); }}
    }}
    @keyframes breath {{
      0%, 100% {{ opacity: 0.28; transform: scale(0.97); }}
      50% {{ opacity: 0.65; transform: scale(1.02); }}
    }}
    @keyframes scan {{
      0%, 100% {{ transform: translateY(-64px); }}
      50% {{ transform: translateY(64px); }}
    }}
    @keyframes pulse-target {{
      0%, 100% {{ opacity: 0.75; transform: scale(1.0); }}
      50% {{ opacity: 1; transform: scale(1.03); }}
    }}
    @keyframes heartbeat {{
      0%, 100% {{ opacity: 0.35; transform: scale(0.8); }}
      50% {{ opacity: 1; transform: scale(1.2); }}
    }}
    .spin-cw {{ animation: spin-cw 18s linear infinite; transform-origin: 90px 90px; }}
    .spin-ccw {{ animation: spin-ccw 9s linear infinite; transform-origin: 90px 90px; }}
    .breath {{ animation: breath 4.5s ease-in-out infinite; transform-origin: 90px 90px; }}
    .scan-beam {{ animation: scan 3.2s ease-in-out infinite; transform-origin: 90px 90px; }}
    .target-pulse {{ animation: pulse-target 2.5s ease-in-out infinite; transform-origin: 90px 90px; }}
  </style>
</defs>

<!-- Deep cybernetic space background grid (ambient tech decor) -->
<rect width="180" height="180" fill="#0d1117"/>
<g stroke="#1a2333" stroke-width="0.5" opacity="0.4">
  <line x1="20" y1="0" x2="20" y2="180"/>
  <line x1="55" y1="0" x2="55" y2="180"/>
  <line x1="90" y1="0" x2="90" y2="180"/>
  <line x1="125" y1="0" x2="125" y2="180"/>
  <line x1="160" y1="0" x2="160" y2="180"/>
  <line x1="0" y1="20" x2="180" y2="20"/>
  <line x1="0" y1="55" x2="180" y2="55"/>
  <line x1="0" y1="90" x2="180" y2="90"/>
  <line x1="0" y1="125" x2="180" y2="125"/>
  <line x1="0" y1="160" x2="180" y2="160"/>
</g>

<!-- Pulsing ambient glow backplane -->
<circle cx="90" cy="90" r="64" fill="url(#holo-glow)" class="breath"/>

<!-- Segment 1: Outer tech ticking bezel (Spinning Clockwise) -->
<circle cx="90" cy="90" r="83" fill="none" stroke="url(#ring-grad-1)" stroke-width="0.8"
  stroke-dasharray="2 6" class="spin-cw"/>

<!-- Segment 2: Heavy energy sweep brackets (Spinning Counter-Clockwise) -->
<circle cx="90" cy="90" r="79" fill="none" stroke="url(#ring-grad-2)" stroke-width="1.8"
  stroke-dasharray="120 40 40 40" class="spin-ccw" filter="url(#neon-glow)"/>

<!-- Segment 3: Telemetry HUD (Spinning Clockwise) -->
<circle cx="90" cy="90" r="74" fill="none" stroke="url(#ring-grad-1)" stroke-width="0.6"
  stroke-dasharray="10 50 30 15 8 12" class="spin-cw"/>

<!-- Segment 4: Interior aperture divider ring -->
<circle cx="90" cy="90" r="67.5" fill="none" stroke="#ffffff" stroke-width="0.5" stroke-dasharray="1 3" opacity="0.35"/>

<!-- Profile Photo clipped inside cyber-seal -->
<g class="breath">
  <image href="{avatar_data_uri}" x="26" y="26" width="128" height="128"
    clip-path="url(#avatar-clip)" preserveAspectRatio="xMidYMid slice"/>
</g>

<!-- Double-beam holographic trailing scanline laser -->
<!-- Soft trailing backbeam -->
<rect x="25" y="86" width="130" height="8" fill="url(#laser-grad)" opacity="0.32" class="scan-beam"/>
<!-- High-intensity laser scanning wire -->
<rect x="25" y="89" width="130" height="2" fill="url(#laser-grad)" class="scan-beam" filter="url(#neon-glow)"/>

<!-- Inner active neon core framing ring -->
<circle cx="90" cy="90" r="64.5" fill="none" stroke="#00f2fe" stroke-width="1.5" stroke-dasharray="402"
  style="stroke-dashoffset: 0; animation: spin-cw 4s linear infinite; transform-origin: 90px 90px;"/>

<!-- Telemetry Viewfinder Corner Brackets (Target Locking UI) -->
<g stroke="#00f2fe" stroke-width="1.8" fill="none" class="target-pulse">
  <!-- Top-Left Viewfinder -->
  <path d="M 14,26 L 14,14 L 26,14" stroke-linecap="round"/>
  <circle cx="20" cy="20" r="1.5" fill="#ff00de" stroke="none"/>
  
  <!-- Top-Right Viewfinder -->
  <path d="M 166,26 L 166,14 L 154,14" stroke-linecap="round"/>
  <circle cx="160" cy="20" r="1.5" fill="#ff00de" stroke="none"/>
  
  <!-- Bottom-Left Viewfinder -->
  <path d="M 14,154 L 14,166 L 26,166" stroke-linecap="round"/>
  <circle cx="20" cy="160" r="1.5" fill="#ff00de" stroke="none"/>
  
  <!-- Bottom-Right Viewfinder -->
  <path d="M 166,154 L 166,166 L 154,166" stroke-linecap="round"/>
  <circle cx="160" cy="160" r="1.5" fill="#ff00de" stroke="none"/>
</g>

<!-- Online Status Pill / Heartbeat Dashboard Capsule -->
<g>
  <!-- Background Pill Shape -->
  <rect x="58" y="162" width="64" height="12" rx="6" fill="#0d1117" stroke="url(#ring-grad-1)" stroke-width="1.0" opacity="0.9"/>
  <!-- Glowing Heartbeat Status Light -->
  <circle cx="68" cy="168" r="2.0" fill="#00ffcc" style="animation: heartbeat 1.5s ease-in-out infinite; transform-origin: 68px 168px;"/>
  <!-- Online Tech Readout Status -->
  <text x="94" y="171" text-anchor="middle" font-family="Courier New, monospace, sans-serif" font-weight="bold" font-size="7" fill="#00ffcc" letter-spacing="0.5">[ ONLINE ]</text>
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
