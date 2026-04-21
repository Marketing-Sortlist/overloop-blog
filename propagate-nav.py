#!/usr/bin/env python3
"""Propagate the new nav.html to all HTML files, replacing the old inlined nav."""
import os, re

# Read the new nav
with open('assets/nav.html') as f:
    new_nav = f.read().strip()

# Process all HTML files
updated = 0
for root, dirs, files in os.walk('blog/'):
    for f in files:
        if not f.endswith('.html'):
            continue
        filepath = os.path.join(root, f)
        with open(filepath) as fh:
            content = fh.read()

        # Find and replace the nav block: from <!-- Overloop Navigation --> to </nav>
        pattern = r'<!-- Overloop Navigation -->.*?</nav>\s*(?:</script>)?'
        if re.search(pattern, content, re.DOTALL):
            new_content = re.sub(pattern, new_nav, content, count=1, flags=re.DOTALL)
            if new_content != content:
                with open(filepath, 'w') as fh:
                    fh.write(new_content)
                updated += 1

# Also do versus/
for f in os.listdir('versus/'):
    if not f.endswith('.html'):
        continue
    filepath = os.path.join('versus/', f)
    with open(filepath) as fh:
        content = fh.read()
    pattern = r'<!-- Overloop Navigation -->.*?</nav>\s*(?:</script>)?'
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, new_nav, content, count=1, flags=re.DOTALL)
        if new_content != content:
            with open(filepath, 'w') as fh:
                fh.write(new_content)
            updated += 1

print("Updated nav on {} files".format(updated))
