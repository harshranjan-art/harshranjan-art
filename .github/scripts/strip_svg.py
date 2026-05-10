"""
Remove the language pie chart and radar chart from the 3D contrib SVG.
Uses regex to find and remove <g>...</g> blocks containing target keywords.
"""
import re

SVG_FILE = "profile-3d-contrib/profile-custom.svg"

with open(SVG_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# We'll repeatedly remove top-level <g> blocks that contain these keywords
# Strategy: find all <g...>...</g> blocks and remove those containing keywords
KEYWORDS = ["TypeScript", "JavaScript", "donut", "Commit", "Repo", "Issue", "Review", "PullReq"]

def contains_keyword(s):
    return any(k in s for k in KEYWORDS)

def remove_g_blocks_with_keywords(svg):
    # Match <g...>...</g> at top level (non-greedy won't work for nested,
    # so we iterate to handle nesting)
    changed = True
    while changed:
        changed = False
        # Remove <g ...>content</g> blocks where content contains a keyword
        # This handles single-level groups
        new_svg = re.sub(
            r'<g(?:[^>]*)>(?:(?!</g>).)*?(?:TypeScript|JavaScript|donut|Commit|Repo|Issue|Review|PullReq)(?:(?!</g>).)*?</g>',
            '',
            svg,
            flags=re.DOTALL
        )
        if new_svg != svg:
            svg = new_svg
            changed = True
    return svg

content = remove_g_blocks_with_keywords(content)

with open(SVG_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print("SVG cleaned successfully")
