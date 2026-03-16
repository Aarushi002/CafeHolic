"""
Download dish-specific food images using Pexels API (free).
One API key, one command – gets PNGs for all menu items.

SETUP (one time):
  1. Go to https://www.pexels.com/api/
  2. Sign up / log in, copy your API key
  3. Paste it below replacing YOUR_PEXELS_API_KEY
  4. Run: python download_food_images_api.py
"""
import os
import time
import urllib.request
import urllib.parse
import json
import ssl

# ============ PASTE YOUR PEXELS API KEY HERE ============
PEXELS_API_KEY = "cXk203psAs7qeRCCTtsfuDnCviPXkEYUu9g50KHSGalUwRd39nMpGlty"
# =========================================================

PHOTOS_DIR = os.path.join(os.path.dirname(__file__), "photos")
os.makedirs(PHOTOS_DIR, exist_ok=True)

# Filename -> search query (what to type in Pexels)
FILENAME_TO_QUERY = {
    "ChholeBhature.png": "chole bhature",
    "PavBhaji2.png": "pav bhaji",
    "Chowmein.png": "veg chowmein",
    "Macaroni.jpg": "macaroni pasta",
    "Pasta.jpg": "pasta italian",
    "chillipotato.jpg": "chilli potato",
    "Fries.jpg": "french fries",
    "ChholeChawal.jpeg": "chole chawal",
    "Rajma_Chawal.jpg": "rajma chawal",
    "frooti.png": "mango drink",
    "chole-bhature-chick-pea-curry-260nw-1072270634.png": "chole bhature",
    "pavbhaji.png": "pav bhaji",
    "Fried-veg-momos.jpg": "veg momos",
    "dosa.png": "dosa",
    "idli.png": "idli sambar",
    "veg-biryani.png": "veg biryani",
    "paneer-tikka.png": "paneer tikka",
    "samosa.png": "samosa",
    "aloo-paratha.png": "aloo paratha",
    "dal-rice.png": "dal rice",
    "kadhi-chawal.png": "kadhi chawal",
    "poha.png": "poha",
    "upma.png": "upma",
    "masala-dosa.png": "masala dosa",
    "uttapam.png": "uttapam",
    "medu-vada.png": "medu vada",
    "bhel-puri.png": "bhel puri",
    "pani-puri.png": "pani puri",
    "dahi-puri.png": "dahi puri",
    "aloo-tikki.png": "aloo tikki",
    "butter-naan.png": "butter naan",
    "paneer-butter-masala.png": "paneer butter masala",
    "dal-makhani.png": "dal makhani",
    "veg-pulao.png": "veg pulao",
    "jeera-rice.png": "jeera rice",
    "mix-veg.png": "mixed vegetable curry",
    "malai-kofta.png": "malai kofta",
    "gulab-jamun.png": "gulab jamun",
    "rasmalai.png": "rasmalai",
    "rava-dosa.png": "rava dosa",
    "pongal.png": "pongal",
    "sambar-rice.png": "sambar rice",
    "curd-rice.png": "curd rice",
    "lemon-rice.png": "lemon rice",
    "tamarind-rice.png": "tamarind rice",
    "sandwich.png": "veg sandwich",
    "burger.png": "burger",
    "pizza-slice.png": "pizza slice",
    "nachos.png": "nachos",
    "spring-roll.png": "spring roll",
    "manchurian.png": "veg manchurian",
    "hakka-noodles.png": "hakka noodles",
    "veg-fried-rice.png": "veg fried rice",
    "tomato-soup.png": "tomato soup",
    "hot-coffee.png": "hot coffee",
    "masala-chai.png": "masala chai",
    "lassi.png": "lassi",
    "jaljeera.png": "jaljeera",
    "fresh-lime.png": "fresh lime soda",
    "ice-cream.png": "ice cream",
    "brownie.png": "brownie",
    "cake-slice.png": "cake slice",
    "fruit-salad.png": "fruit salad",
    "kisspng-iced-coffee-latte-tea-cafe-cold-5abceb9127b3c7.9037224715223305131626.png": "iced coffee",
    "chocolateshake.jpg": "chocolate shake",
}

ctx = ssl.create_default_context()


def fetch_pexels_image_url(query):
    """Get first photo URL from Pexels search."""
    if PEXELS_API_KEY == "YOUR_PEXELS_API_KEY":
        return None
    url = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode(
        {"query": query, "per_page": "1", "orientation": "landscape"}
    )
    req = urllib.request.Request(url, headers={"Authorization": PEXELS_API_KEY})
    with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
        data = json.loads(r.read().decode())
    if not data.get("photos"):
        return None
    # Prefer medium size (~400px) for menu thumbnails
    photo = data["photos"][0]
    return photo.get("src", {}).get("medium") or photo.get("src", {}).get("large") or photo.get("src", {}).get("original")


def download_image(url: str, save_path: str) -> bool:
    """Download image from URL and save to path."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
        data = r.read()
    with open(save_path, "wb") as f:
        f.write(data)
    return len(data) > 1000


def main():
    if PEXELS_API_KEY == "YOUR_PEXELS_API_KEY":
        print("ERROR: Set your Pexels API key at the top of this file.")
        print("  1. Go to https://www.pexels.com/api/")
        print("  2. Sign up and copy your API key")
        print("  3. Open this file and replace YOUR_PEXELS_API_KEY with your key")
        return
    ok = 0
    fail = 0
    for filename, query in FILENAME_TO_QUERY.items():
        time.sleep(1)  # avoid rate limit
        out = os.path.join(PHOTOS_DIR, filename)
        try:
            url = fetch_pexels_image_url(query)
            if not url:
                print("No result:", filename, "query:", query)
                fail += 1
                continue
            if download_image(url, out):
                print("OK:", filename)
                ok += 1
            else:
                print("Skip (tiny):", filename)
                fail += 1
        except Exception as e:
            print("Fail:", filename, e)
            fail += 1
    print("Done. Downloaded:", ok, "Failed:", fail)


if __name__ == "__main__":
    main()
