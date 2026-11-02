"""PDF helper for the solve-assignment skill (needs PyMuPDF, installed in the repo venv).

Usage:
  pdf_tool.py toc     <book.pdf>                        print the bookmark tree with page numbers
  pdf_tool.py find    <book.pdf> <text>                 list pages containing the text (case-insensitive)
  pdf_tool.py text    <book.pdf> <first> <last>         print the text of pages first..last (1-based)
  pdf_tool.py extract <book.pdf> <first> <last> <out>   save pages first..last (1-based, inclusive) as a new PDF
  pdf_tool.py info    <file.pdf>                        page count and whether pages have a text layer
"""
import sys

import pymupdf


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd, path, rest = argv[0], argv[1], argv[2:]
    doc = pymupdf.open(path)
    if cmd == "toc":
        toc = doc.get_toc()
        if not toc:
            print("no bookmarks; use 'find' with the chapter title instead")
        for level, title, page in toc:
            print(f"{'  ' * (level - 1)}{title}  ->  p.{page}")
    elif cmd == "find":
        needle = " ".join(rest).lower()
        for i, page in enumerate(doc, start=1):
            if needle in page.get_text().lower():
                print(f"p.{i}")
    elif cmd == "text":
        first, last = int(rest[0]), int(rest[1])
        for i in range(first, last + 1):
            print(f"\n===== page {i} =====\n{doc[i - 1].get_text()}")
    elif cmd == "extract":
        first, last, out = int(rest[0]), int(rest[1]), rest[2]
        new = pymupdf.open()
        new.insert_pdf(doc, from_page=first - 1, to_page=last - 1)
        new.save(out)
        print(f"wrote {out} (pages {first}-{last} of {path})")
    elif cmd == "info":
        with_text = sum(1 for p in doc if p.get_text().strip())
        print(f"{doc.page_count} pages, {with_text} with a text layer"
              + ("" if with_text else " (scanned/handwritten: read the pages visually)"))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
