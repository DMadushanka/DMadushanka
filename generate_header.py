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

def make_header_svg(username, name, desc, avatar_data_uri):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="220" viewBox="0 0 800 220">
<defs>
  <!-- Clipping circular window for avatar -->
  <clipPath id="avatar-clip">
    <circle cx="90" cy="90" r="64"/>
  </clipPath>

  <!-- Cyberpunk background linear gradients (Left is colorful/light, Right is dark for avatar contrast) -->
  <linearGradient id="bg-grad-back" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#0d1117"/>
    <stop offset="60%" stop-color="#2c1a4d"/>
    <stop offset="100%" stop-color="#0d1117"/>
  </linearGradient>

  <linearGradient id="bg-grad-front" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#00f2fe"/>
    <stop offset="40%" stop-color="#7c4dff"/>
    <stop offset="75%" stop-color="#141c2b"/>
    <stop offset="100%" stop-color="#0d1117"/>
  </linearGradient>

  <!-- Profile frame gradients -->
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

  <!-- Volumetric glow backplane -->
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
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&amp;display=swap');
    
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
    @keyframes gl-pulse {{
      0%, 100% {{ opacity: 0.8; text-shadow: 0 0 8px #00f2fe; }}
      50% {{ opacity: 1; text-shadow: 0 0 18px #ff00de, 0 0 28px #00f2fe; }}
    }}
    @keyframes anti-gravity {{
      0% {{ transform: translateY(230px) translateX(0px); opacity: 0; }}
      15% {{ opacity: 0.8; }}
      50% {{ transform: translateY(110px) translateX(12px); }}
      85% {{ opacity: 0.8; }}
      100% {{ transform: translateY(0px) translateX(-6px); opacity: 0; }}
    }}
    @keyframes matrix-rain {{
      0% {{ transform: translateY(-160px); }}
      100% {{ transform: translateY(220px); }}
    }}
    
    .spin-cw {{ animation: spin-cw 18s linear infinite; transform-origin: 90px 90px; }}
    .spin-ccw {{ animation: spin-ccw 9s linear infinite; transform-origin: 90px 90px; }}
    .breath {{ animation: breath 4.5s ease-in-out infinite; transform-origin: 90px 90px; }}
    .scan-beam {{ animation: scan 3.2s ease-in-out infinite; transform-origin: 90px 90px; }}
    .target-pulse {{ animation: pulse-target 2.5s ease-in-out infinite; transform-origin: 90px 90px; }}
    .text-glow {{ animation: gl-pulse 4s ease-in-out infinite; }}
    
    /* Float nodes */
    .float-node {{ animation: anti-gravity 9s ease-in-out infinite; fill: #00f2fe; filter: url(#neon-glow); }}
    .float-node-purple {{ animation: anti-gravity 13s ease-in-out infinite; fill: #7c4dff; filter: url(#neon-glow); }}
    .float-node-pink {{ animation: anti-gravity 11s ease-in-out infinite; fill: #ff00de; filter: url(#neon-glow); }}
    
    /* Matrix rain columns */
    .matrix-col {{ animation: matrix-rain 10s linear infinite; font-family: 'Space Mono', Courier, monospace; font-size: 7.5px; font-weight: bold; }}
  </style>
</defs>

<!-- Parallax waving background banner with smooth morph animations -->
<!-- Back wave -->
<path fill="url(#bg-grad-back)" opacity="0.35">
  <animate attributeName="d" 
    dur="16s" 
    repeatCount="indefinite" 
    values="
      M 0,0 L 800,0 L 800,165 Q 680,205 520,175 T 200,175 T 0,165 Z;
      M 0,0 L 800,0 L 800,180 Q 680,185 520,195 T 200,160 T 0,175 Z;
      M 0,0 L 800,0 L 800,165 Q 680,205 520,175 T 200,175 T 0,165 Z
    "
    keyTimes="0; 0.5; 1"
    calcMode="spline"
    keySplines="0.45 0.05 0.55 0.95; 0.45 0.05 0.55 0.95"/>
</path>

<!-- Front wave with neon stroke border and morph animation -->
<path fill="url(#bg-grad-front)" stroke="#00f2fe" stroke-width="1.2">
  <animate attributeName="d" 
    dur="12s" 
    repeatCount="indefinite" 
    values="
      M 0,0 L 800,0 L 800,150 Q 640,210 440,160 T 120,170 T 0,155 Z;
      M 0,0 L 800,0 L 800,160 Q 640,175 440,180 T 120,150 T 0,165 Z;
      M 0,0 L 800,0 L 800,150 Q 640,210 440,160 T 120,170 T 0,155 Z
    "
    keyTimes="0; 0.5; 1"
    calcMode="spline"
    keySplines="0.45 0.05 0.55 0.95; 0.45 0.05 0.55 0.95"/>
</path>

<!-- Dynamic Scrolling Cyberpunk Matrix Rain (Drifting in background) -->
<g opacity="0.06">
  <!-- Col 1: Cyan -->
  <text x="80" y="0" fill="#00f2fe" class="matrix-col" style="animation-duration: 11s; animation-delay: 0s;">
    <tspan x="80" dy="10">1</tspan>
    <tspan x="80" dy="10">0</tspan>
    <tspan x="80" dy="10">Δ</tspan>
    <tspan x="80" dy="10">g=0</tspan>
    <tspan x="80" dy="10">1</tspan>
    <tspan x="80" dy="10">Σ</tspan>
    <tspan x="80" dy="10">x</tspan>
    <tspan x="80" dy="10">0</tspan>
  </text>
  <!-- Col 2: Purple -->
  <text x="180" y="0" fill="#7c4dff" class="matrix-col" style="animation-duration: 14s; animation-delay: -3s;">
    <tspan x="180" dy="10">0</tspan>
    <tspan x="180" dy="10">1</tspan>
    <tspan x="180" dy="10">F=0</tspan>
    <tspan x="180" dy="10">Ω</tspan>
    <tspan x="180" dy="10">1</tspan>
    <tspan x="180" dy="10">y</tspan>
    <tspan x="180" dy="10">0</tspan>
  </text>
  <!-- Col 3: Pink -->
  <text x="310" y="0" fill="#ff00de" class="matrix-col" style="animation-duration: 12s; animation-delay: -6s;">
    <tspan x="310" dy="10">λ</tspan>
    <tspan x="310" dy="10">0</tspan>
    <tspan x="310" dy="10">1</tspan>
    <tspan x="310" dy="10">anti_g</tspan>
    <tspan x="310" dy="10">Σ</tspan>
    <tspan x="310" dy="10">z</tspan>
    <tspan x="310" dy="10">1</tspan>
  </text>
  <!-- Col 4: Cyan -->
  <text x="440" y="0" fill="#00f2fe" class="matrix-col" style="animation-duration: 15s; animation-delay: -1.5s;">
    <tspan x="440" dy="10">1</tspan>
    <tspan x="440" dy="10">g=0</tspan>
    <tspan x="440" dy="10">0</tspan>
    <tspan x="440" dy="10">Δt</tspan>
    <tspan x="440" dy="10">Ω</tspan>
    <tspan x="440" dy="10">1</tspan>
  </text>
  <!-- Col 5: Purple -->
  <text x="560" y="0" fill="#7c4dff" class="matrix-col" style="animation-duration: 10s; animation-delay: -4.5s;">
    <tspan x="560" dy="10">0</tspan>
    <tspan x="560" dy="10">1</tspan>
    <tspan x="560" dy="10">F_g=0</tspan>
    <tspan x="560" dy="10">λ</tspan>
    <tspan x="560" dy="10">0</tspan>
    <tspan x="560" dy="10">1</tspan>
  </text>
  <!-- Col 6: Cyan -->
  <text x="730" y="0" fill="#00f2fe" class="matrix-col" style="animation-duration: 13s; animation-delay: -8s;">
    <tspan x="730" dy="10">1</tspan>
    <tspan x="730" dy="10">0</tspan>
    <tspan x="730" dy="10">Σ</tspan>
    <tspan x="730" dy="10">anti_g</tspan>
    <tspan x="730" dy="10">1</tspan>
  </text>
</g>

<!-- Sleek Cybernetic Gravitational-Warp Grid Overlay (Deflected around avatar frame center (695,105)) -->
<g stroke="#ffffff" stroke-width="0.35" opacity="0.08" fill="none">
  <!-- Horizontal Lines (warping around avatar center) -->
  <path>
    <animate attributeName="d" dur="8s" repeatCount="indefinite" values="
      M 0,40 L 520,40 C 580,40 620,20 695,20 C 770,20 780,40 800,40;
      M 0,40 L 520,40 C 580,40 620,10 695,10 C 770,10 780,40 800,40;
      M 0,40 L 520,40 C 580,40 620,20 695,20 C 770,20 780,40 800,40
    "/>
  </path>
  <path>
    <animate attributeName="d" dur="8s" repeatCount="indefinite" values="
      M 0,80 L 480,80 C 560,80 600,45 695,45 C 780,45 770,80 800,80;
      M 0,80 L 480,80 C 560,80 600,35 695,35 C 780,35 770,80 800,80;
      M 0,80 L 480,80 C 560,80 600,45 695,45 C 780,45 770,80 800,80
    "/>
  </path>
  <path>
    <animate attributeName="d" dur="8s" repeatCount="indefinite" values="
      M 0,120 L 480,120 C 560,120 600,165 695,165 C 780,165 770,120 800,120;
      M 0,120 L 480,120 C 560,120 600,175 695,175 C 780,175 770,120 800,120;
      M 0,120 L 480,120 C 560,120 600,165 695,165 C 780,165 770,120 800,120
    "/>
  </path>
  <path>
    <animate attributeName="d" dur="8s" repeatCount="indefinite" values="
      M 0,160 L 520,160 C 580,160 620,190 695,190 C 770,190 780,160 800,160;
      M 0,160 L 520,160 C 580,160 620,200 695,200 C 770,200 780,160 800,160;
      M 0,160 L 520,160 C 580,160 620,190 695,190 C 770,190 780,160 800,160
    "/>
  </path>

  <!-- Vertical Lines (warping outward/inward) -->
  <line x1="50" y1="0" x2="50" y2="180"/>
  <line x1="150" y1="0" x2="150" y2="180"/>
  <line x1="250" y1="0" x2="250" y2="180"/>
  <line x1="350" y1="0" x2="350" y2="180"/>
  <line x1="450" y1="0" x2="450" y2="180"/>
  
  <path>
    <animate attributeName="d" dur="8s" repeatCount="indefinite" values="
      M 550,0 C 550,50 520,105 550,220;
      M 550,0 C 550,50 500,105 550,220;
      M 550,0 C 550,50 520,105 550,220
    "/>
  </path>
  <path>
    <animate attributeName="d" dur="8s" repeatCount="indefinite" values="
      M 600,0 C 600,50 560,105 600,220;
      M 600,0 C 600,50 540,105 600,220;
      M 600,0 C 600,50 560,105 600,220
    "/>
  </path>
  <path>
    <animate attributeName="d" dur="8s" repeatCount="indefinite" values="
      M 740,0 C 740,50 780,105 740,220;
      M 740,0 C 740,50 800,105 740,220;
      M 740,0 C 740,50 780,105 740,220
    "/>
  </path>
  <path>
    <animate attributeName="d" dur="8s" repeatCount="indefinite" values="
      M 785,0 C 785,50 805,105 785,220;
      M 785,0 C 785,50 820,105 785,220;
      M 785,0 C 785,50 805,105 785,220
    "/>
  </path>
</g>

<!-- Floating Antigravity digital nodes (drifting slowly upwards in organic vectors) -->
<!-- Cyan nodes -->
<g class="float-node" style="animation-duration: 8s; animation-delay: 0s;">
  <circle cx="120" cy="0" r="1.8"/>
</g>
<g class="float-node" style="animation-duration: 10s; animation-delay: -5s;">
  <path d="M 400,-3 L 400,3 M 397,0 L 403,0" stroke="#00f2fe" stroke-width="1.0"/>
</g>
<g class="float-node" style="animation-duration: 9s; animation-delay: -7s;">
  <circle cx="510" cy="0" r="1.5"/>
</g>
<g class="float-node" style="animation-duration: 11s; animation-delay: -2s;">
  <circle cx="340" cy="0" r="2.0"/>
</g>

<!-- Purple nodes -->
<g class="float-node-purple" style="animation-duration: 12s; animation-delay: -3s;">
  <circle cx="280" cy="0" r="2.2"/>
</g>
<g class="float-node-purple" style="animation-duration: 15s; animation-delay: -1s;">
  <circle cx="210" cy="0" r="1.4"/>
</g>
<g class="float-node-purple" style="animation-duration: 13s; animation-delay: -4s;">
  <path d="M 80,-3 L 80,3 M 77,0 L 83,0" stroke="#7c4dff" stroke-width="1.0"/>
</g>
<g class="float-node-purple" style="animation-duration: 14s; animation-delay: -8s;">
  <rect x="460" y="-2" width="4" height="4" fill="none" stroke="#7c4dff" stroke-width="0.8"/>
</g>

<!-- Pink nodes -->
<g class="float-node-pink" style="animation-duration: 10.5s; animation-delay: -2.5s;">
  <polygon points="160,-3 163,2 157,2" fill="#ff00de"/>
</g>
<g class="float-node-pink" style="animation-duration: 12.5s; animation-delay: -6.5s;">
  <circle cx="370" cy="0" r="1.6"/>
</g>
<g class="float-node-pink" style="animation-duration: 14.5s; animation-delay: -4.5s;">
  <path d="M 640,-3 L 640,3 M 637,0 L 643,0" stroke="#ff00de" stroke-width="1.0"/>
</g>

<!-- Left-Aligned Header Text (Highly Structured) -->
<g transform="translate(0, 0)">
  <!-- Antigravity Systems Status Readout -->
  <text x="50" y="52" font-family="'Space Mono', monospace, sans-serif" font-weight="bold" font-size="7.5" fill="#00f2fe" opacity="0.65" letter-spacing="1.2" class="text-glow">SYS.STATUS: ANTIGRAVITY_DRIVE = ACTIVE // GRID.FIELD = WAVE_MORPH_102 // NODE: USR_MADUSHANKA</text>
  <!-- Name with glow effect -->
  <text x="50" y="95" font-family="'Space Mono', monospace, sans-serif" font-weight="bold" font-size="34" fill="#ffffff" class="text-glow" letter-spacing="1">{name}</text>
  <!-- Role / Description (Changed from cyan #00f2fe to high-contrast white #ffffff for maximum readability) -->
  <text x="50" y="132" font-family="'Space Mono', monospace, sans-serif" font-size="13" fill="#ffffff" opacity="0.9" letter-spacing="0.5">{desc}</text>
</g>

<!-- Right-Aligned Profile Frame Embedded Directly Inside the Banner (Scaled down to 0.86 and shifted for perfect centering inside boundaries) -->
<g transform="translate(605, 15) scale(0.86)">
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
    <!-- Solid dark backdrop to block out background color wash and maintain pristine image colors -->
    <circle cx="90" cy="90" r="64" fill="#0d1117" clip-path="url(#avatar-clip)"/>
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
</g>
</svg>'''

if __name__ == "__main__":
    username = "DMadushanka"
    name = "Gayan Madushanka"
    desc = "Full-Stack Developer | UI/UX Designer | ICT Undergraduate"
    print(f"Fetching avatar for @{username}...")
    try:
        avatar = fetch_avatar_base64(username)
        print(f"  -> Avatar fetched ({len(avatar)//1024}KB base64)")
    except Exception as e:
        print(f"  Warning: Could not fetch avatar ({e}), using placeholder")
        avatar = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

    print("Generating header.svg...")
    svg = make_header_svg(username, name, desc, avatar)
    path = os.path.join(OUTPUT_DIR, "header.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  -> {path} ({len(svg)//1024}KB)")
    print("Done!")
