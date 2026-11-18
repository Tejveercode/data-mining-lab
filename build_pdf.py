#!/usr/bin/env python3
"""Build printable PDFs from the Markdown notes in this pack.

Pure reportlab, no system libraries.  From this folder:

    pip install reportlab
    python3 build_pdf.py

Writes five PDFs into pdf/.
"""
import os
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, HRFlowable, PageBreak, PageTemplate, Paragraph,
    Preformatted, Spacer, Table, TableStyle,
)

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "pdf")
ACCENT = colors.HexColor("#14453d")
RULE = colors.HexColor("#b7ccc7")
GREY = colors.HexColor("#444444")
WIDTH = A4[0] - 34 * mm


def st(name, **kw):
    base = dict(fontName="Helvetica", fontSize=9.6, leading=13.4, spaceAfter=5,
                alignment=TA_JUSTIFY)
    base.update(kw)
    return ParagraphStyle(name, **base)


S = {
    "title": st("t", fontName="Helvetica-Bold", fontSize=26, leading=31,
                textColor=ACCENT, alignment=TA_CENTER, spaceAfter=10),
    "sub": st("s", fontSize=12.5, leading=18, alignment=TA_CENTER, textColor=GREY),
    "h1": st("h1", fontName="Helvetica-Bold", fontSize=17, leading=21,
             textColor=colors.white, backColor=ACCENT, borderPadding=(6, 8, 6, 8),
             spaceBefore=6, spaceAfter=10, alignment=0),
    "h2": st("h2", fontName="Helvetica-Bold", fontSize=12.6, leading=16,
             textColor=ACCENT, spaceBefore=11, spaceAfter=4, alignment=0),
    "h3": st("h3", fontName="Helvetica-BoldOblique", fontSize=10.8, leading=14,
             spaceBefore=8, spaceAfter=3, alignment=0),
    "body": st("b"),
    "bullet": st("bu", leftIndent=13, bulletIndent=2, spaceAfter=2.5),
    "quote": st("q", leftIndent=12, textColor=GREY, fontName="Helvetica-Oblique"),
    "cell": st("c", fontSize=8.1, leading=10.4, spaceAfter=0, alignment=0),
    "cellh": st("ch", fontSize=8.1, leading=10.4, spaceAfter=0, alignment=0,
                fontName="Helvetica-Bold", textColor=colors.white),
    "code": ParagraphStyle("code", fontName="Courier", fontSize=7.9, leading=10.2,
                           textColor=colors.HexColor("#14303f")),
}


def inline(text):
    """Small Markdown subset -> reportlab mini-HTML, protecting code spans."""
    t = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    codes = []

    def stash(m):
        codes.append(m.group(1))
        return "\x00%d\x00" % (len(codes) - 1)

    t = re.sub(r"`([^`]+)`", stash, t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<i>\1</i>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", t)
    return re.sub(r"\x00(\d+)\x00",
                  lambda m: '<font face="Courier" size="8.4" color="#0d4f63">%s</font>'
                            % codes[int(m.group(1))], t)


def boxed(flowable):
    t = Table([[flowable]], colWidths=[WIDTH])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f4f6f8")),
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def table(rows):
    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]
    data = [[Paragraph(inline(c), S["cellh"]) for c in rows[0]]]
    data += [[Paragraph(inline(c), S["cell"]) for c in r] for r in rows[1:]]
    weights = [max(6, min(max(len(re.sub(r"[*`\[\]]", "", r[i])) for r in rows), 46))
               for i in range(ncols)]
    total = sum(weights)
    t = Table(data, colWidths=[WIDTH * w / total for w in weights],
              repeatRows=1, hAlign="CENTER")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#faf9f8")]),
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def to_flowables(md, first=False):
    flow, lines, i, n = [], md.split("\n"), 0, len(md.split("\n"))
    while i < n:
        s = lines[i].strip()

        if s.startswith("```"):
            i += 1
            block = []
            while i < n and not lines[i].strip().startswith("```"):
                block.append(lines[i].rstrip())
                i += 1
            i += 1
            flow += [boxed(Preformatted("\n".join(block), S["code"])), Spacer(1, 6)]
            continue

        if s.startswith("|") and i + 1 < n and re.match(r"^\|[\s:\-|]+\|$", lines[i + 1].strip()):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                raw = lines[i].strip().strip("|")
                if not re.match(r"^[\s:\-|]+$", raw):
                    rows.append([c.strip() for c in raw.split("|")])
                i += 1
            flow += [Spacer(1, 3), table(rows), Spacer(1, 7)]
            continue

        if not s:
            i += 1
            continue

        if re.match(r"^-{3,}$", s):
            flow += [Spacer(1, 2), HRFlowable(width="100%", thickness=0.7, color=RULE),
                     Spacer(1, 5)]
            i += 1
            continue

        m = re.match(r"^(#{1,3})\s+(.*)$", s)
        if m:
            level = len(m.group(1))
            if level == 1 and not first:
                flow.append(PageBreak())
            flow.append(Paragraph(inline(m.group(2)), S["h%d" % level]))
            i += 1
            continue

        if s.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            flow.append(Paragraph(inline(" ".join(buf)), S["quote"]))
            continue

        m = re.match(r"^[-*]\s+(.*)$", s)
        if m:
            flow.append(Paragraph(inline(m.group(1)), S["bullet"], bulletText="\u2022"))
            i += 1
            continue

        m = re.match(r"^(\d+)\.\s+(.*)$", s)
        if m:
            flow.append(Paragraph(inline(m.group(2)), S["bullet"],
                                  bulletText="%s." % m.group(1)))
            i += 1
            continue

        buf = [s]
        i += 1
        while i < n:
            nxt = lines[i].strip()
            if (not nxt or nxt.startswith(("#", "|", ">", "```", "- ", "* "))
                    or re.match(r"^\d+\.\s", nxt) or re.match(r"^-{3,}$", nxt)):
                break
            buf.append(nxt)
            i += 1
        flow.append(Paragraph(inline(" ".join(buf)), S["body"]))
    return flow


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.6)
    canvas.setFillColor(GREY)
    if doc.page > 1:
        canvas.drawString(17 * mm, 11 * mm, doc.doc_title)
        canvas.drawRightString(A4[0] - 17 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(17 * mm, 14 * mm, A4[0] - 17 * mm, 14 * mm)
    canvas.restoreState()


def build(name, title, subtitle, files):
    path = os.path.join(OUT, name)

    class Doc(BaseDocTemplate):
        def __init__(self, fn, **kw):
            BaseDocTemplate.__init__(self, fn, pagesize=A4, leftMargin=17 * mm,
                                     rightMargin=17 * mm, topMargin=16 * mm,
                                     bottomMargin=18 * mm, **kw)
            self.addPageTemplates([PageTemplate(
                id="all", onPage=footer,
                frames=[Frame(self.leftMargin, self.bottomMargin, self.width,
                              self.height, id="normal")])])

    doc = Doc(path, title=title)
    doc.doc_title = title
    story = [Spacer(1, 55 * mm), Paragraph(title, S["title"]),
             HRFlowable(width="45%", thickness=1.6, color=ACCENT, hAlign="CENTER",
                        spaceBefore=4, spaceAfter=12),
             Paragraph(subtitle, S["sub"]), Spacer(1, 14),
             Paragraph("Data Mining Lab (24CAP-308) &middot; compiled November 2026",
                       st("m", alignment=TA_CENTER, fontSize=9.4, textColor=GREY)),
             PageBreak()]
    for idx, f in enumerate(files):
        with open(f, encoding="utf-8") as fh:
            story += to_flowables(fh.read(), first=(idx == 0))
    doc.build(story)
    return path, os.path.getsize(path)


def main():
    os.makedirs(OUT, exist_ok=True)
    N = lambda f: os.path.join(BASE, "notes", f)
    notes = sorted(f for f in os.listdir(os.path.join(BASE, "notes")) if f.endswith(".md"))
    experiments = [f for f in notes if f.split("-")[0].isdigit() and int(f.split("-")[0]) <= 6]
    jobs = [
        ("Lab-Manual-Experiments-1-6.pdf", "Data Mining Lab - Complete Manual",
         "Six experiments: aim, theory, algorithm, program, verified output, viva",
         [N(f) for f in experiments]),
        ("Lab-Projects-and-Written-Paper.pdf", "Lab Projects and the Written Paper",
         "Churn, market basket, XYZ Mart case, and every formula drill solved",
         [N("07-projects.md"), N("09-written-paper-drills.md")]),
        ("Lab-Viva-Handbook.pdf", "The Viva Handbook",
         "120 questions in the order they are asked, with answers",
         [N("08-viva-handbook.md")]),
        ("Lab-Question-Bank.pdf", "Lab Question Bank",
         "Written, viva and code-reading questions with model answer outlines",
         [os.path.join(BASE, "exam", "question-bank.md")]),
        ("Lab-Cheat-Sheet.pdf", "Lab Cheat Sheet",
         "Formulas, commands, Weka steps and the numbers to remember",
         [os.path.join(BASE, "exam", "cheat-sheet.md")]),
    ]
    for name, title, sub, files in jobs:
        p, size = build(name, title, sub, files)
        print("built %-40s (%d KB)" % (os.path.basename(p), size // 1024))


if __name__ == "__main__":
    main()
