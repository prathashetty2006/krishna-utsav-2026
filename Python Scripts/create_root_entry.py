import os

def generate_root_index():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_html = os.path.join(base_dir, "HTML and CSS", "index.html")
    target_html = os.path.join(base_dir, "index.html")

    with open(source_html, "r", encoding="utf-8") as f:
        content = f.read()

    # Adjust paths for root deployment
    updated = content.replace('href="index.css"', 'href="HTML and CSS/index.css"')
    updated = updated.replace('src="../Java Script/index.js"', 'src="Java Script/index.js"')
    updated = updated.replace('src="../Image and Audio/', 'src="Image and Audio/')

    with open(target_html, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"Created root index.html successfully ({len(updated)} bytes)")

if __name__ == "__main__":
    generate_root_index()
