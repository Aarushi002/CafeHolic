with open("menu.html", "r", encoding="utf-8") as f:
    content = f.read()

m1 = '<div class="recipe-menu">'
m2 = '</div>\n      </div>\n    </div>\n\n    <div id="finishOrderDialog" title="Confirm Order">'

print("Start found:", content.find(m1))
print("End found:", content.find(m2))

if content.find(m2) == -1:
    idx = content.find("finishOrderDialog")
    snippet = content[idx-250:idx+50]
    print("Snippet before finishOrderDialog:", repr(snippet))
