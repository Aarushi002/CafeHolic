# -*- coding: utf-8 -*-
"""Extract recipe blocks, build name->block mapping, reorganize menu sections."""

import re

MENU_PATH = "menu.html"

with open(MENU_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Boundaries: replace content between these
START_MARKER = '<div class="recipe-menu">'
END_MARKER = '      </div>\n    </div>\n\n    <div id="finishOrderDialog" title="Confirm Order">'

# Extract the part that contains all recipe blocks (between the two markers)
start_idx = content.find(START_MARKER)
end_idx = content.find(END_MARKER)
if start_idx == -1 or end_idx == -1:
    raise SystemExit("Markers not found")
inner_start = start_idx + len(START_MARKER)
old_inner = content[inner_start:end_idx]

# Split by "        <!-- Recipe " to get chunks; first chunk is section headers/empty
chunks = re.split(r'(\s{8}<!-- Recipe \d+ -->)', old_inner)
# chunks[0] = leading content (section + heading), chunks[1],chunks[2] = comment + block, ...
# Actually split keeps the delimiter, so we get: [leading, "        <!-- Recipe 1 -->", block1, "        <!-- Recipe 2 -->", block2, ...]
# So we need to find blocks differently: use regex to find each "        <!-- Recipe N -->" and then find the matching closing "        </div>"

def extract_recipe_blocks(text):
    """Extract each recipe block: from '        <!-- Recipe N -->' to closing '        </div>' of recipe card."""
    blocks = []
    # Pattern: optional whitespace, then comment, then <div class="recipe"> ... </div> (8-space close)
    pattern = r'\s*<!-- Recipe \d+ -->\s*\n(\s*<div class="recipe">.*?) (\n        </div>)'
    # The inner div closes with 10 spaces, recipe closes with 8. So we want to match from <div class="recipe"> to the LAST occurrence of \n        </div> within that block - i.e. we need to match balanced. Simpler: find <!-- Recipe N --> then find the next <div class="recipe"> then find the closing 8-space </div> by counting: after <div class="recipe"> we have one child div (checkOrder), so we see "          </div>" then "        </div>". So we need to match from start to the second "\n        </div>" or the first one that is at depth 0. Actually the simplest is: from "        <!-- Recipe N -->" take until we have "\n        </div>\n" that is followed by either "\n        <!-- Recipe" or "\n        </section" or end. So we look for the 8-space </div> that is followed by newline and then either 8 spaces (next recipe comment) or 0 spaces (</section>). Let me try a different approach: find all positions of "        <!-- Recipe " and for each, find the next "        <!-- Recipe " or "</section" or end; then the block is from this comment to the "        </div>" that appears just before that next start. So block = from "        <!-- Recipe N -->" to the last "        </div>" before the next "        <!-- Recipe " or "</section".
    pos = 0
    while True:
        comment_match = re.search(r'\s{8}<!-- Recipe \d+ -->', text[pos:])
        if not comment_match:
            break
        block_start = pos + comment_match.start()
        block_start_abs = block_start
        # From block_start, find the next <div class="recipe"> (immediately after comment)
        recipe_div = re.search(r'\s*<div class="recipe">', text[block_start:])
        if not recipe_div:
            pos = block_start + 1
            continue
        inner_start = block_start + recipe_div.end()
        # Find the matching closing </div> for <div class="recipe"> - it's at 8 spaces indent
        # Count depth: we're inside recipe (depth 1). We see nested divs at 10 spaces. So we need to find "\n        </div>" that brings depth to 0. So scan for </div> with 8 spaces - that's our closer.
        depth = 1
        search_start = inner_start
        end_pos = None
        while True:
            # Find next </div> with exactly 8 spaces before it (newline + 8 spaces)
            match = re.search(r'\n        </div>', text[search_start:])
            if not match:
                break
            # This could be inner div (10 spaces would be different - we're looking for 8). So this is the recipe's </div>.
            end_pos = search_start + match.start() + match.end()
            break
        if end_pos is None:
            pos = block_start + 1
            continue
        block = text[block_start:end_pos]
        blocks.append(block)
        pos = end_pos
    return blocks

# Simpler: split by "        <!-- Recipe " and for each part (except first), block = "        <!-- Recipe " + part up to and including first "\n        </div>". But the first part has no recipe. So:
parts = re.split(r'(\s{8}<!-- Recipe \d+ -->)', old_inner)
recipe_blocks = []
i = 1
while i < len(parts):
    if re.match(r'\s{8}<!-- Recipe \d+ -->', parts[i]):
        # This is the comment; parts[i+1] is the content until next comment or end
        comment = parts[i]
        rest = parts[i+1] if i+1 < len(parts) else ''
        # Rest starts with newline and "        <div class="recipe">...". Find the closing "        </div>" (8 spaces).
        end_match = re.search(r'\n        </div>', rest)
        if end_match:
            block_content = rest[:end_match.end()]
            full_block = comment + block_content
            recipe_blocks.append(full_block)
        i += 2
    else:
        i += 1

def get_name(block):
    m = re.search(r'<p class="name">([^<]+)</p>', block)
    return m.group(1).strip() if m else None

# Build mapping: key = normalized name (strip), value = full block
name_to_block = {}
for b in recipe_blocks:
    name = get_name(b)
    if name:
        name_to_block[name] = b

# Aliases for "match X" in user spec: file might say "Chhole Chawal", list says "Chole Chawal"
alias_to_canonical = {
    "Chhole Chawal": "Chole Chawal",
    "Dal Makhani": "Dal Makhani",  # same in file
    "Chowmein": "Chowmein",
    "Chilli Potato": "Chilli Potato",
    "Mix Veg": "Mix Veg",
    "Jaljeera": "Jaljeera",
    "Fruity": "Frooti",
}
# Also map file names to themselves so we can look up by canonical list name
for canonical, block in list(name_to_block.items()):
    if canonical not in name_to_block:
        pass
    alias_to_canonical[canonical] = canonical
for file_name in name_to_block:
    if file_name not in alias_to_canonical:
        alias_to_canonical[file_name] = file_name

def get_block_for_dish(dish_name):
    if dish_name in name_to_block:
        return name_to_block[dish_name]
    if dish_name in alias_to_canonical:
        canon = alias_to_canonical[dish_name]
        return name_to_block.get(canon)
    # Try by exact match in file
    for file_name, block in name_to_block.items():
        if file_name.strip() == dish_name.strip():
            return block
    return None

# Section order and dish lists (user spec)
SECTIONS = [
    ("North Indian", "north-indian", [
        "Chole Bhature", "Pav Bhaji", "Chole Chawal", "Rajma Chawal", "Veg Biryani",
        "Paneer Tikka", "Aloo Paratha", "Dal Rice", "Kadhi Chawal", "Paneer Butter Masala",
        "Butter Naan", "Dal Makhani", "Veg Pulao", "Jeera Rice", "Mix Veg", "Malai Kofta"
    ]),
    ("South Indian", "south-indian", [
        "Dosa", "Idli", "Rava Dosa", "Pongal", "Sambar Rice", "Curd Rice",
        "Lemon Rice", "Tamarind Rice"
    ]),
    ("Chinese", "chinese", [
        "Chowmein", "Chilli Potato", "Spring Roll", "Manchurian", "Hakka Noodles", "Veg Fried Rice"
    ]),
    ("Snacks and Fast Food", "snacks--fast-food", [
        "French Fries", "Macaroni", "Pasta", "Samosa", "Sandwich", "Burger", "Pizza Slice", "Nachos"
    ]),
    ("Beverages", "beverages", [
        "Cold Coffee", "Chocolate Shake", "Frooti", "Tomato Soup", "Hot Coffee",
        "Masala Chai", "Lassi", "Jaljeera", "Fresh Lime"
    ]),
    ("Desserts", "desserts", [
        "Gulab Jamun", "Rasmalai", "Ice Cream", "Brownie", "Cake Slice", "Fruit Salad"
    ]),
]

# Resolve "Chole Chawal" -> file has "Chhole Chawal"
dish_to_file_name = {}
for name, block in name_to_block.items():
    dish_to_file_name[name] = name
dish_to_file_name["Chole Chawal"] = "Chhole Chawal"  # match "Chhole Chawal" in file

lines = []
for section_title, section_id, dishes in SECTIONS:
    lines.append('        <section class="menu-category" id="' + section_id + '">')
    lines.append('          <h2 class="category-heading">' + section_title + '</h2>')
    for dish in dishes:
        block = get_block_for_dish(dish)
        if block is None:
            block = name_to_block.get(dish_to_file_name.get(dish, dish))
        if block is None:
            # try by stripping
            for k, v in name_to_block.items():
                if k.replace(" ", "").lower() == dish.replace(" ", "").lower():
                    block = v
                    break
        if block:
            lines.append(block)
        else:
            raise SystemExit("Missing block for dish: " + repr(dish))
    lines.append('')
    lines.append('</section>')

new_inner = "\n".join(lines)

# Ensure exactly one newline after recipe-menu opening and before the first section (match original style)
new_content = content[:inner_start] + "\n" + new_inner + "\n      " + content[end_idx:]
# Actually the user said "replace the entire content between" - so we replace old_inner with new_inner. The closing part "</div>\n      </div>..." stays. So:
new_content = content[:inner_start] + "\n" + new_inner + "\n" + content[end_idx:]

with open(MENU_PATH, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Done. Reorganized menu into 6 sections.")
