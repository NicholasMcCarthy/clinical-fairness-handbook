"""Check book packaging, local references, and stated teaching arithmetic."""
from collections import Counter
from decimal import Decimal, ROUND_CEILING
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set()
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag in ('a', 'link') and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag in ('img', 'script') and 'src' in attrs:
            self.links.append(attrs['src'])


config = (ROOT / '_quarto.yml').read_text(encoding='utf-8')
registered = re.findall(r'^\s*-\s+([^\s]+\.qmd)\s*$', config, re.M)
sources = [ROOT / 'index.qmd', ROOT / 'references.qmd']
sources += sorted((ROOT / 'chapters').glob('*.qmd'))
sources += sorted((ROOT / 'appendices').glob('*.qmd'))
check(set(registered) == {p.relative_to(ROOT).as_posix() for p in sources},
      'Quarto chapter registration differs from source files.')
check(len(registered) == len(set(registered)), 'Duplicate chapter registration.')
texts = {}
for path in sources:
    check(path.exists(), f'Missing source: {path}')
    if path.exists():
        texts[path] = path.read_text(encoding='utf-8')
combined = '\n'.join(texts.values())
bib = (ROOT / 'references.bib').read_text(encoding='utf-8')
bib_keys = re.findall(r'^@\w+\{([^,]+),', bib, re.M)
check(len(bib_keys) == len(set(bib_keys)), 'Duplicate bibliography keys.')
ids = re.findall(r'\{[^}\n]*#([\w:-]+)[^}\n]*\}', combined)
for identifier, count in Counter(ids).items():
    check(count == 1, f'Duplicate source identifier: {identifier}')
references = set(re.findall(r'(?<![\w])@([A-Za-z][\w:-]*)', combined))
for reference in references:
    targets = ids if reference.startswith(('sec-', 'eq-', 'fig-', 'tbl-')) else bib_keys
    check(reference in targets, f'Unresolved source reference: {reference}')
illustrations = {i for i in ids if i.startswith('ill-')}
brief = (ROOT / 'appendices/illustration-briefs.qmd').read_text(encoding='utf-8')
brief_ids = set(re.findall(r'`(ill-[\w-]+)`', brief))
check(illustrations == brief_ids, 'Illustration placeholders and briefs differ.')

# Check the numbers printed in the two principal confusion tables.
for path, expected_rows in [
    (ROOT / 'chapters/02-clinical-applications.qmd', 2),
    (ROOT / 'chapters/06-fairness.qmd', 2),
]:
    rows = []
    for line in texts[path].splitlines():
        if not line.startswith('| '):
            continue
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        if len(cells) == 8 and cells[1].isdigit() and all(c.isdigit() for c in cells[2:6]):
            rows.append(cells)
    check(len(rows) == expected_rows, f'Could not inspect teaching table: {path.name}')
    for cells in rows:
        cases, tp, fn, fp, tn = map(int, cells[1:6])
        check(tp + fn == cases and tp + fn + fp + tn == 1000,
              f'Inconsistent confusion counts: {cells[0]}')
        check(abs(tp / (tp + fn) - 0.9) < 1e-12
              and abs(tn / (tn + fp) - 0.9) < 1e-12,
              f'Incorrect stated sensitivity/specificity: {cells[0]}')
        if 'clinical-applications' in path.name:
            ppv, npv = cells[6:8]
            check(ppv == f'{100 * tp / (tp + fp):.1f}%', f'Incorrect PPV: {cells[0]}')
            check(npv == f'{100 * tn / (tn + fn):.1f}%', f'Incorrect NPV: {cells[0]}')

# The fairness table has eight columns; verify it independently.
fairness_rows = []
for line in texts[ROOT / 'chapters/06-fairness.qmd'].splitlines():
    cells = [c.strip() for c in line.strip('|').split('|')]
    if len(cells) == 8 and cells[0] in ('A', 'B'):
        fairness_rows.append(cells)
        cases, tp, fn, fp, tn = map(int, cells[1:6])
        check(tp + fn == cases and tp + fn + fp + tn == 1000, 'Fairness count mismatch.')
        check(cells[6] == f'{100 * (tp + fp) / 1000:.0f}%', 'Fairness selection mismatch.')
        check(cells[7] == f'{100 * tp / (tp + fp):.1f}%', 'Fairness PPV mismatch.')
check(len(fairness_rows) == 2, 'Could not inspect fairness table.')
for n, expected in [(19, 18), (4, 5)]:
    k = int((Decimal(n + 1) * Decimal('0.9')).to_integral_value(rounding=ROUND_CEILING))
    check(k == expected, 'Conformal order-statistic arithmetic mismatch.')

book = ROOT / '_book'
html_files = sorted(book.rglob('*.html'))
check(len(html_files) >= len(sources), 'Render HTML before running the complete check.')
pages = {p.resolve(): Page(p.read_text(encoding='utf-8')) for p in html_files}
for path, page in pages.items():
    raw = path.read_text(encoding='utf-8')
    check('quarto-unresolved-ref' not in raw, f'Unresolved rendered reference: {path.name}')
    for link in page.links:
        parts = urlsplit(link)
        if parts.scheme or parts.netloc or link.startswith('//'):
            continue
        target = (book / unquote(parts.path.lstrip('/')) if parts.path.startswith('/')
                  else path.parent / unquote(parts.path)) if parts.path else path
        target = target.resolve()
        if target.is_dir():
            target /= 'index.html'
        check(target.exists(), f'Broken local link in {path.name}: {link}')
        fragment = unquote(parts.fragment)
        if fragment and target in pages:
            check(fragment in pages[target].ids, f'Broken anchor in {path.name}: {link}')

epubs = list(book.glob('*.epub'))
check(len(epubs) == 1, 'Expected one rendered EPUB.')
if len(epubs) == 1:
    with zipfile.ZipFile(epubs[0]) as archive:
        check(archive.testzip() is None, 'Corrupt EPUB member.')
        check(archive.read('mimetype') == b'application/epub+zip', 'Invalid EPUB mimetype.')
        ET.fromstring(archive.read('META-INF/container.xml'))
        for name in archive.namelist():
            if name.endswith(('.xhtml', '.opf', '.ncx')):
                try:
                    ET.fromstring(archive.read(name))
                except ET.ParseError as exc:
                    errors.append(f'Invalid EPUB XML in {name}: {exc}')

if errors:
    print('\n'.join(f'ERROR: {error}' for error in errors))
    sys.exit(1)
print(f'PASS: {len(sources)} sources, {len(bib_keys)} references, '
      f'{len(illustrations)} illustration briefs, {len(html_files)} HTML pages, '
      'EPUB package, local links, and teaching arithmetic.')
