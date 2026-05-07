import json
import os


COVERAGE_JSON_PATH = "/tmp/coverage.json"
OUTPUT_DIR = "badge_output"


def load_coverage():
    with open(COVERAGE_JSON_PATH) as f:
        data = json.load(f)
    return float(data["totals"]["percent_covered_display"])


def color_for_pct(pct):
    if pct >= 90:
        return "brightgreen", "#4c1"
    if pct >= 80:
        return "green", "#97ca00"
    if pct >= 60:
        return "yellowgreen", "#a4a61d"
    if pct >= 40:
        return "yellow", "#dfb317"
    return "red", "#e05d44"


def make_svg_badge(pct):
    _, hex_color = color_for_pct(pct)
    label = "coverage"
    message = f"{pct:.1f}%"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="120" height="20">
  <linearGradient id="a" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <rect rx="3" width="120" height="20" fill="#555"/>
  <rect rx="3" x="0" width="60" height="20" fill="#555"/>
  <rect rx="3" x="60" width="60" height="20" fill="{hex_color}"/>
  <rect fill="url(#a)" width="120" height="20"/>
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="30" y="15" fill="#010101" fill-opacity=".3">{label}</text>
    <text x="30" y="14">{label}</text>
    <text x="90" y="15" fill="#010101" fill-opacity=".3">{message}</text>
    <text x="90" y="14">{message}</text>
  </g>
</svg>'''


def make_shields_endpoint(pct):
    color_name, _ = color_for_pct(pct)
    return {
        "schemaVersion": 1,
        "label": "coverage",
        "message": f"{pct:.1f}%",
        "color": color_name,
    }


def main():
    pct = load_coverage()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    svg = make_svg_badge(pct)
    with open(f"{OUTPUT_DIR}/coverage.svg", "w") as f:
        f.write(svg)

    endpoint = make_shields_endpoint(pct)
    with open(f"{OUTPUT_DIR}/coverage.json", "w") as f:
        json.dump(endpoint, f)

    print(f"Coverage badge generated: {pct:.1f}%")


if __name__ == "__main__":
    main()
