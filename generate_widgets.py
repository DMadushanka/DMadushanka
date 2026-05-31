import os

OUTPUT_DIR = "dist"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_divider():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="30" viewBox="0 0 800 30">
<defs>
  <!-- Sleek neon horizontal linear gradient -->
  <linearGradient id="div-grad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#0d1117" stop-opacity="0"/>
    <stop offset="25%" stop-color="#00f2fe" stop-opacity="0.3"/>
    <stop offset="50%" stop-color="#7c4dff" stop-opacity="1"/>
    <stop offset="75%" stop-color="#ff00de" stop-opacity="0.3"/>
    <stop offset="100%" stop-color="#0d1117" stop-opacity="0"/>
  </linearGradient>

  <!-- Neon glow filter -->
  <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="1.5" result="blur"/>
    <feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>

  <!-- Spark rising animations -->
  <style>
    @keyframes rise-spark {{
      0% {{ transform: translateY(18px) translateX(0); opacity: 0; }}
      15% {{ opacity: 0.8; }}
      85% {{ opacity: 0.8; }}
      100% {{ transform: translateY(-5px) translateX(var(--drift, 4px)); opacity: 0; }}
    }}
    .spark {{
      animation: rise-spark 4s ease-in-out infinite;
      fill: #00f2fe;
      filter: url(#neon-glow);
    }}
    .spark-pink {{
      animation: rise-spark 5s ease-in-out infinite;
      fill: #ff00de;
      filter: url(#neon-glow);
    }}
  </style>
</defs>

<!-- Outer track baseline (fading transparently at ends) -->
<path d="M 50,15 L 750,15" fill="none" stroke="url(#div-grad)" stroke-width="1.5"/>

<!-- High-intensity laser core wire -->
<path d="M 250,15 L 550,15" fill="none" stroke="#ffffff" stroke-width="0.5" opacity="0.6" stroke-dasharray="150 10 30 10"/>

<!-- Moving Data Packets -->
<!-- Packet 1: Cyan travelling Left to Right -->
<circle r="2.2" fill="#00ffcc" filter="url(#neon-glow)">
  <animateMotion dur="4.2s" repeatCount="indefinite" path="M 120,15 L 680,15"/>
</circle>

<!-- Packet 2: Pink travelling Right to Left -->
<circle r="1.8" fill="#ff00de" filter="url(#neon-glow)">
  <animateMotion dur="5.5s" repeatCount="indefinite" path="M 680,15 L 120,15"/>
</circle>

<!-- Central Telemetry Anchor Core -->
<g transform="translate(0,0)">
  <!-- Bezel circles -->
  <circle cx="400" cy="15" r="5" fill="#0d1117" stroke="#00f2fe" stroke-width="1" filter="url(#neon-glow)"/>
  <circle cx="400" cy="15" r="2" fill="#ff00de"/>
  
  <!-- Technical sub-lines -->
  <line x1="384" y1="15" x2="390" y2="15" stroke="#00f2fe" stroke-width="0.8" opacity="0.6"/>
  <line x1="410" y1="15" x2="416" y2="15" stroke="#00f2fe" stroke-width="0.8" opacity="0.6"/>
  
  <line x1="387" y1="12" x2="387" y2="18" stroke="#7c4dff" stroke-width="0.8" opacity="0.6"/>
  <line x1="413" y1="12" x2="413" y2="18" stroke="#7c4dff" stroke-width="0.8" opacity="0.6"/>
</g>

<!-- Antigravity Sparks rising from center (organic staggered offsets) -->
<g class="spark" style="animation-delay: 0s; --drift: 6px;">
  <circle cx="370" cy="0" r="0.8"/>
</g>
<g class="spark-pink" style="animation-delay: -1.5s; --drift: -5px;">
  <circle cx="385" cy="0" r="1.0"/>
</g>
<g class="spark" style="animation-delay: -3s; --drift: 4px;">
  <circle cx="415" cy="0" r="0.8"/>
</g>
<g class="spark-pink" style="animation-delay: -0.8s; --drift: -7px;">
  <circle cx="430" cy="0" r="1.2"/>
</g>

</svg>'''
    
    path = os.path.join(OUTPUT_DIR, "divider.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {path}")

def generate_dashboard():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="200" viewBox="0 0 800 200">
<defs>
  <!-- Cyberpunk Linear & Radial Gradients -->
  <linearGradient id="border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#00f2fe"/>
    <stop offset="50%" stop-color="#7c4dff" stop-opacity="0.2"/>
    <stop offset="100%" stop-color="#ff00de"/>
  </linearGradient>

  <linearGradient id="hud-grad-blue" x1="0%" y1="100%" x2="0%" y2="0%">
    <stop offset="0%" stop-color="#7c4dff"/>
    <stop offset="100%" stop-color="#00f2fe"/>
  </linearGradient>

  <linearGradient id="hud-grad-pink" x1="0%" y1="100%" x2="0%" y2="0%">
    <stop offset="0%" stop-color="#7c4dff"/>
    <stop offset="100%" stop-color="#ff00de"/>
  </linearGradient>

  <!-- Gaussian blur for neon glowing elements -->
  <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="2.5" result="blur"/>
    <feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>

  <!-- CSS Animation rules -->
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&amp;display=swap');
    
    @keyframes spin-cw {{
      to {{ transform: rotate(360deg); }}
    }}
    @keyframes spin-ccw {{
      to {{ transform: rotate(-360deg); }}
    }}
    @keyframes wave-pulse {{
      0%, 100% {{ transform: scaleY(0.95); opacity: 0.75; }}
      50% {{ transform: scaleY(1.05); opacity: 1; }}
    }}
    @keyframes text-blink {{
      0%, 100% {{ opacity: 0.8; }}
      50% {{ opacity: 0.4; }}
    }}
    @keyframes dashboard-drift {{
      0% {{ transform: translateY(160px); opacity: 0; }}
      15% {{ opacity: 0.8; }}
      85% {{ opacity: 0.8; }}
      100% {{ transform: translateY(10px); opacity: 0; }}
    }}
    
    .spin-cw {{ transform-origin: center; animation: spin-cw 12s linear infinite; }}
    .spin-ccw {{ transform-origin: center; animation: spin-ccw 8s linear infinite; }}
    .wave-visualizer {{ transform-origin: 135px 100px; animation: wave-pulse 2.5s ease-in-out infinite; }}
    .blink-text {{ animation: text-blink 2s infinite; }}
    
    .drift-node {{ animation: dashboard-drift 8s ease-in-out infinite; fill: #00f2fe; filter: url(#neon-glow); }}
    .drift-node-purple {{ animation: dashboard-drift 11s ease-in-out infinite; fill: #7c4dff; filter: url(#neon-glow); }}
  </style>
</defs>

<!-- Premium matte background canvas -->
<rect width="800" height="200" rx="8" fill="#0d1117"/>

<!-- Fine cybernetic background grid overlay -->
<g stroke="#1a2333" stroke-width="0.5" opacity="0.3">
  <line x1="20" y1="0" x2="20" y2="200"/>
  <line x1="60" y1="0" x2="60" y2="200"/>
  <line x1="100" y1="0" x2="100" y2="200"/>
  <line x1="140" y1="0" x2="140" y2="200"/>
  <line x1="180" y1="0" x2="180" y2="200"/>
  <line x1="220" y1="0" x2="220" y2="200"/>
  <line x1="260" y1="0" x2="260" y2="200"/>
  <line x1="300" y1="0" x2="300" y2="200"/>
  <line x1="340" y1="0" x2="340" y2="200"/>
  <line x1="380" y1="0" x2="380" y2="200"/>
  <line x1="420" y1="0" x2="420" y2="200"/>
  <line x1="460" y1="0" x2="460" y2="200"/>
  <line x1="500" y1="0" x2="500" y2="200"/>
  <line x1="540" y1="0" x2="540" y2="200"/>
  <line x1="580" y1="0" x2="580" y2="200"/>
  <line x1="620" y1="0" x2="620" y2="200"/>
  <line x1="660" y1="0" x2="660" y2="200"/>
  <line x1="700" y1="0" x2="700" y2="200"/>
  <line x1="740" y1="0" x2="740" y2="200"/>
  <line x1="780" y1="0" x2="780" y2="200"/>
  
  <line x1="0" y1="30" x2="800" y2="30"/>
  <line x1="0" y1="65" x2="800" y2="65"/>
  <line x1="0" y1="100" x2="800" y2="100"/>
  <line x1="0" y1="135" x2="800" y2="135"/>
  <line x1="0" y1="170" x2="800" y2="170"/>
</g>

<!-- Sleek glassmorphic glowing border -->
<rect x="1.5" y="1.5" width="797" height="197" rx="6.5" fill="none" stroke="url(#border-grad)" stroke-width="1.2" opacity="0.8"/>

<!-- Telemetry Viewfinder Corner Brackets -->
<g stroke="#00f2fe" stroke-width="1.5" fill="none" opacity="0.7">
  <!-- Top-Left -->
  <path d="M 10,25 L 10,10 L 25,10" stroke-linecap="round"/>
  <!-- Top-Right -->
  <path d="M 790,25 L 790,10 L 775,10" stroke-linecap="round"/>
  <!-- Bottom-Left -->
  <path d="M 10,175 L 10,190 L 25,190" stroke-linecap="round"/>
  <!-- Bottom-Right -->
  <path d="M 790,175 L 790,190 L 775,190" stroke-linecap="round"/>
</g>

<!-- SECTION 1: Active Wave Telemetry Monitor (Left: x=30 to x=240) -->
<g transform="translate(30, 0)">
  <!-- Monitor border framing -->
  <rect x="0" y="35" width="200" height="135" fill="#0d1117" stroke="#161b22" stroke-width="1.0" rx="3" opacity="0.95"/>
  <!-- Scanning grid line -->
  <line x1="0" y1="35" x2="200" y2="35" stroke="#00f2fe" stroke-width="0.8" opacity="0.15">
    <animate attributeName="y1" values="35;170;35" dur="4s" repeatCount="indefinite"/>
    <animate attributeName="y2" values="35;170;35" dur="4s" repeatCount="indefinite"/>
  </line>

  <!-- Section Title -->
  <text x="10" y="24" font-family="'Space Mono', monospace" font-weight="bold" font-size="7.5" fill="#00f2fe" opacity="0.8" letter-spacing="1">[ 01_WAVE_TELEMETRY ]</text>
  
  <!-- Waveform Visualizer (Morphing continuous splines) -->
  <path fill="none" stroke="url(#hud-grad-blue)" stroke-width="1.6" filter="url(#neon-glow)" class="wave-visualizer">
    <animate attributeName="d" 
      dur="3.5s" 
      repeatCount="indefinite" 
      values="
        M 10,102 Q 35,62 60,102 T 110,102 T 160,102 T 190,102;
        M 10,102 Q 35,132 60,102 T 110,72 T 160,122 T 190,102;
        M 10,102 Q 35,62 60,102 T 110,102 T 160,102 T 190,102
      "
      keyTimes="0; 0.5; 1"
      calcMode="spline"
      keySplines="0.45 0.05 0.55 0.95; 0.45 0.05 0.55 0.95"/>
  </path>
  <path fill="none" stroke="#ff00de" stroke-width="0.8" opacity="0.6" class="wave-visualizer" style="animation-delay: -1.2s;">
    <animate attributeName="d" 
      dur="3s" 
      repeatCount="indefinite" 
      values="
        M 10,102 Q 30,122 55,102 T 100,102 T 145,102 T 190,102;
        M 10,102 Q 30,72 55,102 T 100,122 T 145,82 T 190,102;
        M 10,102 Q 30,122 55,102 T 100,102 T 145,102 T 190,102
      "
      keyTimes="0; 0.5; 1"
      calcMode="spline"
      keySplines="0.45 0.05 0.55 0.95; 0.45 0.05 0.55 0.95"/>
  </path>
  
  <!-- Digital readouts -->
  <text x="12" y="157" font-family="'Space Mono', monospace" font-size="7" fill="#ffffff" opacity="0.8">GRAV_DRIVE: ACTIVE</text>
  <text x="120" y="157" font-family="'Space Mono', monospace" font-size="7" fill="#00ffcc" class="blink-text">[ LOCK: OK ]</text>
</g>

<!-- SECTION 2: Skill Telemetry Rings (Center: x=270 to x=530) -->
<g transform="translate(250, 0)">
  <!-- Title -->
  <text x="30" y="24" font-family="'Space Mono', monospace" font-weight="bold" font-size="7.5" fill="#7c4dff" opacity="0.8" letter-spacing="1">[ 02_SKILL_MATRICES ]</text>
  
  <!-- Skill Ring 1: Full-Stack Dev -->
  <g transform="translate(60, 100)">
    <circle r="26" fill="none" stroke="#161b22" stroke-width="3"/>
    <circle r="26" fill="none" stroke="url(#hud-grad-blue)" stroke-width="3.5"
      stroke-dasharray="163" stroke-dashoffset="8" class="spin-cw" filter="url(#neon-glow)"/>
    <text text-anchor="middle" dy="3.5" font-family="'Space Mono', monospace" font-weight="bold" font-size="8.5" fill="#ffffff">95%</text>
    <text y="42" text-anchor="middle" font-family="'Space Mono', monospace" font-size="7" fill="#00f2fe" opacity="0.8">FULL-STACK</text>
  </g>

  <!-- Skill Ring 2: UI/UX Design -->
  <g transform="translate(150, 100)">
    <circle r="26" fill="none" stroke="#161b22" stroke-width="3"/>
    <circle r="26" fill="none" stroke="url(#hud-grad-pink)" stroke-width="3.5"
      stroke-dasharray="163" stroke-dashoffset="16" class="spin-ccw" filter="url(#neon-glow)"/>
    <text text-anchor="middle" dy="3.5" font-family="'Space Mono', monospace" font-weight="bold" font-size="8.5" fill="#ffffff">90%</text>
    <text y="42" text-anchor="middle" font-family="'Space Mono', monospace" font-size="7" fill="#ff00de" opacity="0.8">UI/UX DESIGN</text>
  </g>

  <!-- Skill Ring 3: Mobile & AI -->
  <g transform="translate(240, 100)">
    <circle r="26" fill="none" stroke="#161b22" stroke-width="3"/>
    <circle r="26" fill="none" stroke="url(#hud-grad-blue)" stroke-width="3.5"
      stroke-dasharray="163" stroke-dashoffset="24" class="spin-cw" filter="url(#neon-glow)"/>
    <text text-anchor="middle" dy="3.5" font-family="'Space Mono', monospace" font-weight="bold" font-size="8.5" fill="#ffffff">85%</text>
    <text y="42" text-anchor="middle" font-family="'Space Mono', monospace" font-size="7" fill="#00ffcc" opacity="0.8">MOBILE &amp; AI</text>
  </g>
</g>

<!-- SECTION 3: Quantum Particle Drift Chamber (Right: x=560 to x=770) -->
<g transform="translate(570, 0)">
  <!-- Drift chamber framing -->
  <rect x="0" y="35" width="200" height="135" fill="#0d1117" stroke="#161b22" stroke-width="1.0" rx="3" opacity="0.95"/>

  <!-- Title -->
  <text x="10" y="24" font-family="'Space Mono', monospace" font-weight="bold" font-size="7.5" fill="#ff00de" opacity="0.8" letter-spacing="1">[ 03_GRAVITY_DRIFT ]</text>
  
  <!-- Fine tech measurements inside chamber -->
  <g stroke="#ffffff" stroke-width="0.3" opacity="0.1">
    <line x1="50" y1="35" x2="50" y2="170"/>
    <line x1="100" y1="35" x2="100" y2="170"/>
    <line x1="150" y1="35" x2="150" y2="170"/>
    <line x1="0" y1="70" x2="200" y2="70"/>
    <line x1="0" y1="105" x2="200" y2="105"/>
    <line x1="0" y1="140" x2="200" y2="140"/>
  </g>

  <!-- Floating nodes inside chamber -->
  <!-- Cyan nodes -->
  <g class="drift-node" style="animation-duration: 6s; animation-delay: 0s;">
    <circle cx="40" cy="0" r="1.5"/>
  </g>
  <g class="drift-node" style="animation-duration: 9s; animation-delay: -4s;">
    <path d="M 120,-3 L 120,3 M 117,0 L 123,0" stroke="#00f2fe" stroke-width="0.8"/>
  </g>
  <g class="drift-node" style="animation-duration: 8s; animation-delay: -2s;">
    <circle cx="160" cy="0" r="1.2"/>
  </g>
  
  <!-- Purple & Pink nodes -->
  <g class="drift-node-purple" style="animation-duration: 10s; animation-delay: -1.5s;">
    <circle cx="70" cy="0" r="2.0"/>
  </g>
  <g class="drift-node-purple" style="animation-duration: 12s; animation-delay: -5s;">
    <circle cx="140" cy="0" r="1.4"/>
  </g>
  
  <!-- Readout Watermark -->
  <text x="10" y="157" font-family="'Space Mono', monospace" font-size="7" fill="#ffffff" opacity="0.6">FIELD_POTENTIAL: 0.00G</text>
  <text x="190" y="157" text-anchor="end" font-family="'Space Mono', monospace" font-size="7" fill="#7c4dff" opacity="0.8">SYS_OK</text>
</g>

</svg>'''

    path = os.path.join(OUTPUT_DIR, "dashboard.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {path}")

if __name__ == "__main__":
    print("Generating active neon dividers...")
    generate_divider()
    print("Generating systems dashboard...")
    generate_dashboard()
    print("All widgets generated successfully!")
