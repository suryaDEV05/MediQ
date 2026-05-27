import re
from pathlib import Path

ROOT = Path('.')
PHONE_EXPECTED = re.compile(r'\+91\s*9848453938')
phone_any = re.compile(r'\+91[\s-]?\d{10}')

missing_assets = []
issues = {}
fixed_files = []

for path in sorted(ROOT.rglob('*.html')):
    text = path.read_text(encoding='utf-8')
    orig = text
    file_issues = []

    # Ensure head meta charset exists
    head_match = re.search(r'<head[^>]*>', text, re.IGNORECASE)
    if head_match:
        head_end = head_match.end()
        head_section = text[head_end: head_end+500]
        if 'charset' not in head_section.lower():
            insert = '\n  <meta charset="UTF-8" />\n'
            text = text[:head_end] + insert + text[head_end:]
            file_issues.append('Inserted <meta charset> in <head>')

    # Ensure title exists
    if '<title' not in text.lower():
        # insert simple title after head tag
        if head_match:
            insert = '\n  <title>' + path.stem + '</title>\n'
            text = text[:head_end] + insert + text[head_end:]
            file_issues.append('Inserted <title>')

    # Add alt to images missing alt
    def add_alt(m):
        tag = m.group(0)
        if 'alt=' in tag.lower():
            return tag
        # find src
        src_m = re.search(r'src=["\']([^"\']+)["\']', tag)
        alt_text = Path(src_m.group(1)).stem if src_m else 'image'
        newtag = tag[:-1] + f' alt="{alt_text}"' + '>'
        return newtag
    text, nimg = re.subn(r'<img[^>]*>', add_alt, text, flags=re.IGNORECASE)
    if nimg>0:
        file_issues.append(f'Added alt to {nimg} <img> tags where missing')

    # Ensure closing body/html
    if '</body>' not in text.lower():
        text = text + '\n</body>'
        file_issues.append('Appended </body>')
    if '</html>' not in text.lower():
        text = text + '\n</html>'
        file_issues.append('Appended </html>')

    # Check local asset links: script src, link href rel=stylesheet, img src
    for m in re.finditer(r'(?:src|href)=["\']([^"\']+)["\']', text):
        ref = m.group(1)
        if re.match(r'https?://', ref):
            continue
        # strip query/hash
        ref_path = ref.split('?')[0].split('#')[0]
        refp = (path.parent / ref_path).resolve()
        # only check relative inside repo
        try:
            repo_root = ROOT.resolve()
            if not str(refp).startswith(str(repo_root)):
                continue
        except Exception:
            pass
        if not refp.exists():
            missing_assets.append((str(path), ref))

    # Check internal HTML links
    for m in re.finditer(r'href=["\']([^"\']+\.html)["\']', text, flags=re.IGNORECASE):
        ref = m.group(1)
        if re.match(r'https?://', ref):
            continue
        refp = (path.parent / ref).resolve()
        if not refp.exists():
            file_issues.append(f'Broken HTML link: {ref}')

    # Check phone numbers
    phones = phone_any.findall(text)
    for p in phones:
        if not PHONE_EXPECTED.search(p):
            file_issues.append(f'Unexpected phone number: {p}')

    if text != orig:
        path.write_text(text, encoding='utf-8')
        fixed_files.append(str(path))

    if file_issues:
        issues[str(path)] = file_issues

# Deduplicate missing assets
missing_assets = list(dict.fromkeys(missing_assets))

# Output summary
print('Final site check summary')
print('Checked HTML files:', len(list(ROOT.rglob("*.html"))))
print('Files modified with safe fixes:', len(fixed_files))
for f in fixed_files[:50]:
    print('  -', f)
print('Files with reported issues:', len(issues))
for f,its in list(issues.items())[:200]:
    print('  -', f)
    for it in its:
        print('     *', it)
if missing_assets:
    print('\nMissing asset references:')
    for p,ref in missing_assets[:200]:
        print('  -', p, '->', ref)
else:
    print('\nNo missing assets detected (relative files).')
