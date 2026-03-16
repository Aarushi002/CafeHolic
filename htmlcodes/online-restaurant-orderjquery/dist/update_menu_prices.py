# -*- coding: utf-8 -*-
"""Update menu.html: add cuisine categories and randomized cafeteria prices (all under 200)."""
import re

# Recipe number -> (category, half_price, full_price). Single-portion items: half=full.
PRICES = {
    1: ("North Indian", 45, 85),    # Chole Bhature
    2: ("North Indian", 40, 75),    # Pav Bhaji
    3: ("Chinese", 40, 75),         # Chowmein
    4: ("Chinese", 35, 65),         # Macaroni
    5: ("Chinese", 40, 70),         # Pasta
    6: ("Chinese", 35, 60),         # Chilli Potato
    7: ("Snacks & Fast Food", 30, 55),  # French Fries
    8: ("North Indian", 35, 65),    # Chhole Chawal
    9: ("North Indian", 35, 65),    # Rajma Chawal
    10: ("Beverages", 35, 60),      # Cold Coffee
    11: ("Beverages", 45, 75),      # Chocolate Shake
    12: ("Beverages", 25, 25),      # Frooti (single)
    13: ("South Indian", 35, 65),   # Dosa
    14: ("South Indian", 25, 50),   # Idli
    15: ("North Indian", 50, 95),   # Veg Biryani
    16: ("North Indian", 45, 85),   # Paneer Tikka
    17: ("Snacks & Fast Food", 25, 45),  # Samosa
    18: ("North Indian", 30, 55),   # Aloo Paratha
    19: ("North Indian", 30, 55),   # Dal Rice
    20: ("North Indian", 35, 60),   # Kadhi Chawal
    30: ("North Indian", 25, 45),   # Butter Naan
    31: ("North Indian", 55, 95),   # Paneer Butter Masala
    32: ("North Indian", 45, 85),   # Dal Makhani
    33: ("North Indian", 40, 75),   # Veg Pulao
    34: ("North Indian", 25, 45),   # Jeera Rice
    35: ("North Indian", 35, 65),   # Mix Veg
    36: ("North Indian", 50, 90),   # Malai Kofta
    37: ("Desserts", 35, 60),       # Gulab Jamun
    38: ("Desserts", 45, 75),       # Rasmalai
    39: ("South Indian", 40, 70),   # Rava Dosa
    40: ("South Indian", 35, 60),   # Pongal
    41: ("South Indian", 35, 65),   # Sambar Rice
    42: ("South Indian", 30, 55),   # Curd Rice
    43: ("South Indian", 30, 55),   # Lemon Rice
    44: ("South Indian", 35, 60),   # Tamarind Rice
    45: ("Snacks & Fast Food", 35, 65),  # Sandwich
    46: ("Snacks & Fast Food", 45, 85),  # Burger
    47: ("Snacks & Fast Food", 40, 75),  # Pizza Slice
    48: ("Snacks & Fast Food", 40, 70),  # Nachos
    49: ("Chinese", 35, 65),        # Spring Roll
    50: ("Chinese", 40, 70),        # Manchurian
    51: ("Chinese", 40, 75),        # Hakka Noodles
    52: ("Chinese", 40, 75),        # Veg Fried Rice
    53: ("Beverages", 35, 60),      # Tomato Soup
    54: ("Beverages", 30, 50),      # Hot Coffee
    55: ("Beverages", 20, 35),      # Masala Chai
    56: ("Beverages", 30, 55),      # Lassi
    57: ("Beverages", 25, 45),      # Jaljeera
    58: ("Beverages", 25, 45),     # Fresh Lime
    59: ("Desserts", 40, 70),      # Ice Cream
    60: ("Desserts", 45, 45),       # Brownie (single)
    61: ("Desserts", 50, 50),       # Cake Slice (single)
    62: ("Desserts", 55, 55),       # Fruit Salad (single)
}

def section_id(cat):
    return re.sub(r'[^\w\-]', '', cat.replace(' ', '-').lower())

def main():
    path = "menu.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # 0) Fix Butter Naan missing recipe wrapper and comment (recipe 30)
    html = html.replace(
        '        </div>\n\n          <img src="../../photos/butter-naan.png" alt="Butter Naan">\n          <a class="btnStyle3 btnStyle addToCart" id="addToCartButterNaan">',
        '        </div>\n\n        <!-- Recipe 30 -->\n        <div class="recipe">\n          <p class="name">Butter Naan</p>\n          <img src="../../photos/butter-naan.png" alt="Butter Naan">\n          <a class="btnStyle3 btnStyle addToCart" id="addToCartButterNaan">'
    )
    # 1) Insert category sections: after <div class="recipe-menu"> add first section
    html = html.replace(
        '<div class="recipe-menu">\n\n        <!-- Recipe 1 -->',
        '<div class="recipe-menu">\n        <section class="menu-category" id="north-indian">\n          <h2 class="category-heading">North Indian</h2>\n        <!-- Recipe 1 -->'
    )

    # 2) For each recipe num: update data-half, data-full, portion radios, totalAmount
    for num, (cat, half, full) in PRICES.items():
        # Already using half, full in data so dialog works. Just need to update data-half, data-full and the radio values/labels.
        # General replacement for div with data-recipe-num="num"
        pattern = r'(data-half=")\d+(" data-full=")\d+(" data-recipe-num="' + str(num) + '")'
        replacement = r'\g<1>' + str(half) + r'\g<2>' + str(full) + r'\g<3>'
        html = re.sub(pattern, replacement, html, count=1)

        # Portion radios: name="portionXXX" value="20" checked> Half plate ₹20</label><label><input type="radio" name="portionXXX" value="40"> Full plate ₹40
        # We need to match the exact name for each recipe. So we do per-recipe replacement for the block that has data-recipe-num="num"
        # Match the div that contains data-recipe-num="num", then replace its portion-choice content
        portion_pattern = (
            r'(<div id="checkOrder[^"]+"[^>]*data-recipe-num="' + str(num) + '"[^>]*>)\s*'
            r'<div class="portion-choice">\s*'
            r'<label><input type="radio" name="[^"]+" value="\d+"([^>]*)> [^<]+</label>\s*'
            r'<label><input type="radio" name="[^"]+" value="\d+"> [^<]+</label>\s*'
            r'</div>'
        )
        pname = "portion" + _portion_name(num)
        if half == full:
            portion_repl = (
                r'\1<div class="portion-choice">'
                r'<label><input type="radio" name="' + pname + '" value="' + str(half) + '" checked> ₹' + str(half) + '</label>'
                r'</div>'
            )
        else:
            portion_repl = (
                r'\1<div class="portion-choice">'
                r'<label><input type="radio" name="' + pname + '" value="' + str(half) + '" checked> Half ₹' + str(half) + '</label> '
                r'<label><input type="radio" name="' + pname + '" value="' + str(full) + '"> Full ₹' + str(full) + '</label>'
                r'</div>'
            )
        html = re.sub(portion_pattern, portion_repl, html, count=1)

        # Total amount span: <span class="totalAmount">20</span> inside totalDialog + num
        html = re.sub(
            r'(id="totalDialog' + str(num) + '"[^>]*>Total: ₹<span class="totalAmount">)\d+(</span>)',
            r'\g<1>' + str(half) + r'\g<2>',
            html,
            count=1
        )

    # 3) Update displayed price line <p class="price"> for each recipe (we already did in step 2? No - we only replaced when followed by checkOrder div. Let me add explicit replacements for each recipe's price line.)
    # Actually the first regex _replace_price_and_data was supposed to replace the price line - but I used a lambda that doesn't have the replacement built. Let me do simple search/replace for each recipe's price.
    for num, (cat, half, full) in PRICES.items():
        if num == 12:
            continue  # already special
        # Find the recipe block for num: from <!-- Recipe N --> or previous </div> to the <p class="price"> line
        # Simpler: replace any <p class="price">Half ₹X | Full ₹Y</p> that appears in the file - but there are many. We need to replace only the one for recipe num.
        # So we replace in context of data-recipe-num="num". So replace the price line that is 2-4 lines before data-recipe-num="num".
        # Pattern: <p class="price">ANY</p> ... <div id="checkOrder... data-recipe-num="num"
        old_price = re.search(
            r'(<p class="price">)[^<]+(</p>\s*\n\s*<div id="checkOrder[^"]+"[^>]*data-recipe-num="' + str(num) + '")',
            html
        )
        if old_price:
            if half == full:
                new_price = r'\1₹' + str(half) + r'\2'
            else:
                new_price = r'\1Half ₹' + str(half) + r' | Full ₹' + str(full) + r'\2'
            html = re.sub(
                r'(<p class="price">)[^<]+(</p>\s*\n\s*<div id="checkOrder[^"]+"[^>]*data-recipe-num="' + str(num) + '")',
                new_price,
                html,
                count=1
            )
    # Frooti price
    html = re.sub(
        r'<p class="price">₹ MRP</p>\s*\n\s*<div id="checkOrderFrooti"',
        '<p class="price">₹25</p>\n          <div id="checkOrderFrooti"',
        html,
        count=1
    )

    # 4) Insert section breaks (close section, open new) before recipes that start a new category
    order = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62]
    prev_cat = None
    for num in order:
        if num not in PRICES:
            continue
        cat = PRICES[num][0]
        if prev_cat is not None and cat != prev_cat:
            # Insert </section><section...><h2>Cat</h2> before this recipe's block
            # Recipe block for num starts with <!-- Recipe num --> or <div class="recipe"> with this recipe
            sid = section_id(cat)
            insert = '</section>\n        <section class="menu-category" id="' + sid + '">\n          <h2 class="category-heading">' + cat + '</h2>\n        '
            # Insert before "        <!-- Recipe N -->" for this num
            html = html.replace(
                '        <!-- Recipe ' + str(num) + ' -->',
                insert + '        <!-- Recipe ' + str(num) + ' -->',
                1
            )
        prev_cat = cat

    # 5) Close last section before </div> of recipe-menu
    html = re.sub(r'(        </div>\s*\n)(\s*</div>\s*\n\s*<div id="finishOrderDialog")', r'\1        </section>\n\2', html, count=1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated menu.html with categories and prices.")

def _portion_name(num):
    """Return the portion input name suffix for recipe num (e.g. CholeBhature for 1)."""
    names = {
        1: "CholeBhature", 2: "PavBhaji", 3: "Chowmein", 4: "Macaroni", 5: "Pasta",
        6: "ChilliPotato", 7: "FrenchFries", 8: "ChholeChawal", 9: "RajmaChawal",
        10: "ColdCoffee", 11: "ChocolateShake", 12: "Frooti", 13: "Dosa", 14: "Idli",
        15: "VegBiryani", 16: "PaneerTikka", 17: "Samosa", 18: "AlooParatha", 19: "DalRice",
        20: "KadhiChawal", 30: "ButterNaan", 31: "PaneerButterMasala", 32: "DalMakhani",
        33: "VegPulao", 34: "JeeraRice", 35: "MixVeg", 36: "MalaiKofta", 37: "GulabJamun",
        38: "Rasmalai", 39: "RavaDosa", 40: "Pongal", 41: "SambarRice", 42: "CurdRice",
        43: "LemonRice", 44: "TamarindRice", 45: "Sandwich", 46: "Burger", 47: "PizzaSlice",
        48: "Nachos", 49: "SpringRoll", 50: "Manchurian", 51: "HakkaNoodles", 52: "VegFriedRice",
        53: "TomatoSoup", 54: "HotCoffee", 55: "MasalaChai", 56: "Lassi", 57: "Jaljeera",
        58: "FreshLime", 59: "IceCream", 60: "Brownie", 61: "CakeSlice", 62: "FruitSalad",
    }
    return names.get(num, "Recipe" + str(num))

def _replace_price_and_data(match, num, half, full, is_frooti):
    # Not used in the end - we do separate replacements
    return match.group(0)

if __name__ == "__main__":
    main()
