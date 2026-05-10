"""
Strip the language pie chart and radar chart from the 3D contrib SVG.
The SVG is structured with <g> groups. We identify them by their text content.
"""
import xml.etree.ElementTree as ET
import re

SVG_FILE = "profile-3d-contrib/profile-custom.svg"

ET.register_namespace("", "http://www.w3.org/2000/svg")
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")

# Parse with regex since SVG may have namespace issues
with open(SVG_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Keywords that identify the pie chart and radar sections
REMOVE_KEYWORDS = [
    "TypeScript", "JavaScript", "donut", "pie",
    "Commit", "Repo", "Issue", "Review", "PullReq"
]

# Split into lines, find and remove <g>...</g> blocks containing these keywords
# Strategy: track depth of <g> tags, mark blocks for removal
lines = content.split("\n")
result = []
skip_depth = 0
g_depth = 0
i = 0

while i < len(lines):
    line = lines[i]
    opens = line.count("<g") - line.count("</g") - line.count("/>")
    closes = line.count("</g>")
    
    if skip_depth > 0:
        skip_depth += opens
        skip_depth -= closes
        if skip_depth <= 0:
            skip_depth = 0
        i += 1
        continue
    
    # Check if this line or next few lines contain removal keywords
    lookahead = "\n".join(lines[i:min(i+3, len(lines))])
    should_remove = any(kw in lookahead for kw in REMOVE_KEYWORDS)
    
    if should_remove and "<g" in line and opens > 0:
        skip_depth = opens
        i += 1
        continue
    
    result.append(line)
    i += 1

with open(SVG_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(result))

print("SVG cleaned successfully")
