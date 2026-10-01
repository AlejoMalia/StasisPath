#!/usr/bin/env python3
"""Render the StasisPath manuscripts to PDF from their Markdown sources.

Single source of truth: PAPER_STASISPATH_EN.md and PAPER_STASISPATH_ES.md. The previous
generator carried 154 KB of hardcoded content, so regenerating it reproduced a stale paper.
This one reads the Markdown, so the PDF cannot drift from the manuscript.

    python3 build_papers_pdf.py
"""
from __future__ import annotations
import re, sys, pathlib
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether, Preformatted)

ROOT = pathlib.Path(__file__).resolve().parent
INK = colors.HexColor("#1a1a1a")
MUTED = colors.HexColor("#5c5c5c")
RULE = colors.HexColor("#d4d4d4")
BAND = colors.HexColor("#f2f2f2")
ACCENT = colors.HexColor("#14532d")

S = getSampleStyleSheet()
def st(name, **kw):
    base = dict(fontName="Times-Roman", fontSize=9.6, leading=13.2, textColor=INK)
    base.update(kw)
    return ParagraphStyle(name, parent=S["BodyText"], **base)

STY = {
    "title":   st("t",  fontName="Times-Bold", fontSize=19, leading=23, alignment=TA_CENTER, spaceAfter=7),
    "authors": st("a",  fontName="Times-Bold", fontSize=11, leading=14, alignment=TA_CENTER, spaceAfter=2),
    "meta":    st("m",  fontSize=8.8, leading=12, alignment=TA_CENTER, textColor=MUTED, spaceAfter=12),
    "h1":      st("h1", fontName="Times-Bold", fontSize=13.5, leading=17, textColor=ACCENT,
                  spaceBefore=14, spaceAfter=5),
    "h2":      st("h2", fontName="Times-Bold", fontSize=11.2, leading=14, spaceBefore=10, spaceAfter=4),
    "h3":      st("h3", fontName="Times-Italic", fontSize=10.2, leading=13, spaceBefore=8, spaceAfter=3),
    "body":    st("b",  alignment=TA_JUSTIFY, spaceAfter=5),
    "quote":   st("q",  fontSize=9.2, leading=12.6, alignment=TA_JUSTIFY, leftIndent=9,
                  textColor=colors.HexColor("#333333"), spaceBefore=3, spaceAfter=6),
    "li":      st("li", alignment=TA_JUSTIFY, leftIndent=11, bulletIndent=2, spaceAfter=2.5),
    "cell":    st("c",  fontSize=7.9, leading=10.4),
    "cellh":   st("ch", fontName="Times-Bold", fontSize=7.9, leading=10.4),
    "refs":    st("r",  fontSize=8.6, leading=11.4, alignment=TA_JUSTIFY, leftIndent=9,
                  firstLineIndent=-9, spaceAfter=2.5),
}
MONO = ParagraphStyle("mono", fontName="Courier", fontSize=6.9, leading=8.4, textColor=colors.HexColor("#222222"))

# --------------------------------------------------------------- inline markdown -> reportlab
def inline(s: str) -> str:
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\$\$(.+?)\$\$", r"\1", s, flags=re.S)          # display math -> plain
    s = re.sub(r"\$(.+?)\$", r"\1", s)                           # inline math -> plain
    s = re.sub(r"\\(?:boxed|text|mathrm|textbf)\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\(?:le|leq)\b", "≤", s); s = re.sub(r"\\(?:ge|geq)\b", "≥", s)
    s = re.sub(r"\\times\b", "×", s);      s = re.sub(r"\\approx\b", "≈", s)
    s = re.sub(r"\\circ\b", "°", s);       s = re.sub(r"\\cdot\b", "·", s)
    s = re.sub(r"\\(?:tau|sigma|rho|kappa|Delta|alpha|beta|nu)\b",
               lambda m: {"tau":"τ","sigma":"σ","rho":"ρ","kappa":"κ","Delta":"Δ",
                          "alpha":"α","beta":"β","nu":"ν"}[m.group(0)[1:]], s)
    s = re.sub(r"[\\{}]", "", s)
    s = re.sub(r"_\{?([A-Za-z0-9,+\-]+)\}?", r"<sub>\1</sub>", s)
    s = re.sub(r"\^\{?([A-Za-z0-9,+\-]+)\}?", r"<super>\1</super>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<i>\1</i>", s)
    s = re.sub(r"`([^`]+)`", r'<font face="Courier" size="8.4">\1</font>', s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", s)
    return s

def table_flow(rows, width):
    head, body = rows[0], rows[1:]
    data = [[Paragraph(inline(c), STY["cellh"]) for c in head]]
    data += [[Paragraph(inline(c), STY["cell"]) for c in r] for r in body]
    n = max(len(r) for r in data)
    data = [r + [Paragraph("", STY["cell"])] * (n - len(r)) for r in data]
    t = Table(data, colWidths=[width / n] * n, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BAND),
        ("LINEABOVE", (0, 0), (-1, 0), 0.7, INK),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, INK),
        ("LINEBELOW", (0, -1), (-1, -1), 0.7, INK),
        ("INNERGRID", (0, 1), (-1, -1), 0.25, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3.5), ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
    ]))
    return t

def parse(md: str, width: float):
    lines = md.split("\n")
    flow, i, n = [], 0, len(lines)
    in_refs = False
    while i < n:
        L = lines[i]
        if L.strip() in ("---", "***", "___"):
            flow.append(Spacer(1, 4)); i += 1; continue
        if L.startswith("```"):
            i += 1; buf = []
            while i < n and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            flow.append(Spacer(1, 2))
            flow.append(Preformatted("\n".join(buf), MONO))
            flow.append(Spacer(1, 5)); continue
        if L.startswith("|") and i + 1 < n and re.match(r"^\|[\s:\-|]+\|?\s*$", lines[i + 1]):
            rows = []
            while i < n and lines[i].startswith("|"):
                if not re.match(r"^\|[\s:\-|]+\|?\s*$", lines[i]):
                    rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            flow.append(Spacer(1, 3)); flow.append(table_flow(rows, width)); flow.append(Spacer(1, 7))
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", L)
        if m:
            lvl, txt = len(m.group(1)), m.group(2)
            in_refs = bool(re.match(r"^\d*\.?\s*(References|Referencias)", txt))
            if lvl == 1 and not flow:
                flow.append(Paragraph(inline(txt), STY["title"]))
            else:
                flow.append(Paragraph(inline(txt), STY["h1" if lvl <= 2 else "h2" if lvl == 3 else "h3"]))
            i += 1; continue
        if L.startswith(">"):
            buf = []
            while i < n and lines[i].startswith(">"):
                buf.append(re.sub(r"^>\s?\[!\w+\]\s*", "", lines[i][1:]).strip()); i += 1
            txt = " ".join(x for x in buf if x)
            if txt:
                p = Paragraph(inline(txt), STY["quote"])
                t = Table([[p]], colWidths=[width], hAlign="LEFT")
                t.setStyle(TableStyle([("LINEBEFORE", (0, 0), (0, -1), 1.6, ACCENT),
                                       ("LEFTPADDING", (0, 0), (-1, -1), 7),
                                       ("TOPPADDING", (0, 0), (-1, -1), 3),
                                       ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
                flow.append(t); flow.append(Spacer(1, 5))
            continue
        m = re.match(r"^(\s*)([-*•]|\d+\.)\s+(.*)", L)
        if m:
            body = m.group(3)
            j = i + 1
            while j < n and lines[j].strip() and not re.match(r"^(\s*)([-*•]|\d+\.)\s+|^[#>|]|^```", lines[j]):
                body += " " + lines[j].strip(); j += 1
            num = re.match(r"^\d+\.$", m.group(2))
            if in_refs and num:
                flow.append(Paragraph(f"{m.group(2)} {inline(body)}", STY["refs"]))
            else:
                mark = m.group(2) if num else "•"
                flow.append(Paragraph(f"{mark} {inline(body)}", STY["li"]))
            i = j; continue
        if not L.strip():
            i += 1; continue
        body = L
        j = i + 1
        while j < n and lines[j].strip() and not re.match(r"^[#>|\-*]|^```|^\d+\.\s", lines[j]):
            body += " " + lines[j].strip(); j += 1
        if len(flow) <= 3 and body.startswith("**") and body.rstrip().endswith("**"):
            flow.append(Paragraph(inline(body), STY["authors"]))
        elif len(flow) <= 4 and body.startswith("*") and not body.startswith("**"):
            flow.append(Paragraph(inline(body), STY["meta"]))
        else:
            flow.append(Paragraph(inline(body), STY["body"]))
        i = j
    return flow

def build(md_path: pathlib.Path, pdf_path: pathlib.Path, footer: str):
    pw, ph = A4
    ml = mr = 19 * mm; mt = 17 * mm; mb = 17 * mm
    width = pw - ml - mr

    def page(canv, doc):
        canv.saveState()
        canv.setFont("Times-Roman", 7.4); canv.setFillColor(MUTED)
        canv.drawString(ml, mb - 8 * mm, footer)
        canv.drawRightString(pw - mr, mb - 8 * mm, str(doc.page))
        canv.setStrokeColor(RULE); canv.setLineWidth(0.4)
        canv.line(ml, mb - 5.6 * mm, pw - mr, mb - 5.6 * mm)
        canv.restoreState()

    doc = BaseDocTemplate(str(pdf_path), pagesize=A4, leftMargin=ml, rightMargin=mr,
                          topMargin=mt, bottomMargin=mb,
                          title=md_path.stem.replace("_", " "), author="Alejo Malia; Claude (Anthropic); Grok (xAI)")
    doc.addPageTemplates([PageTemplate(id="p",
        frames=[Frame(ml, mb, width, ph - mt - mb, id="f")], onPage=page)])
    doc.build(parse(md_path.read_text(), width))
    return pdf_path.stat().st_size

if __name__ == "__main__":
    for stem, foot in (("PAPER_STASISPATH_EN", "StasisPath · Alejo Malia, Claude, Grok · StasisPath Initiative"),
                       ("PAPER_STASISPATH_ES", "StasisPath · Alejo Malia, Claude, Grok · StasisPath Initiative")):
        md = ROOT / f"{stem}.md"
        if not md.exists():
            print(f"missing {md}", file=sys.stderr); continue
        size = build(md, ROOT / f"{stem}.pdf", foot)
        print(f"{stem}.pdf  {size/1024:,.0f} KB  <- {md.name} ({len(md.read_text().split()):,} words)")
