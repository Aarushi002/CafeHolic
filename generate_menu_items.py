# Generate 50 new menu recipe blocks and carousel items
items = [
    (13, "Dosa", "dosa.png", "Coconut Chutney", "Sambar"),
    (14, "Idli", "idli.png", "Sambar", "Chutney"),
    (15, "Veg Biryani", "veg-biryani.png", "Raita", "Salad"),
    (16, "Paneer Tikka", "paneer-tikka.png", "Mint Chutney", "Onion"),
    (17, "Samosa", "samosa.png", "Tamarind Chutney", "Green Chutney"),
    (18, "Aloo Paratha", "aloo-paratha.png", "Curd", "Pickle"),
    (19, "Dal Rice", "dal-rice.png", "Ghee", "Pickle"),
    (20, "Kadhi Chawal", "kadhi-chawal.png", "Rice", "Boondi"),
    (21, "Poha", "poha.png", "Sev", "Lemon"),
    (22, "Upma", "upma.png", "Coconut", "Chutney"),
    (23, "Masala Dosa", "masala-dosa.png", "Potato Masala", "Chutney"),
    (24, "Uttapam", "uttapam.png", "Onion", "Tomato"),
    (25, "Medu Vada", "medu-vada.png", "Sambar", "Coconut Chutney"),
    (26, "Bhel Puri", "bhel-puri.png", "Sev", "Tamarind"),
    (27, "Pani Puri", "pani-puri.png", "Pani", "Tamarind"),
    (28, "Dahi Puri", "dahi-puri.png", "Dahi", "Sev"),
    (29, "Aloo Tikki", "aloo-tikki.png", "Chutney", "Curd"),
    (30, "Butter Naan", "butter-naan.png", "Butter", "Garlic"),
    (31, "Paneer Butter Masala", "paneer-butter-masala.png", "Naan", "Onion"),
    (32, "Dal Makhani", "dal-makhani.png", "Butter", "Cream"),
    (33, "Veg Pulao", "veg-pulao.png", "Raita", "Salad"),
    (34, "Jeera Rice", "jeera-rice.png", "Dal", "Raita"),
    (35, "Mix Veg", "mix-veg.png", "Roti", "Salad"),
    (36, "Malai Kofta", "malai-kofta.png", "Naan", "Rice"),
    (37, "Gulab Jamun", "gulab-jamun.png", "Rabri", "None"),
    (38, "Rasmalai", "rasmalai.png", "Cardamom", "Pista"),
    (39, "Rava Dosa", "rava-dosa.png", "Chutney", "Sambar"),
    (40, "Pongal", "pongal.png", "Sambar", "Coconut Chutney"),
    (41, "Sambar Rice", "sambar-rice.png", "Ghee", "Papad"),
    (42, "Curd Rice", "curd-rice.png", "Pickle", "Pomegranate"),
    (43, "Lemon Rice", "lemon-rice.png", "Peanuts", "Curry Leaf"),
    (44, "Tamarind Rice", "tamarind-rice.png", "Peanuts", "Curry Leaf"),
    (45, "Sandwich", "sandwich.png", "Cheese", "Veggies"),
    (46, "Burger", "burger.png", "Lettuce", "Sauce"),
    (47, "Pizza Slice", "pizza-slice.png", "Cheese", "Olives"),
    (48, "Nachos", "nachos.png", "Salsa", "Cheese"),
    (49, "Spring Roll", "spring-roll.png", "Sauce", "Veggies"),
    (50, "Manchurian", "manchurian.png", "Sauce", "Spring Onion"),
    (51, "Hakka Noodles", "hakka-noodles.png", "Veggies", "Soy Sauce"),
    (52, "Veg Fried Rice", "veg-fried-rice.png", "Soy Sauce", "Veggies"),
    (53, "Tomato Soup", "tomato-soup.png", "Croutons", "Basil"),
    (54, "Hot Coffee", "hot-coffee.png", "Milk", "Sugar"),
    (55, "Masala Chai", "masala-chai.png", "Ginger", "Cardamom"),
    (56, "Lassi", "lassi.png", "Mango", "Roohafza"),
    (57, "Jaljeera", "jaljeera.png", "Mint", "Cumin"),
    (58, "Fresh Lime", "fresh-lime.png", "Salt", "Mint"),
    (59, "Ice Cream", "ice-cream.png", "Chocolate", "Vanilla"),
    (60, "Brownie", "brownie.png", "Walnut", "Ice Cream"),
    (61, "Cake Slice", "cake-slice.png", "Cream", "Fruit"),
    (62, "Fruit Salad", "fruit-salad.png", "Honey", "Mint"),
]

def id_base(name):
    return name.replace(" ", "")

def recipe_block(n, name, img, ing1, ing2):
    bid = id_base(name)
    return f'''        <!-- Recipe {n} -->
        <div class="recipe">
          <p class="name">{name}</p>
          <img src="../../photos/{img}" alt="{name}">
          <a class="btnStyle3 btnStyle addToCart" id="addToCart{bid}">Add to Cart</a>
          <p class="price">Half ₹20 | Full ₹40</p>
          <div id="checkOrder{bid}" title="{bid}" data-half="20" data-full="40" data-recipe-num="{n}">
            <div class="portion-choice">
              <label><input type="radio" name="portion{bid}" value="20" checked> Half plate ₹20</label>
              <label><input type="radio" name="portion{bid}" value="40"> Full plate ₹40</label>
            </div>
            <h3 class="listHeading">List of Ingredients:</h3>
            <ul class="listOfIngredients" id="recipe{n}">
              <li><input type="checkbox" checked>{ing1}</li>
              <li><input type="checkbox" checked>{ing2}</li>
            </ul>
            <a class="btnStyle3 btnStyle addIngredient">Add Ingredient</a>
            <a class="btnStyle listOver">Done</a>
            <h4 class="totalDialog" id="totalDialog{n}">Total: ₹<span class="totalAmount">20</span></h4>
          </div>
        </div>
'''

def carousel_item(name, img, tagline):
    return f'''            <div class="col-lg-4">
              <img class="testimonial-image" src="photos/{img}" alt="{name}">
              <div class="feature-box">
                <h3>{name.upper()}</h3>
                <p>{tagline}</p>
              </div>
            </div>
'''

carousel_taglines = [
    "Crispy and delicious!", "Soft and fluffy!", "Fragrant and filling!", "Smoky and spicy!",
    "Crispy outside, soft inside!", "Hearty and wholesome!", "Comfort in a plate!", "Light and tasty!",
    "Perfect breakfast!", "Savory and satisfying!", "Loaded with flavor!", "Crispy edges!", "Classic street food!",
    "Tangy and sweet!", "Cool and refreshing!", "Crispy and tangy!", "Spiced and crispy!", "Buttery and soft!",
    "Creamy and rich!", "Creamy dal goodness!", "Fragrant rice!", "Aromatic and light!", "Wholesome mix!",
    "Creamy gravy!", "Sweet and syrupy!", "Milk and saffron!", "Crispy and golden!", "Comfort food!",
    "South Indian staple!", "Cool and creamy!", "Tangy and fresh!", "Sweet and tangy!", "Toasted and cheesy!",
    "Juicy and filling!", "Cheesy and hot!", "Crunchy and cheesy!", "Crispy and savory!", "Spicy and saucy!",
    "Stir-fried goodness!", "Wok-tossed rice!", "Warm and comforting!", "Hot and strong!", "Spiced tea!",
    "Cool and sweet!", "Refreshing drink!", "Zesty and fresh!", "Cold and sweet!", "Chocolatey treat!",
    "Sweet slice!", "Fresh and healthy!",
]

menu_html = "\n".join(recipe_block(n, name, img, i1, i2) for n, name, img, i1, i2 in items)
carousel_html = ""
for i, (n, name, img, i1, i2) in enumerate(items):
    tag = carousel_taglines[i] if i < len(carousel_taglines) else "Delicious!"
    carousel_html += carousel_item(name, img, tag)

# Write to files for manual inclusion
with open("menu_50_recipes.txt", "w", encoding="utf-8") as f:
    f.write(menu_html)
with open("carousel_50_items.txt", "w", encoding="utf-8") as f:
    f.write(carousel_html)
print("Generated menu_50_recipes.txt and carousel_50_items.txt")
# Also output list of image filenames for README
with open("new_photo_list.txt", "w", encoding="utf-8") as f:
    for _, _, img, _, _ in items:
        f.write(img + "\n")
print("Generated new_photo_list.txt")
