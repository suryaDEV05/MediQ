import re
from pathlib import Path

NEW_PHONE = "+91 9848453938"
NEW_PHONE_NUMERIC = "+919848453938"
MAP_QUERY = "Plot No 92 Ramreddy Nagar IDA Jeedimetla HYD-500055"
MAP_IFRAME = f"<iframe src=\"https://www.google.com/maps?q={re.sub(r'\\s+', '+', MAP_QUERY)}&output=embed\" width=\"100%\" height=\"250\" style=\"border:0;\" loading=\"lazy\" referrerpolicy=\"no-referrer-when-downgrade\"></iframe>"

html_files = list(Path('.').rglob('*.html'))
updated = []

phone_pattern = re.compile(r'\+91[\s-]?\d{10}')
wa_pattern = re.compile(r'https?://wa\.me/91\d{9,10}(\?[^"\'\s>]*)?')
tel_pattern = re.compile(r'tel:\+91\d{10}')

for path in html_files:
    text = path.read_text(encoding='utf-8')
    original = text

    # Update visible phone numbers like +91 9876543210 -> NEW_PHONE
    text = phone_pattern.sub(NEW_PHONE, text)

    # Update tel: links
    text = tel_pattern.sub('tel:' + NEW_PHONE_NUMERIC, text)

    # Update wa.me links, preserve query if any
    def wa_repl(m):
        q = m.group(1) or ''
        return 'https://wa.me/' + NEW_PHONE_NUMERIC + q
    text = wa_pattern.sub(wa_repl, text)

    # Also update whatsapp links that use query parameters with numbers in query
    text = re.sub(r'(https?://api\.whatsapp\.com/send\?phone=)91\d{9,10}', r'\1' + NEW_PHONE_NUMERIC, text)

    # Ensure Owner paragraph and Manufacturing Unit paragraph exist after email paragraph in Contact blocks
    if 'info@mediqhealthcare.com' in text:
        # Find email closing </p> after the email occurrence
        idx = text.find('info@mediqhealthcare.com')
        if idx != -1:
            # find the closing </p> after idx
            close_p = text.find('</p>', idx)
            insert_block = ''
            # Check for Owner presence within next 300 chars
            snippet_after = text[idx: idx+400]
            if 'Owner:' not in snippet_after:
                insert_block += '\n                <p>\n                    Owner: Srinivas.N\n                </p>'
            if 'Manufacturing Unit:' not in snippet_after:
                insert_block += '\n                <p>\n                    Manufacturing Unit: Plot No:92 Ramreddy Nagar IDA Jeedimetla<br>\n                    HYD-500055<br>\n                    Manufacture Of Hospital Furniture & Equipment\n                </p>'
            if insert_block and close_p != -1:
                # Insert right after the closing </p> of the email
                insert_pos = close_p + len('</p>')
                text = text[:insert_pos] + insert_block + text[insert_pos:]

    # For index.html, embed the map inside the Contact footer column after contact paragraphs
    if path.name.lower() == 'index.html':
        if 'Manufacturing Unit:' in text and 'google.com/maps' not in text:
            # find the contact column end (closing </div> of the column). We will insert iframe before the closing </div> of footer-column containing Contact header.
            # Locate '<h3>Contact'</h3>
            m = re.search(r'(<div[^>]*class="footer-column"[^>]*>.*?<h3>\s*Contact\s*</h3>)(.*?)</div>', text, re.DOTALL|re.IGNORECASE)
            if m:
                # insert iframe before the column closing </div>
                col_start = m.start()
                col_end = m.end()
                col_html = m.group(0)
                if 'google.com/maps' not in col_html:
                    # insert iframe before the trailing </div>
                    new_col = col_html.replace('</div>', MAP_IFRAME + '\n</div>', 1)
                    text = text[:col_start] + new_col + text[col_end:]

    if text != original:
        path.write_text(text, encoding='utf-8')
        updated.append(str(path))

print('Updated', len(updated))
for u in updated:
    print(u)
