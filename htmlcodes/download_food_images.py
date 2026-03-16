"""Download dish-specific food images into photos/ so menu and carousel show images.

This script uses Unsplash's simple source endpoint with a cuisine/food query
per dish name (e.g. ?food,dosa). Filenames are the ones expected by the app.
"""
import os
import urllib.request
import ssl

PHOTOS_DIR = os.path.join(os.path.dirname(__file__), "photos")
os.makedirs(PHOTOS_DIR, exist_ok=True)

# All filenames the menu/carousel expect (from README and menu paths)
FILENAMES = [
    "ChholeBhature.png", "PavBhaji2.png", "Chowmein.png", "Macaroni.jpg", "Pasta.jpg",
    "chillipotato.jpg", "Fries.jpg", "ChholeChawal.jpeg", "Rajma_Chawal.jpg", "frooti.png",
    "chole-bhature-chick-pea-curry-260nw-1072270634.png", "pavbhaji.png", "Fried-veg-momos.jpg",
    "dosa.png", "idli.png", "veg-biryani.png", "paneer-tikka.png", "samosa.png",
    "aloo-paratha.png", "dal-rice.png", "kadhi-chawal.png", "poha.png", "upma.png",
    "masala-dosa.png", "uttapam.png", "medu-vada.png", "bhel-puri.png", "pani-puri.png",
    "dahi-puri.png", "aloo-tikki.png", "butter-naan.png", "paneer-butter-masala.png", "dal-makhani.png",
    "veg-pulao.png", "jeera-rice.png", "mix-veg.png", "malai-kofta.png", "gulab-jamun.png",
    "rasmalai.png", "rava-dosa.png", "pongal.png", "sambar-rice.png", "curd-rice.png",
    "lemon-rice.png", "tamarind-rice.png", "sandwich.png", "burger.png", "pizza-slice.png",
    "nachos.png", "spring-roll.png", "manchurian.png", "hakka-noodles.png", "veg-fried-rice.png",
    "tomato-soup.png", "hot-coffee.png", "masala-chai.png", "lassi.png", "jaljeera.png",
    "fresh-lime.png", "ice-cream.png", "brownie.png", "cake-slice.png", "fruit-salad.png",
]
# Cold coffee, chocolate shake - menu may use different names
EXTRA = ["kisspng-iced-coffee-latte-tea-cafe-cold-5abceb9127b3c7.9037224715223305131626.png", "chocolateshake.jpg"]

FILENAMES.extend(EXTRA)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Map filename (lowercased) to an Unsplash food query
QUERIES = {
    "chholebhature.png": "indian,food,chole,bhature,plate",
    "pavbhaji2.png": "indian,food,pav,bhaji,street",
    "chowmein.png": "indian,veg,chowmein,noodles",
    "macaroni.jpg": "macaroni,pasta,cheese",
    "pasta.jpg": "pasta,italian,restaurant",
    "chillipotato.jpg": "chilli,potato,indo chinese",
    "fries.jpg": "french,fries",
    "chholechawal.jpeg": "chole,rice,indian,plate",
    "rajma_chawal.jpg": "rajma,rice,indian",
    "frooti.png": "mango,juice,bottle",
    "chole-bhature-chick-pea-curry-260nw-1072270634.png": "chickpea,curry,indian",
    "pavbhaji.png": "pav,bhaji,indian",
    "fried-veg-momos.jpg": "veg,momos,dumplings",
    "dosa.png": "dosa,south indian,breakfast",
    "idli.png": "idli,sambar,chutney",
    "veg-biryani.png": "veg,biryani,indian,rice",
    "paneer-tikka.png": "paneer,tikka,skewers",
    "samosa.png": "samosa,indian,snack",
    "aloo-paratha.png": "aloo,paratha,indian,stuffed,bread",
    "dal-rice.png": "dal,rice,indian,comfort,food",
    "kadhi-chawal.png": "kadhi,rice,indian",
    "poha.png": "poha,indian,breakfast",
    "upma.png": "upma,indian,breakfast",
    "masala-dosa.png": "masala,dosa,south indian",
    "uttapam.png": "uttapam,south indian",
    "medu-vada.png": "medu,vada,sambar",
    "bhel-puri.png": "bhel,puri,chaat,street,food",
    "pani-puri.png": "pani,puri,golgappa,chaat",
    "dahi-puri.png": "dahi,puri,chaat",
    "aloo-tikki.png": "aloo,tikki,chaat",
    "butter-naan.png": "butter,naan,indian,bread",
    "paneer-butter-masala.png": "paneer,butter,masala,curry",
    "dal-makhani.png": "dal,makhani,curry",
    "veg-pulao.png": "veg,pulao,rice",
    "jeera-rice.png": "jeera,rice,cumin",
    "mix-veg.png": "mixed,vegetable,curry",
    "malai-kofta.png": "malai,kofta,curry",
    "gulab-jamun.png": "gulab,jamun,indian,dessert",
    "rasmalai.png": "rasmalai,indian,sweet",
    "rava-dosa.png": "rava,dosa",
    "pongal.png": "pongal,south indian",
    "sambar-rice.png": "sambar,rice,south indian",
    "curd-rice.png": "curd,rice,south indian",
    "lemon-rice.png": "lemon,rice,south indian",
    "tamarind-rice.png": "tamarind,rice,south indian",
    "sandwich.png": "grilled,veg,sandwich",
    "burger.png": "burger,fast,food",
    "pizza-slice.png": "pizza,slice,cheese",
    "nachos.png": "nachos,cheese",
    "spring-roll.png": "veg,spring,rolls",
    "manchurian.png": "veg,manchurian",
    "hakka-noodles.png": "hakka,noodles,indo chinese",
    "veg-fried-rice.png": "veg,fried,rice",
    "tomato-soup.png": "tomato,soup",
    "hot-coffee.png": "hot,coffee,cup",
    "masala-chai.png": "masala,chai,tea",
    "lassi.png": "lassi,indian,drink",
    "jaljeera.png": "jaljeera,drink",
    "fresh-lime.png": "fresh,lime,soda",
    "ice-cream.png": "ice,cream,scoops",
    "brownie.png": "chocolate,brownie,dessert",
    "cake-slice.png": "cake,slice,dessert",
    "fruit-salad.png": "fruit,salad,bowl",
    "kisspng-iced-coffee-latte-tea-cafe-cold-5abceb9127b3c7.9037224715223305131626.png": "iced,coffee,latte",
    "chocolateshake.jpg": "chocolate,shake,drink",
}

def query_for(filename: str) -> str:
    key = filename.lower()
    return QUERIES.get(key, "indian,food,plate")

for fn in FILENAMES:
    out = os.path.join(PHOTOS_DIR, fn)
    q = query_for(fn).replace(" ", "+")
    # Unsplash source endpoint with query
    url = f"https://source.unsplash.com/featured/400x300/?{q}"
    try:
        print("Downloading", fn, "from", url)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            data = r.read()
        with open(out, "wb") as f:
            f.write(data)
        print("Downloaded (overwrote if existed):", fn)
    except Exception as e:
        print("Failed", fn, e)

print("Done.")
