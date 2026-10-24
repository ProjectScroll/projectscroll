"""Short addresses for printed QR codes: projectscroll.com/go/<name>/ forwards to the page.
Change a destination here and every flyer already printed follows it.  python3 _tools/build_go.py"""
import pathlib, html
R = pathlib.Path(__file__).resolve().parents[1]
GO = {
    'clue': '/treasure-hunt-quest/',
    'facebook': 'https://www.facebook.com/projectscroll/',
    'dewey': '/news/the-week-dewey-lake-went-wild/',
    'lore': '/lore/',
    'sponsor': '/sponsor-and-advertise/',
    'newsletter': '/newsletter/',
    'desk': '/#contact',
}
for k, to in GO.items():
    d = R / 'go' / k; d.mkdir(parents=True, exist_ok=True)
    e = html.escape(to)
    (d / 'index.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Project Scroll</title><meta name="robots" content="noindex"><link rel="canonical" href="{e if to.startswith('http') else 'https://projectscroll.com' + e}">
<meta http-equiv="refresh" content="0; url={e}"><script>location.replace({to!r})</script></head>
<body style="font:16px Georgia,serif;padding:2rem"><p><a href="{e}">Continue to Project Scroll</a></p></body></html>
''')
print('go built', len(GO))
