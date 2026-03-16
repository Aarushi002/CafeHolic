# Add 50 carousel items to index.html as new slides (3 per slide)
import re
with open('CafeHolic-main/htmlcodes/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
with open('carousel_50_items.txt', 'r', encoding='utf-8') as f:
    content = f.read()
# Each item: from "            <div class=\"col-lg-4\">" to next "            <div" or end
parts = content.strip().split('\n            <div class="col-lg-4">')
items = []
for p in parts:
    if not p.strip():
        continue
    items.append('            <div class="col-lg-4">' + p.strip())
# Now wrap every 3 items in carousel-item
slides_html = []
for i in range(0, len(items), 3):
    chunk = items[i:i+3]
    slide = '\n        <div class="carousel-item">\n          <div class="row">\n' + '\n'.join(chunk) + '\n          </div>\n        </div>'
    slides_html.append(slide)
new_slides = '\n'.join(slides_html)
# Insert before carousel-control-prev (after the third carousel-item)
marker = '      </div>\n      <a class="carousel-control-prev"'
idx = html.rfind(marker)  # last occurrence (the one after carousel-inner)
if idx == -1:
    print("carousel-control-prev not found")
    exit(1)
# Insert new_slides before the closing </div> of carousel-inner and the control
# So we want to replace "      </div>\n      <a class="carousel-control-prev"" with "      " + new_slides + "\n      </div>\n      <a class=\"carousel-control-prev\""
# Actually the structure is: </div> (row) </div> (carousel-item) </div> (carousel-inner) <a control-prev
# So we need to insert new_slides before the "</div>" that closes carousel-inner. So find "</div>\n      <a class=\"carousel-control-prev\"" and the </div> is the carousel-inner close. So insert new_slides + "\n      " before that </div>.
insert_point = idx  # we insert at idx, so we add new_slides + "\n      " and keep "</div>\n      <a..."
html = html[:idx] + new_slides + '\n      ' + html[idx:]
with open('CafeHolic-main/htmlcodes/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Added 50 carousel items as", len(slides_html), "slides")
