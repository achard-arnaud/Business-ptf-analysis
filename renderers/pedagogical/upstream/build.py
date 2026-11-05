#!/usr/bin/env python3
"""Strategic note renderer — Markdown (+ light directives) → HTML → PDF (A4 portrait).

Pipeline
  1. front matter  → cover band (kicker, title, subtitle, meta)
  2. ```mermaid``` → PNG via mermaid-cli (scale 3), 30 % transposition gate
  3. ::: directives → styled blocks (tldr, kpis, callout, callout gold, story, cols)
  4. Markdown       → HTML (tables, footnotes = sources, md_in_html)
  5. Chromium (Playwright) → PDF with running footer + page numbers
  6. QA report      → page count vs page_range, figure scale factors, min font sizes

Usage
  python build.py note.md --out out_dir [--pages 5-7] [--no-fonts]

Directives (one per line, closed by a line ':::')
  ::: tldr [Label]          numbered executive messages (use an ordered list inside)
  ::: kpis                   lines '- VALUE | label'
  ::: callout [Label]        dark key-message box      (::: callout-gold [Label] for gold variant)
  ::: story [Label]          narrative / retex box
  ::: cols                   two columns, split with a line '+++'
  \\newpage                   hard page break
A mermaid block may start with '%% caption: Figure title', '%% maxh: 95' (max height in mm)
and '%% width: 900' (render viewport in px — use it for gantt/timeline, which stretch to the viewport).
"""
from __future__ import annotations

import argparse, hashlib, html, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent
CONTENT_W_MM = 210 - 2 * 17          # printable width
PX_PER_MM = 96 / 25.4
MIN_SCALE = 0.70                      # style-contract 30 % gate
CHROME = os.environ.get("CHROME_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
MMDC = shutil.which("mmdc") or "mmdc"

MERMAID_CFG = {
    "theme": "base",
    "themeVariables": {
        "fontFamily": "Inter, Carlito, Arial, sans-serif", "fontSize": "15px",
        "primaryColor": "#EAF1FA", "primaryBorderColor": "#1F4E8C", "primaryTextColor": "#13213A",
        "lineColor": "#5B6B82", "secondaryColor": "#E3F4F6", "tertiaryColor": "#FFF6E3",
        "clusterBkg": "#F3F6FA", "clusterBorder": "#CBD6E4", "edgeLabelBackground": "#FFFFFF",
    },
    "flowchart": {"htmlLabels": True, "curve": "basis", "nodeSpacing": 22, "rankSpacing": 26, "padding": 8},
    "gantt": {"fontSize": 13, "barHeight": 22, "barGap": 5, "topPadding": 40, "leftPadding": 150, "sectionFontSize": 13},
}

# --------------------------------------------------------------------------- front matter

def split_front_matter(text: str):
    meta = {}
    if text.startswith("---\n"):
        _, block, body = text.split("---", 2)
        for line in block.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
        return meta, body.lstrip("\n")
    return meta, text


def cover_html(meta: dict) -> str:
    items = [(k, meta.get(k)) for k in ("author", "date", "horizon", "audience") if meta.get(k)]
    labels = {"author": "Auteur", "date": "Date", "horizon": "Horizon", "audience": "Public"}
    meta_html = "".join(f"<span>{labels[k]} <b>{html.escape(v)}</b></span>" for k, v in items)
    return (
        '<header class="cover">'
        f'<div class="kicker">{html.escape(meta.get("kicker", "Note stratégique"))}</div>'
        f'<h1>{html.escape(meta.get("title", ""))}</h1>'
        f'<div class="subtitle">{html.escape(meta.get("subtitle", ""))}</div>'
        f'<div class="meta">{meta_html}</div></header>'
    )

# --------------------------------------------------------------------------- mermaid

def _direction(src: str):
    m = re.search(r"^\s*(flowchart|graph)\s+(LR|RL|TB|TD|BT)\b", src, re.M)
    return m.group(2) if m else None


def _transpose(src: str) -> str:
    swap = {"LR": "TB", "RL": "BT", "TB": "LR", "TD": "LR", "BT": "RL"}
    return re.sub(r"^(\s*(?:flowchart|graph)\s+)(LR|RL|TB|TD|BT)\b",
                  lambda m: m.group(1) + swap[m.group(2)], src, count=1, flags=re.M)


def _render_png(src: str, out_png: Path, workdir: Path, width: int = 1400):
    mmd = workdir / (out_png.stem + ".mmd")
    mmd.write_text(src)
    cfg = workdir / "mermaid.json"; cfg.write_text(json.dumps(MERMAID_CFG))
    pp = workdir / "puppeteer.json"; pp.write_text(json.dumps({"executablePath": CHROME, "args": ["--no-sandbox"]}))
    subprocess.run([MMDC, "-i", str(mmd), "-o", str(out_png), "-c", str(cfg), "-p", str(pp),
                    "-s", "3", "-b", "white", "-w", str(width)], check=True, capture_output=True)
    from PIL import Image
    w, h = Image.open(out_png).size
    return w / 3, h / 3  # CSS px at 1x


def render_mermaid(src: str, idx: int, assets: Path, workdir: Path, qa: list) -> str:
    caption = re.search(r"^%%\s*caption:\s*(.+)$", src, re.M)
    maxh = re.search(r"^%%\s*maxh:\s*(\d+)$", src, re.M)
    vw = re.search(r"^%%\s*width:\s*(\d+)$", src, re.M)
    vw = int(vw.group(1)) if vw else 1400
    caption = caption.group(1).strip() if caption else ""
    max_h_px = (int(maxh.group(1)) if maxh else 110) * PX_PER_MM
    max_w_px = CONTENT_W_MM * PX_PER_MM

    def fit(w, h):
        return min(1.0, max_w_px / w, max_h_px / h)

    tag = hashlib.md5(src.encode()).hexdigest()[:8]
    png = assets / f"fig{idx:02d}_{tag}.png"
    w, h = _render_png(src, png, workdir, vw)
    scale, used_src, transposed = fit(w, h), src, False
    if scale < MIN_SCALE and _direction(src):
        alt_src = _transpose(src)
        alt_png = assets / f"fig{idx:02d}_{tag}_t.png"
        aw, ah = _render_png(alt_src, alt_png, workdir, vw)
        if fit(aw, ah) > scale:
            png, w, h, scale, used_src, transposed = alt_png, aw, ah, fit(aw, ah), alt_src, True
    (assets / (png.stem + ".mmd")).write_text(used_src)          # canonical source kept next to image
    qa.append({"figure": idx, "caption": caption, "native_px": [round(w), round(h)],
               "scale": round(scale, 3), "transposed": transposed,
               "gate_ok": scale >= MIN_SCALE})
    disp_w = w * scale
    cap = f'<figcaption><b>Figure {idx}</b>{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure><img src="{png.name}" style="width:{disp_w:.0f}px" alt="{html.escape(caption)}">{cap}</figure>'

# --------------------------------------------------------------------------- directives

def md(text: str) -> str:
    return markdown.markdown(text, extensions=["tables", "sane_lists", "attr_list", "md_in_html"])


def render_directive(kind: str, label: str, body: str) -> str:
    """Return HTML shells with markdown="1" so the main converter (footnotes included) fills them."""
    if kind == "kpis":
        cells = []
        for line in body.strip().splitlines():
            line = line.strip().lstrip("-").strip()
            if "|" in line:
                v, l = [s.strip() for s in line.split("|", 1)]
                cells.append(f'<div class="kpi" markdown="1"><div class="v">{html.escape(v)}</div>'
                             f'<div class="l" markdown="span">{l}</div></div>')
        return f'<div class="kpis" markdown="1">{"".join(cells)}</div>'
    if kind == "cols":
        parts = re.split(r"^\+\+\+\s*$", body, flags=re.M)
        return '<div class="cols" markdown="1">' + "".join(f'<div markdown="1">\n\n{p.strip()}\n\n</div>' for p in parts) + "</div>"
    css = {"tldr": "tldr", "callout": "callout", "callout-gold": "callout gold", "story": "story"}[kind]
    default = {"tldr": "En bref", "callout": "Message clé", "callout-gold": "Point d'attention", "story": "Retour d'expérience"}[kind]
    return (f'<div class="{css}" markdown="1">\n<span class="label">{html.escape(label or default)}</span>\n\n'
            f'{body.strip()}\n\n</div>')


def preprocess(body: str, assets: Path, workdir: Path, qa: list) -> str:
    fig = [0]

    def mer(m):
        fig[0] += 1
        return "\n" + render_mermaid(m.group(1), fig[0], assets, workdir, qa) + "\n"
    body = re.sub(r"```mermaid\n(.*?)```", mer, body, flags=re.S)

    stash = {}

    def dire(m):
        return "\n" + render_directive(m.group(1), (m.group(2) or "").strip(), m.group(3)) + "\n"
    body = re.sub(r"^:::\s*(tldr|kpis|callout-gold|callout|story|cols)[ \t]*([^\n]*)\n(.*?)^:::[ \t]*$", dire, body, flags=re.S | re.M)
    body = body.replace("\\newpage", '<div class="pagebreak"></div>')
    return body, stash


def reorder_footnotes(body: str) -> str:
    """Number sources in order of first citation (python-markdown numbers by definition order)."""
    defs = dict(re.findall(r"^\[\^([^\]]+)\]:(.*)$", body, flags=re.M))
    text = re.sub(r"^\[\^[^\]]+\]:.*$\n?", "", body, flags=re.M)
    order = []
    for k in re.findall(r"\[\^([^\]]+)\]", text):
        if k in defs and k not in order:
            order.append(k)
    order += [k for k in defs if k not in order]
    return text.rstrip() + "\n\n" + "\n".join(f"[^{k}]:{defs[k]}" for k in order) + "\n"


def to_html(md_path: Path, out_dir: Path, fonts: bool, qa: dict) -> Path:
    meta, body = split_front_matter(md_path.read_text())
    body = reorder_footnotes(body)
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in list(out_dir.glob("fig*.png")) + list(out_dir.glob("fig*.mmd")):
        old.unlink()                                    # no stale figures from previous runs
    work = Path(tempfile.mkdtemp(prefix="snote_"))
    body, stash = preprocess(body, out_dir, work, qa.setdefault("figures", []))
    conv = markdown.Markdown(extensions=["tables", "sane_lists", "attr_list", "md_in_html", "footnotes"],
                             extension_configs={"footnotes": {"BACKLINK_TEXT": ""}})
    html_body = conv.convert(body)
    for k, v in stash.items():
        html_body = html_body.replace(f"<p>{k}</p>", v).replace(k, v)
    # adjacent source calls: 12,15 instead of 1215
    html_body = re.sub(r"</sup>\s*<sup", "</sup><sup>,</sup><sup", html_body)
    # numbered section headings "## 1 — Titre" → styled number
    html_body = re.sub(r"<h2([^>]*)>(\d+)\s*[—-]\s*", r'<h2\1><span class="num">\2</span>', html_body)
    # sources block title
    src_title = meta.get("sources_title", "Sources")
    src_intro = meta.get("sources_intro", "")
    html_body = html_body.replace('<div class="footnote">',
        f'<div class="sources-title">{html.escape(src_title)}</div>'
        + (f'<div class="sources-intro">{html.escape(src_intro)}</div>' if src_intro else "")
        + '<div class="footnote">', 1)
    font_link = ('<link rel="preconnect" href="https://fonts.gstatic.com">'
                 '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700'
                 '&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">') if fonts else ""
    shutil.copy(HERE / "theme.css", out_dir / "theme.css")
    page = (f'<!doctype html><html lang="{meta.get("lang","fr")}"><head><meta charset="utf-8">'
            f'<title>{html.escape(meta.get("title",""))}</title>{font_link}'
            f'<link rel="stylesheet" href="theme.css"></head><body>{cover_html(meta)}{html_body}</body></html>')
    out = out_dir / (md_path.stem + ".html")
    out.write_text(page)
    qa["meta"] = meta
    return out


def to_pdf(html_path: Path, pdf_path: Path, meta: dict):
    from playwright.sync_api import sync_playwright
    footer = ('<div style="width:100%;font-family:Arial,sans-serif;font-size:7.5pt;color:#5B6B82;'
              'padding:0 17mm;display:flex;justify-content:space-between">'
              f'<span>{html.escape(meta.get("footer",""))}</span>'
              '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(html_path.resolve().as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.pdf(path=str(pdf_path), format="A4", print_background=True, prefer_css_page_size=True,
               display_header_footer=True, header_template="<span></span>", footer_template=footer)
        b.close()


def qa_pdf(pdf: Path, page_range, qa: dict):
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    qa["pages"] = pages
    qa["page_range"] = page_range
    qa["page_gate_ok"] = page_range[0] <= pages <= page_range[1]
    qa["figure_gate_ok"] = all(f["gate_ok"] for f in qa.get("figures", []))
    css = re.sub(r"/\*.*?\*/", "", (HERE / "theme.css").read_text(), flags=re.S)
    skip = ("sup",)  # superscript source calls are exempt
    secondary = ("figcaption", ".footnote", ".sources-intro", ".kpi .l", ".cover", ".label", "th", ".table-note", ".signoff")
    body, sec = [], []
    for sel, block in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        if sel.strip().startswith(skip):
            continue
        for s in re.findall(r"font-size:(\d+(?:\.\d+)?)pt", block):
            (sec if any(k in sel for k in secondary) else body).append(float(s))
    qa["min_body_font_pt"] = min(body)
    qa["min_secondary_font_pt"] = min(sec)
    qa["font_gate_ok"] = min(body) >= 9 and min(sec) >= 8
    return qa


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source"); ap.add_argument("--out", default="build")
    ap.add_argument("--pages", default="5-7"); ap.add_argument("--no-fonts", action="store_true")
    a = ap.parse_args()
    lo, hi = map(int, a.pages.split("-"))
    src, out = Path(a.source), Path(a.out)
    qa: dict = {}
    h = to_html(src, out, not a.no_fonts, qa)
    pdf = out / (src.stem + ".pdf")
    to_pdf(h, pdf, qa["meta"])
    qa_pdf(pdf, (lo, hi), qa)
    qa.pop("meta", None)
    (out / "qa_report.json").write_text(json.dumps(qa, indent=2, ensure_ascii=False))
    print(json.dumps({k: qa[k] for k in ("pages", "page_gate_ok", "figure_gate_ok", "font_gate_ok", "min_body_font_pt", "min_secondary_font_pt")}, ensure_ascii=False))
    for f in qa.get("figures", []):
        print(f)
    sys.exit(0 if qa["page_gate_ok"] and qa["figure_gate_ok"] and qa["font_gate_ok"] else 2)


if __name__ == "__main__":
    main()
