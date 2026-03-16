"""
Sync image paths in index.html and menu.html with actual filenames in photos/.

Run from repo root or from htmlcodes/:
  python htmlcodes/sync_photo_paths.py
  # or from htmlcodes/:
  python sync_photo_paths.py

This updates img src="photos/..." so they match the exact filenames in photos/
(case-sensitive, for Vercel). Run after adding/renaming images.
"""
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTOS_DIR = os.path.join(SCRIPT_DIR, "photos")
INDEX_HTML = os.path.join(SCRIPT_DIR, "index.html")
MENU_HTML = os.path.join(SCRIPT_DIR, "online-restaurant-orderjquery", "dist", "menu.html")

# Normalized key (lowercase, spaces -> hyphens) -> actual filename in photos/
def normalize(name):
    base = os.path.splitext(name)[0].lower().replace(" ", "-")
    ext = os.path.splitext(name)[1].lower()
    return base + ext

def build_lookup():
    if not os.path.isdir(PHOTOS_DIR):
        return {}
    lookup = {}
    for f in os.listdir(PHOTOS_DIR):
        if not f.startswith("."):
            key = normalize(f)
            lookup[key] = f
    return lookup

def replace_photos_in_file(path, prefix, lookup):
    """prefix is 'photos/' for index, '../../photos/' for menu."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    original = text

    # Match src="prefixSOMETHING" or src='prefixSOMETHING'
    pattern = re.compile(
        r'(src=["\'])(' + re.escape(prefix) + r')([^"\']+)(["\'])',
        re.IGNORECASE
    )
    def repl(m):
        pre, path_pre, filename, end = m.groups()
        key = normalize(filename)
        actual = lookup.get(key, filename)
        if actual != filename:
            return f"{pre}{path_pre}{actual}{end}"
        return m.group(0)
    text = pattern.sub(repl, text)
    if text != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return True
    return False

def main():
    lookup = build_lookup()
    if not lookup:
        print("No photos folder or empty. Nothing to sync.")
        return
    updated_index = replace_photos_in_file(INDEX_HTML, "photos/", lookup)
    updated_menu = replace_photos_in_file(MENU_HTML, "../../photos/", lookup)
    if updated_index:
        print("Updated:", INDEX_HTML)
    if updated_menu:
        print("Updated:", MENU_HTML)
    if not updated_index and not updated_menu:
        print("Paths already in sync. No changes made.")

if __name__ == "__main__":
    main()
