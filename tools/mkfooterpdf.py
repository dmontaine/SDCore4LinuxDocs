#!/usr/bin/env python3
"""
mkfooterpdf.py - print one mkdoc.py page to a PDF whose footer reads, left to
right, the NAME OF THE SECTION the page is in, the PAGE NUMBER and the DATE.

    python3 tools/mkfooterpdf.py <page.html> <out.pdf> [--date "24 October 2026"]

24 Oct 2026, owner's request for the changes document.  The footer that
mkbookpdf.py draws is one fixed text for the whole book, because Chrome's
printToPDF footerTemplate is a single template for every page and cannot know
which heading a page is under.  This script gets a running section name by
printing the document in pieces:

  1. one full print, only to learn which page each heading falls on (the text of
     each page is read with pdftotext and the headings are looked for in the
     order they appear in the HTML, so a word that is also a table cell cannot
     match out of turn);
  2. one print of each run of pages that share a section, with pageRanges, whose
     footer template carries that section's name and Chrome's own page number
     (which stays the page number of the whole document when pageRanges is
     used - checked, the script refuses the result if the last footer disagrees
     with the page count);
  3. pdfunite, which joins the pieces.

WHAT IS LOST.  pdfunite does not carry the bookmark tree that
generateDocumentOutline makes, so this PDF has no outline.  mkbookpdf.py's
books keep theirs.

The section is the page's last <h2>; under the h2 "New Features Unique to SD
Core" it is that h2 and the last <h3>.
"""

import argparse
import base64
import datetime
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mkbookpdf  # noqa: E402  (find_browser, wait_for_debug_port, CDP)

UNIQUE = 'New Features Unique to SD Core'


def headings(page_html):
    """[(level, text)] of every h2 and h3 of the page, in order."""
    out = []
    for m in re.finditer(r'<h([23])[^>]*>(.*?)</h\1>', page_html, re.S):
        t = html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip()
        t = re.sub(r'\s*[#¶]$', '', t).strip()
        out.append((int(m.group(1)), t))
    return out


def page_texts(pdf):
    n = int(re.search(r'Pages:\s+(\d+)',
                      subprocess.check_output(['pdfinfo', pdf]).decode()).group(1))
    pages = []
    for p in range(1, n + 1):
        txt = subprocess.check_output(
            ['pdftotext', '-f', str(p), '-l', str(p), '-layout', pdf, '-']).decode()
        pages.append([ln.strip() for ln in txt.split('\n')])
    return pages


def labels_for(pages, heads, title):
    """One label for each page: the last section heading on the page, or the one
    in force when the page began if it has none.  Taking the LAST heading means
    every section is named on at least the page it starts on."""
    labels = []
    h2 = title
    h3 = ''
    nxt = 0
    for lines in pages:
        # the stylesheet prints an h3 in capitals, so compare in capitals
        up = [ln.upper() for ln in lines]
        while nxt < len(heads) and heads[nxt][1].upper() in up:
            lvl, text = heads[nxt]
            if lvl == 2:
                h2, h3 = text, ''
            else:
                h3 = text
            nxt += 1
        labels.append(h2 + (' · ' + h3 if h2 == UNIQUE and h3 else ''))
    return labels


def footer_template(label, date):
    e = lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    cell = 'flex:1;'
    return ('<div style="width:100%;font-size:9px;color:#555;padding:0 8mm;'
            'display:flex;font-family:Arial,sans-serif;">'
            '<span style="' + cell + 'text-align:left;">' + e(label) + '</span>'
            '<span style="' + cell + 'text-align:center;"><span class="pageNumber"></span></span>'
            '<span style="' + cell + 'text-align:right;">' + e(date) + '</span>'
            '</div>')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('html')
    ap.add_argument('pdf')
    ap.add_argument('--date', default=datetime.date.today().strftime('%-d %B %Y'))
    ap.add_argument('--timeout', type=int, default=180)
    args = ap.parse_args()

    html_path = os.path.abspath(args.html)
    pdf_path = os.path.abspath(args.pdf)
    page_html = open(html_path, encoding='utf-8').read()
    heads = headings(page_html)
    m = re.search(r'<title>(.*?)</title>', page_html, re.S)
    title = html.unescape(m.group(1)).split(' - ')[0].strip() if m else 'Changes'
    if not heads:
        sys.stderr.write('mkfooterpdf: no h2 or h3 in %s\n' % html_path)
        return 1
    browser = mkbookpdf.find_browser()
    if not browser:
        sys.stderr.write('mkfooterpdf: no Chrome or Chromium found\n')
        return 1
    for tool in ('pdfinfo', 'pdftotext', 'pdfunite'):
        if not shutil.which(tool):
            sys.stderr.write('mkfooterpdf: %s (poppler-utils) is not installed\n' % tool)
            return 1

    work = tempfile.mkdtemp(prefix='mkfooterpdf-')
    profile = os.path.join(work, 'profile')
    port = 9500 + (os.getpid() % 300)
    proc = subprocess.Popen(
        [browser, '--headless=new', '--disable-gpu', '--no-first-run',
         '--no-default-browser-check', '--user-data-dir=' + profile,
         '--remote-debugging-port=%d' % port, 'about:blank'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    cdp = None
    tab_id = None
    try:
        mkbookpdf.wait_for_debug_port(port)
        req = urllib.request.Request(
            'http://127.0.0.1:%d/json/new?%s' % (port, 'file://' + urllib.parse.quote(html_path)),
            method='PUT')
        with urllib.request.urlopen(req, timeout=10) as r:
            tab = json.loads(r.read().decode())
        tab_id = tab['id']
        cdp = mkbookpdf.CDP(tab['webSocketDebuggerUrl'])
        cdp.call('Page.enable')
        cdp.wait_for_event('Page.loadEventFired', timeout=args.timeout)

        base = {'printBackground': True, 'marginTop': 0.4, 'marginBottom': 0.5,
                'marginLeft': 0.4, 'marginRight': 0.4, 'preferCSSPageSize': False}

        def printed(path, **extra):
            opts = dict(base)
            opts.update(extra)
            res = cdp.call('Page.printToPDF', opts, timeout=args.timeout)
            with open(path, 'wb') as f:
                f.write(base64.b64decode(res['data']))

        full = os.path.join(work, 'full.pdf')
        printed(full, displayHeaderFooter=False)
        pages = page_texts(full)
        labels = labels_for(pages, heads, title)
        sys.stdout.write('mkfooterpdf: %d pages, %d headings found in order\n'
                         % (len(pages), len(heads)))

        runs = []
        for i, lab in enumerate(labels, 1):
            if runs and runs[-1][2] == lab:
                runs[-1][1] = i
            else:
                runs.append([i, i, lab])
        pieces = []
        for k, (a, b, lab) in enumerate(runs):
            piece = os.path.join(work, 'p%03d.pdf' % k)
            printed(piece, displayHeaderFooter=True, headerTemplate='<span></span>',
                    footerTemplate=footer_template(lab, args.date),
                    pageRanges='%d-%d' % (a, b))
            pieces.append(piece)
            sys.stdout.write('  pages %3d-%-3d  %s\n' % (a, b, lab))
        subprocess.check_call(['pdfunite'] + pieces + [pdf_path])
    finally:
        if cdp:
            cdp.close()
        if tab_id:
            try:
                urllib.request.urlopen('http://127.0.0.1:%d/json/close/%s' % (port, tab_id), timeout=5)
            except OSError:
                pass
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        keep = os.environ.get('MKFOOTERPDF_KEEP')
        if not keep:
            shutil.rmtree(work, ignore_errors=True)

    n_out = int(re.search(r'Pages:\s+(\d+)', subprocess.check_output(['pdfinfo', pdf_path]).decode()).group(1))
    if n_out != len(pages):
        sys.stderr.write('mkfooterpdf: %d pages out, %d in the full print\n' % (n_out, len(pages)))
        return 1
    sys.stdout.write('mkfooterpdf: wrote %s (%d pages)\n' % (pdf_path, n_out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
