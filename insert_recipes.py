# Insert recipes 21-62 into menu.html
with open('CafeHolic-main/htmlcodes/online-restaurant-orderjquery/dist/menu.html', 'r', encoding='utf-8') as f:
    html = f.read()
with open('menu_50_recipes.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
rest = ''.join(lines[377:]).rstrip()  # recipes 21-62

# Find after totalDialog20 block
marker = 'id="totalDialog20">Total: ₹<span class="totalAmount">20</span></h4>'
idx = html.find(marker)
if idx == -1:
    print("totalDialog20 not found")
    exit(1)
# Find closing of recipe 20 (two </div> then whitespace then </div></div> for recipe-menu)
start = html.find('</div>\n        </div>', idx)
if start == -1:
    print("recipe 20 closing not found")
    exit(1)
start += len('</div>\n        </div>')
# Now start is right after recipe 20. Find "\n\n      </div>\n    </div>\n\n    <div id="finishOrderDialog"'
end_marker = '\n\n      </div>\n    </div>\n\n    <div id="finishOrderDialog"'
end = html.find(end_marker, start)
if end == -1:
    print("finishOrderDialog marker not found")
    exit(1)
# Insert rest between start and end (replace the content between recipe 20 and the closing divs)
between = html[start:end]
new_between = '\n\n' + rest + end_marker
html = html[:start] + new_between + html[end + len(end_marker):]
with open('CafeHolic-main/htmlcodes/online-restaurant-orderjquery/dist/menu.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Inserted recipes 21-62")
