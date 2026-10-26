"""Post-build SEO pass for the GitHub Pages artifact (run from the repo root in CI).

Adds the head tags mdBook and the hand-written pages lack (canonical,
description, Open Graph, twitter:card) and writes sitemap.xml. A tag already
present is left alone, so hand-written values win.
"""
import html
import pathlib
import re

SITE = "https://ferra.rs/"
SKIP_DIRS = {".git", ".github", "graft", "theme"}
OG_IMAGE = "og-v1.png"  # 1200x630; og:image is only emitted once this file exists
# mdBook writes the first chapter twice; both point at the URL the nav links to.
CANONICAL_OVERRIDE = {"docs/introduction.html": "docs/"}


def url_for(rel):
    rel = CANONICAL_OVERRIDE.get(rel, rel)
    return SITE + (rel[: -len("index.html")] if rel.endswith("index.html") else rel)


def text(fragment):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", fragment)).split())


def first_paragraph(page):
    main = re.search(r"(?s)<main\b.*?</main>", page)
    p = re.search(r"(?s)<p\b[^>]*>(.*?)</p>", main.group(0) if main else page)
    if not p:
        return ""
    desc = text(p.group(1))
    return desc if len(desc) <= 160 else desc[:157].rsplit(" ", 1)[0] + "…"


def process(path, root, og_image):
    rel = path.relative_to(root).as_posix()
    page = path.read_text(encoding="utf-8")
    if re.search(r"<meta[^>]+noindex", page) or path.name == "404.html":
        return None
    url = url_for(rel)
    title = text(re.search(r"(?s)<title>(.*?)</title>", page).group(1))
    m = re.search(r'<meta name="description" content="([^"]*)"', page)
    desc = html.unescape(m.group(1)) if m and m.group(1) else first_paragraph(page)
    tags = {
        'rel="canonical"': f'<link rel="canonical" href="{url}">',
        'name="description"': f'<meta name="description" content="{html.escape(desc)}">',
        'property="og:title"': f'<meta property="og:title" content="{html.escape(title)}">',
        'property="og:description"': f'<meta property="og:description" content="{html.escape(desc)}">',
        'property="og:url"': f'<meta property="og:url" content="{url}">',
        'property="og:type"': '<meta property="og:type" content="website">',
        'property="og:site_name"': '<meta property="og:site_name" content="Ferra.rs">',
        'name="twitter:card"': '<meta name="twitter:card" content="'
        + ("summary_large_image" if og_image else "summary") + '">',
    }
    if og_image:
        tags['property="og:image"'] = f'<meta property="og:image" content="{SITE}{OG_IMAGE}">'
    # An empty description from mdBook counts as absent.
    page = re.sub(r'\s*<meta name="description" content="">', "", page)
    new = "\n".join(t for key, t in tags.items() if key not in page)
    if new:
        page = page.replace("</head>", new + "\n</head>", 1)
        path.write_text(page, encoding="utf-8")
    return url


def main(root=pathlib.Path(".")):
    og_image = (root / OG_IMAGE).exists()
    urls = set()
    for path in sorted(root.rglob("*.html")):
        if SKIP_DIRS.isdisjoint(path.relative_to(root).parts[:-1]):
            url = process(path, root, og_image)
            if url:
                urls.add(url)
    body = "".join(f"  <url><loc>{u}</loc></url>\n" for u in sorted(urls))
    (root / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + body + "</urlset>\n",
        encoding="utf-8",
    )
    print(f"seo_postbuild: {len(urls)} URLs in sitemap.xml")


if __name__ == "__main__":
    main()
