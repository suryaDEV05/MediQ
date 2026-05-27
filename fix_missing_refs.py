import base64
import os
import pathlib
import re
from pathlib import Path

root = Path('s:/MediQ')
missing = set()
for html_file in sorted(root.rglob('*.html')):
    text = html_file.read_text(encoding='utf-8', errors='replace')
    for m in re.finditer(r'(?:src|href)=["\"]([^"\']+)["\"]', text):
        ref = m.group(1)
        if ref.startswith(('http://','https://','#','mailto:','tel:','javascript:')):
            continue
        clean = ref.split('?')[0].split('#')[0]
        if clean == '':
            continue
        target = (html_file.parent / clean).resolve()
        if not target.exists():
            missing.add((str(html_file.relative_to(root)), clean))

print(f'Found {len(missing)} missing references')

# Minimal 1x1 transparent PNG bytes
placeholder_png = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVQYV2NgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII='
)

created = {'images':0, 'pages':0}
for source, ref in sorted(missing):
    source_path = root / source
    path = (source_path.parent / ref).resolve()
    if root not in path.parents and path != root:
        # if ref is outside repo due to ../ going above root, skip
        continue
    if ref.lower().endswith('.html'):
        if path.exists():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        title = Path(ref).stem.replace('-', ' ').replace('_', ' ').title()
        rel_style = Path(os.path.relpath(root / 'style.css', start=path.parent)).as_posix()
        rel_script = Path(os.path.relpath(root / 'script.js', start=path.parent)).as_posix()
        body_path = Path(ref).parent
        category_link = ''
        if 'details/' in ref:
            parent_category = ref.split('/')[1] if '/' in ref else ''
            if parent_category:
                category_link = f'<p><a href="{Path(os.path.relpath(root / (parent_category + ".html"), start=path.parent)).as_posix()}">Back to {parent_category.title()} products</a></p>'
        content = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <meta name=\"description\" content=\"{title} product details page placeholder for MEDIQ Healthcare Equipment.\">
  <title>{title} | MEDIQ Healthcare Equipment</title>
  <link rel=\"stylesheet\" href=\"{rel_style}\"> 
  <link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css\">
</head>
<body>
  <div class=\"container section-padding\">
    <h1>{title}</h1>
    <p>This product detail page is a placeholder created to preserve website navigation and layout.</p>
    {category_link}
    <p><a href=\"{Path(os.path.relpath(root / 'index.html', start=path.parent)).as_posix()}\">Back to Home</a></p>
  </div>
  <script src=\"{rel_script}\"></script>
</body>
</html>"""
        path.write_text(content, encoding='utf-8')
        created['pages'] += 1
    elif ref.lower().endswith(('.jpg','.jpeg','.png','.gif','.svg','.webp')):
        if path.exists():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        if ref.lower().endswith(('.jpg','.jpeg')):
            path.write_bytes(placeholder_png)
        elif ref.lower().endswith('.png'):
            path.write_bytes(placeholder_png)
        elif ref.lower().endswith('.gif'):
            path.write_bytes(placeholder_png)
        elif ref.lower().endswith('.svg'):
            path.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400"><rect width="100%" height="100%" fill="#e2e8f0"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="Inter, sans-serif" font-size="24" fill="#0f172a">Placeholder image</text></svg>', encoding='utf-8')
        else:
            path.write_bytes(placeholder_png)
        created['images'] += 1
    else:
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('', encoding='utf-8')
            created['pages'] += 1
print('Created placeholders:', created)
