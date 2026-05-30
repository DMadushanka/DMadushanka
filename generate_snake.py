import os
import requests
import json

# Configuration
USERNAME = "DMadushanka"
OUTPUT_DIR = "dist"
OUTPUT_FILE = f"{OUTPUT_DIR}/github-snake.svg"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_contributions(username):
    # GitHub GraphQL API query to get contribution count for the last year
    headers = {"Authorization": f"bearer {os.getenv('GITHUB_TOKEN')}"}
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays {
                contributionCount
                color
              }
            }
          }
        }
      }
    }
    """
    variables = {"login": username}
    response = requests.post('https://api.github.com/graphql', 
                             json={'query': query, 'variables': variables}, 
                             headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Query failed with status code {response.status_code}")
        
    return response.json()['data']['user']['contributionsCollection']['contributionCalendar']['weeks']

def generate_svg(weeks):
    # Build a pure SVG representation of the grid with a basic css animated snake
    svg_width = 820
    svg_height = 140
    
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">
    <style>
        .meta-cell {{ fill: #ebedf0; }}
        .snake {{ fill: #38bdf8; animation: moveSnake 8s infinite linear; }}
        @keyframes moveSnake {{
            0% {{ transform: translate(0px, 0px); }}
            50% {{ transform: translate(400px, 0px); }}
            100% {{ transform: translate(0px, 0px); }}
        }}
    </style>
    <rect width="100%" height="100%" fill="#0f172a" rx="6"/>
    <g transform="translate(15, 20)">
    """
    
    # Render the contribution squares based on your actual data
    for x, week in enumerate(weeks):
        for y, day in enumerate(week['contributionDays']):
            color = day['color'] if day['contributionCount'] > 0 else "#1e293b"
            svg_content += f'<rect x="{x*14}" y="{y*14}" width="10" height="10" rx="2" fill="{color}" />\n'
            
    # Add our animated pixel snake on top of the grid
    svg_content += '<rect class="snake" x="0" y="0" width="12" height="12" rx="3" />\n'
    svg_content += "</g>\n</svg>"
    
    with open(OUTPUT_FILE, "w") as f:
        f.write(svg_content)
    print("🚀 Advanced Python Snake SVG generated successfully!")

if __name__ == "__main__":
    try:
        data = fetch_contributions(USERNAME)
        generate_svg(data)
    except Exception as e:
        print(f"Error: {e}")
