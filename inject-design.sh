#!/bin/bash
# Inject Overloop design system (CSS + nav + footer) into all EN blog articles
set -e

NAV=$(cat assets/nav.html)
FOOTER=$(cat assets/footer.html)
CSS_LINK='<link rel="stylesheet" href="/assets/css/overloop.css">'

for f in blog/en/*.html; do
    echo "Processing: $f"

    # 1. Add CSS link after <head> opening (before first <style> or other link)
    if ! grep -q 'overloop.css' "$f"; then
        sed -i '' "s|<meta charset=\"UTF-8\">|<meta charset=\"UTF-8\">\n    $CSS_LINK|" "$f"
    fi

    # 2. Inject nav after <body> (before first div)
    if ! grep -q 'class="nav"' "$f"; then
        # Use python for multiline injection (sed is painful for this)
        python3 -c "
import sys
nav = open('assets/nav.html').read()
with open('$f', 'r') as fh:
    content = fh.read()
# Insert nav right after <body>
content = content.replace('<body>', '<body>\n' + nav, 1)
with open('$f', 'w') as fh:
    fh.write(content)
"
    fi

    # 3. Inject footer before </body>
    if ! grep -q 'class="footer"' "$f"; then
        python3 -c "
footer = open('assets/footer.html').read()
with open('$f', 'r') as fh:
    content = fh.read()
content = content.replace('</body>', footer + '\n</body>', 1)
with open('$f', 'w') as fh:
    fh.write(content)
"
    fi

    # 4. Wrap existing content in article-container if not already
    if ! grep -q 'class="article-container"' "$f"; then
        python3 -c "
with open('$f', 'r') as fh:
    content = fh.read()
# Find the container div and add the class
content = content.replace('<div class=\"container\">', '<div class=\"article-container\">', 1)
with open('$f', 'w') as fh:
    fh.write(content)
"
    fi
done

echo "Done! Processed $(ls blog/en/*.html | wc -l | tr -d ' ') files."
