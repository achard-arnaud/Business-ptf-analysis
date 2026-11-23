"""Correlate actual 3-page PDF, screenshots, browser report and render manifest.

Mechanical QA is not reader QA, business evidence or committee permission.
"""
import argparse
import hashlib
import json
import re
import struct
import unicodedata
import zlib
from html.parser import HTMLParser
from pathlib import Path
from pypdf import PdfReader

ISSUE_KEYS=("overlaps","overflows","out_of_bounds","small_fonts","low_padding")
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def check_page_png(path):
    raw = path.read_bytes()
    if len(raw) < 33 or raw[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path.name}: invalid page PNG signature or header")
    if struct.unpack_from(">I", raw, 8)[0] != 13 or raw[12:16] != b"IHDR":
        raise ValueError(f"{path.name}: invalid PNG image header")
    width, height = struct.unpack_from(">II", raw, 16)
    if width < 800 or height < 500:
        raise ValueError(f"{path.name}: page PNG dimensions too small")

    offset = 8
    view = memoryview(raw)
    has_image_data = False
    while offset < len(raw):
        if len(raw) - offset < 12:
            raise ValueError(f"{path.name}: truncated PNG chunk")
        size, kind = struct.unpack_from(">I4s", raw, offset)
        end = offset + 12 + size  # Length, type, data and CRC field.
        if end > len(raw):
            raise ValueError(f"{path.name}: truncated PNG chunk")
        expected_crc = struct.unpack_from(">I", raw, end - 4)[0]
        if zlib.crc32(view[offset + 4:end - 4]) != expected_crc:
            label = kind.decode("ascii", errors="replace")
            raise ValueError(f"{path.name}: invalid PNG {label} chunk CRC")
        if kind == b"IDAT" and size:
            has_image_data = True
        elif kind == b"IEND":
            if size or end != len(raw) or not has_image_data:
                raise ValueError(f"{path.name}: invalid PNG termination or missing image data")
            return
        offset = end
    raise ValueError(f"{path.name}: missing PNG termination (IEND)")

class ExecPageText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.pages = 0
        self.sections = []
        self.divs = []
        self.slots = {}

    def current_page(self):
        return next((page for page in reversed(self.sections) if page is not None), None)

    def handle_starttag(self, tag, attrs):
        classes = (dict(attrs).get("class") or "").split()
        if tag == "section":
            is_page = "page" in classes
            if is_page:
                self.pages += 1
            self.sections.append(self.pages if is_page else None)
        elif tag == "div":
            body = None
            page = self.current_page()
            slot = None
            if "source-line" in classes:
                slot = "source_line"
            elif ("footer-body" in classes
                  and any("footer-strip" in ancestor for ancestor, _ in self.divs)):
                slot = "footer"
            if page is not None and slot is not None:
                body = []
                self.slots.setdefault((page, slot), []).append(body)
            self.divs.append((classes, body))

    def handle_endtag(self, tag):
        if tag == "section" and self.sections:
            self.sections.pop()
        elif tag == "div" and self.divs:
            self.divs.pop()

    def handle_data(self, data):
        if self.current_page() is not None:
            for _, body in reversed(self.divs):
                if body is not None:
                    body.append(data)
                    break


def plain_text(value):
    return " ".join(unicodedata.normalize("NFKC", value).split())


def expected_exec_text(payload, number, slot):
    label = slot.replace("_", " ")
    try:
        page = payload[f"page{number}"]
        body = page["footer"]["body"] if slot == "footer" else page["sources"]
        body = re.sub(r"\{([a-z0-9_]+)\}",
                      lambda match: payload["figures"][match[1]]["value"], body)
        text = plain_text(re.sub(r"\*\*(.+?)\*\*", r"\1", body))
    except (KeyError, TypeError) as err:
        raise ValueError(f"exec payload is missing the page {number} {label} or its figure") from err
    if not text:
        raise ValueError(f"exec payload has a blank page {number} {label}")
    return text


def verify_exec_page_text(payload_path, manifest, pdf, pages, *, all_pages, source_lines):
    raw = Path(payload_path).read_bytes()
    if manifest.get("payload_sha256") != hashlib.sha256(raw).hexdigest():
        raise ValueError("exec payload does not match render manifest")
    payload = json.loads(raw)
    html = pdf.with_suffix(".html")
    if not html.is_file():
        raise ValueError("exec HTML evidence missing")
    witness = ExecPageText()
    witness.feed(html.read_text(encoding="utf-8"))
    witness.close()
    if witness.pages != 3:
        raise ValueError("exec HTML evidence must contain exactly three pages")
    result = {}
    for number in (1, 2, 3) if all_pages or source_lines else (2,):
        slots = ["footer"] if all_pages or number == 2 else []
        if source_lines:
            slots.append("source_line")
        page = pages[number - 1]
        pdf_text = plain_text(page.extract_text())
        layout_text = None
        for slot in slots:
            label = slot.replace("_", " ")
            expected = expected_exec_text(payload, number, slot)
            html_text = [plain_text("".join(body)) for body in witness.slots.get((number, slot), [])]
            if html_text != [expected]:
                raise ValueError(f"exec HTML page {number} {label} differs from payload")
            if expected not in pdf_text:
                # Positioned glyphs can lose spaces; try layout on this same page only.
                if layout_text is None and (all_pages or slot == "source_line"):
                    layout_text = plain_text(page.extract_text(extraction_mode="layout"))
                if not (all_pages or slot == "source_line") or expected not in layout_text:
                    raise ValueError(f"exec PDF page {number} {label} differs from payload")
            result[f"exec_{slot}_page{number}"] = "PASS"
    return result


def verify(folder, *, profile, exec_payload=None, all_exec_footers=False, exec_source_lines=False):
    if all_exec_footers and exec_payload is None:
        raise ValueError("all exec footers comparison needs an exec payload")
    if exec_source_lines and exec_payload is None:
        raise ValueError("exec source line comparison needs an exec payload")
    if exec_payload is not None and profile != "exec":
        raise ValueError("exec payload comparison needs the exec profile")
    folder=Path(folder)
    manifest=json.loads((folder/"render_manifest.json").read_text(encoding="utf-8"))
    report_path=folder/"qa.json"
    report=json.loads(report_path.read_text(encoding="utf-8"))
    if report.get("page_count")!=3 or report.get("pass") is not True:
        raise ValueError("browser report does not pass exactly three pages")
    summary=report.get("summary",{})
    if any(summary.get(key,1)!=0 for key in ISSUE_KEYS):
        raise ValueError("browser report contains layout defects or missing category")
    if manifest.get("qa_sha256") != sha(report_path):
        raise ValueError("QA report changed since manifest")
    pdfs=list(folder.glob("*.pdf"))
    if len(pdfs)!=1:
        raise ValueError("expected exactly one PDF")
    pdf=pdfs[0]
    pages = PdfReader(str(pdf)).pages
    if len(pages)!=3:
        raise ValueError("PDF physical page count != 3")
    if manifest.get("pdf_sha256")!=sha(pdf):
        raise ValueError("PDF changed since manifest")
    pngs=[folder / f"{pdf.stem}_page{page}.png" for page in range(1, 4)]
    captures = {path for path in folder.glob("*_page*.png")
                if re.fullmatch(r".*_page[0-9]+\.png", path.name)}
    if captures != set(pngs):
        raise ValueError("expected exactly three screenshots for pages 1–3 of the same PDF")
    for png in pngs:
        check_page_png(png)
    observed=[sha(p) for p in pngs]
    if manifest.get("png_sha256")!=observed:
        raise ValueError("PNG changed since render manifest")
    if profile=="value-chain-preview":
        receipt=json.loads((folder/"artifact_receipt.json").read_text(encoding="utf-8"))
        if receipt.get("sha256")!=sha(pdf) or receipt.get("publication_state")!="prepared_not_published":
            raise ValueError("preview receipt does not match exact PDF or falsely claims publication")
        if receipt.get("authorization_state")!="UNREVIEWED" or receipt.get("qa_state")!="PASS":
            raise ValueError("preview receipt must be mechanically QAed and not human approved")
    elif profile=="exec":
        if manifest.get("render_profile")!="exec" or manifest.get("visual_qa")!="LAYOUT_PASS_MANUAL_PENDING":
            raise ValueError("exec not in manual-review-pending layout-pass state")
    else:
        raise ValueError("unknown rendering profile")
    result = {"status":"AUTOMATED_LAYOUT_PASS_READER_PENDING","profile":profile,
              "physical_pages":3,"pngs":3,"pdf_sha256":sha(pdf),"committee_authorized":False}
    if exec_payload is not None:
        result.update(verify_exec_page_text(exec_payload, manifest, pdf, pages,
                                           all_pages=all_exec_footers, source_lines=exec_source_lines))
    return result


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("folder",type=Path)
    p.add_argument("--profile",choices=("exec","value-chain-preview"),required=True)
    p.add_argument("--exec-payload", type=Path, help="Optional exec page 2 footer check against the exact rendered payload")
    p.add_argument("--all-exec-footers", action="store_true",
                   help="With --exec-payload, check all three exec footer bodies")
    p.add_argument("--exec-source-lines", action="store_true",
                   help="With --exec-payload, also check the exec source line on each page")
    a=p.parse_args()
    if a.all_exec_footers and a.exec_payload is None:
        p.error("--all-exec-footers requires --exec-payload")
    if a.exec_source_lines and a.exec_payload is None:
        p.error("--exec-source-lines requires --exec-payload")
    print(json.dumps(verify(a.folder, profile=a.profile, exec_payload=a.exec_payload,
                            all_exec_footers=a.all_exec_footers,
                            exec_source_lines=a.exec_source_lines), ensure_ascii=False))
