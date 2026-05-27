from pathlib import Path
import urllib.parse

MAP_QUERY = "Plot No 92 Ramreddy Nagar IDA Jeedimetla HYD-500055"
map_url = "https://www.google.com/maps?q=" + urllib.parse.quote_plus(MAP_QUERY) + "&output=embed"
MAP_IFRAME = '<iframe src="' + map_url + '" width="100%" height="250" style="border:0;" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'

p = Path('index.html')
text = p.read_text(encoding='utf-8')
if 'google.com/maps' in text:
    print('Map already present')
else:
    idx = text.find('info@mediqhealthcare.com')
    if idx == -1:
        print('Email not found; abort')
    else:
        close_p = text.find('</p>', idx)
        if close_p == -1:
            print('Email closing </p> not found; abort')
        else:
            insert_pos = close_p + len('</p>')
            new_text = text[:insert_pos] + '\n' + MAP_IFRAME + '\n' + text[insert_pos:]
            p.write_text(new_text, encoding='utf-8')
            print('Inserted map iframe into index.html')
