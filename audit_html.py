import pathlib
import collections
from html.parser import HTMLParser

root = pathlib.Path('s:/MediQ')

class AuditParser(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids = []
        self.img_no_alt = []
        self.title_count = 0
        self.meta_charset = False
        self.meta_viewport = False
        self.meta_description = False
        self.scripts = []
        self.styles = []
        self.hrefs = []
        self.in_title = False
        self.title_text = ''

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'title':
            self.title_count += 1
            self.in_title = True
        if tag == 'meta':
            if attrs.get('charset'):
                self.meta_charset = True
            if attrs.get('name', '').lower() == 'viewport':
                self.meta_viewport = True
            if attrs.get('name', '').lower() == 'description':
                self.meta_description = True
        if tag == 'img':
            if 'alt' not in attrs or attrs.get('alt', '').strip() == '':
                self.img_no_alt.append(attrs.get('src', ''))
            if attrs.get('src'):
                self.hrefs.append(attrs['src'])
        if tag == 'script' and attrs.get('src'):
            self.scripts.append(attrs['src'])
            self.hrefs.append(attrs['src'])
        if tag == 'link' and attrs.get('rel') and 'stylesheet' in attrs.get('rel') and attrs.get('href'):
            self.styles.append(attrs['href'])
        if tag == 'a' and attrs.get('href'):
            self.hrefs.append(attrs['href'])
        if attrs.get('id'):
            self.ids.append(attrs.get('id'))

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_text += data

    def finalize(self):
        self.duplicate_ids = [id_ for id_, count in collections.Counter(self.ids).items() if count > 1]

report = {}
missing_links = []
missing_refs = []
nav_sets = {}
footer_pages = []
footer_missing = []
for html_file in sorted(root.rglob('*.html')):
    text = html_file.read_text(encoding='utf-8', errors='replace')
    parser = AuditParser(html_file)
    parser.feed(text)
    parser.close()
    parser.finalize()
    issues = []
    if parser.title_count == 0:
        issues.append('Missing <title>')
    if not parser.meta_charset:
        issues.append('Missing charset meta')
    if not parser.meta_viewport:
        issues.append('Missing viewport meta')
    if not parser.meta_description:
        issues.append('Missing description meta')
    if parser.img_no_alt:
        issues.append(f'{len(parser.img_no_alt)} <img> tags missing alt or empty alt')
    if parser.duplicate_ids:
        issues.append(f'Duplicate IDs: {parser.duplicate_ids}')
    if '<body' not in text.lower():
        issues.append('Missing <body>')
    if '</body>' not in text.lower():
        issues.append('Missing </body>')
    if '<html' not in text.lower():
        issues.append('Missing <html>')
    if '</html>' not in text.lower():
        issues.append('Missing </html>')
    for href in parser.hrefs:
        if href.startswith(('#', 'mailto:', 'tel:', 'javascript:')) or href.startswith(('http://', 'https://')):
            continue
        hrefclean = href.split('?')[0].split('#')[0]
        if hrefclean == '':
            continue
        p = (html_file.parent / hrefclean).resolve()
        if not p.exists():
            issues.append(f'Missing referenced file: {href}')
            missing_refs.append((str(html_file.relative_to(root)), href))
    if not any('style.css' in s or 'media-queries.css' in s for s in parser.styles):
        if 'link rel="stylesheet" href="style.css"' not in text and 'link rel="stylesheet" href="/style.css"' not in text:
            issues.append('Missing style.css include')
    if not any('script.js' in s for s in parser.scripts):
        if 'src="script.js"' not in text:
            issues.append('Missing script.js include')
    if issues:
        report[str(html_file.relative_to(root))] = issues
    # collect nav/footer content for consistency checks
    nav_start = text.lower().find('<nav class="nav-menu"')
    if nav_start != -1:
        nav_end = text.lower().find('</nav>', nav_start)
        nav_html = text[nav_start:nav_end] if nav_end != -1 else text[nav_start:]
        nav_links = []
        for href in parser.hrefs:
            if href.startswith('#') or href.startswith('http://') or href.startswith('https://'):
                continue
            if 'nav-menu' in nav_html and href in nav_html:
                nav_links.append(href)
        nav_sets.setdefault(tuple(nav_links), []).append(str(html_file.relative_to(root)))
    else:
        nav_sets.setdefault((), []).append(str(html_file.relative_to(root)))
    if '<footer' in text.lower():
        footer_pages.append(str(html_file.relative_to(root)))
    else:
        footer_missing.append(str(html_file.relative_to(root)))

print('HTML files total:', len(list(root.rglob('*.html'))))
print('Files with issues:', len(report))
for f, issues in report.items():
    print('---', f)
    for issue in issues:
        print(issue)
print('\nMissing references total:', len(missing_refs))
for f, h in missing_refs[:200]:
    print(f, '->', h)
print('\nNavigation variants:', len(nav_sets))
for nav_links, pages in nav_sets.items():
    print('--- variant', len(nav_links), 'links; pages:', len(pages))
    print(nav_links)
print('\nPages without <footer>:', len(footer_missing))
for p in footer_missing:
    print(p)
