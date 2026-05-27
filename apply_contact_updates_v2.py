import re
import urllib.parse
from pathlib import Path

NEW_PHONE_DISPLAY = "+91 9848453938"
NEW_PHONE_NUMERIC = "919848453938"
MAP_QUERY = "Plot No 92 Ramreddy Nagar IDA Jeedimetla HYD-500055"
map_url = "https://www.google.com/maps?q=" + urllib.parse.quote_plus(MAP_QUERY) + "&output=embed"
MAP_IFRAME = '<iframe src="' + map_url + '" width="100%" height="250" style="border:0;" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'

phone_pattern = re.compile(r"\+91[\s-]?\d{10}")
tel_pattern = re.compile(r"tel:\+?91\d{10}")
wa_pattern = re.compile(r"https?://wa\.me/91\d{9,10}(\?[^\"'\s>]*)?")
api_wa_pattern = re.compile(r"(https?://api\.whatsapp\.com/send\?phone=)91\d{9,10}")

updated = []
for path in Path('.').rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    original = text

    # Replace visible phone numbers
    text = phone_pattern.sub(NEW_PHONE_DISPLAY, text)

    # Replace tel: links
    text = tel_pattern.sub('tel:+' + NEW_PHONE_NUMERIC, text)

    # Replace wa.me links and preserve query
    text = wa_pattern.sub(lambda m: 'https://wa.me/' + NEW_PHONE_NUMERIC + (m.group(1) or ''), text)

    # Replace api.whatsapp.com links
    text = api_wa_pattern.sub(lambda m: m.group(1) + NEW_PHONE_NUMERIC, text)

    # Embed map in index.html footer Contact column if not present
    if path.name.lower() == 'index.html' and 'google.com/maps' not in text:
        m = re.search(r'(<div[^>]*class=["\']footer-column["\'][^>]*>.*?<h3>\s*Contact\s*</h3>)(.*?)(</div>)', text, re.DOTALL | re.IGNORECASE)
        if m:
            col = m.group(0)
            # Insert iframe before the closing </div> of this column
            new_col = col.replace('</div>', MAP_IFRAME + '\n</div>', 1)
            text = text[:m.start()] + new_col + text[m.end():]

    if text != original:
        path.write_text(text, encoding='utf-8')
        updated.append(str(path))

print('Updated', len(updated))
for p in updated:
    print(p)
