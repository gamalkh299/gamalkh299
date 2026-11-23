"""Generate assets/experience.svg and assets/projects.svg. Edit the data below, then run: python3 scripts/cards.py"""
import textwrap
from pathlib import Path
from xml.dom import minidom
from xml.sax.saxutils import escape

EXPERIENCE = [
    ("2025 – Now", "Full-Stack Developer", "Adaa Consulting · Crown Prince's Office, Fujairah",
     ["Leading Tarasol gov platform", "UAE Pass SSO", "AI Arabic transcription", "Microservices"], True),
    ("2025", "Backend Developer", "Websters.ae",
     ["Twill CMS", "Lighthouse & SEO", "ASP.NET APIs"], False),
    ("2024 – 2025", "Backend Developer", "LOT.SA · Remote",
     ["IT ticketing system", "Server & Cloudflare security"], False),
    ("2023", "Backend Team Lead", "Beseech Co.",
     ["Led 5 developers", "+30% transaction speed"], True),
    ("2021 – 2024", "Backend Developer", "Spider Tech Co.",
     ["Fintech · E-commerce · Healthcare", "−30% query time", "HIPAA"], False),
    ("2020", "Backend Developer", "4th Pyramids Co. · Freelance",
     ["E-commerce backends", "Payment gateways"], False),
]

PROJECTS = [
    ("Tarasol", "GOVERNMENT · UAE",
     "Arabic-first correspondence & meetings platform with AI transcription and live document co-editing.",
     ["Django", "Next.js", "UAE Pass", "OnlyOffice"]),
    ("Real-Estate Investment Platform", "FINTECH · SAUDI ARABIA",
     "Led the backend team; integrated Absher, Riyadh Bank B2B (MT940) and Zoho Books.",
     ["Laravel", "Banking APIs", "Team Lead"]),
    ("Standing Committee on Int'l Law", "GOVERNMENT · SAUDI ARABIA",
     "Official website of the Saudi Standing Committee on International Law; led backend development.",
     ["Laravel", "Team Lead"]),
    ("Eyadda", "HEALTHCARE",
     "Connects doctors, patients, hospitals and labs around centralized health records.",
     ["Laravel", "HIPAA", "Full-Stack"]),
    ("Premium Ticket", "EVENTS",
     "Event-ticketing platform with seamless purchases; led backend and third-party integrations.",
     ["Payments", "Team Lead"]),
    ("ZI DESK", "SAAS",
     "IT ticketing system with real-time updates and client communication over Twilio.",
     ["Laravel", "Twilio", "Real-time"]),
]

W = 854
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
BG, CARD, BORDER, TEXT, MUTED, ACCENT = "#0d1117", "#161b22", "#30363d", "#e6edf3", "#8b949e", "#36BCF7"


def esc(s):
    return escape(s, {"'": "&#39;"})


def chip(x, y, label, strong=False):
    w = int(len(label) * 6.6) + 20  # shortcut: width estimated from char count; fine for these short labels
    fill, stroke, color = ("#0c2d48", ACCENT, ACCENT) if strong else (BG, BORDER, MUTED)
    return (w, f'<rect x="{x}" y="{y}" width="{w}" height="22" rx="11" fill="{fill}" stroke="{stroke}"/>'
               f'<text x="{x + w / 2}" y="{y + 15}" text-anchor="middle" font-size="12" fill="{color}">{esc(label)}</text>')


def chips(x, y, labels, strong=False):
    out = []
    for label in labels:
        w, svg = chip(x, y, label, strong)
        out.append(svg)
        x += w + 8
    return "".join(out)


def svg(h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" font-family="{FONT}">'
            f'<rect width="{W}" height="{h}" rx="12" fill="{BG}"/>{body}</svg>')


def experience():
    row, top = 92, 24
    h = top * 2 + row * len(EXPERIENCE) - 16
    body = [f'<line x1="36" y1="{top + 14}" x2="36" y2="{h - top - 40}" stroke="{BORDER}" stroke-width="2"/>']
    for i, (period, role, company, tags, highlight) in enumerate(EXPERIENCE):
        y = top + i * row
        dot = ACCENT if i == 0 else (MUTED if not highlight else ACCENT)
        body.append(f'<circle cx="36" cy="{y + 14}" r="7" fill="{BG}" stroke="{dot}" stroke-width="3"/>')
        if i == 0:
            body.append(f'<circle cx="36" cy="{y + 14}" r="3" fill="{ACCENT}"/>')
        body.append(f'<rect x="60" y="{y - 6}" width="{W - 84}" height="{row - 14}" rx="10" fill="{CARD}" stroke="{ACCENT if i == 0 else BORDER}"/>')
        body.append(f'<text x="78" y="{y + 19}" font-size="16" font-weight="700" fill="{TEXT}">{esc(role)}'
                    f'<tspan font-weight="400" fill="{MUTED}" font-size="14">  ·  {esc(company)}</tspan></text>')
        body.append(f'<text x="{W - 42}" y="{y + 19}" text-anchor="end" font-size="13" font-weight="600" fill="{ACCENT}">{esc(period)}</text>')
        body.append(chips(78, y + 34, tags, strong=i == 0))
    return svg(h, "".join(body))


def projects():
    cols, gap, pad, ch = 2, 16, 20, 158
    cw = (W - pad * 2 - gap) // cols
    rows = (len(PROJECTS) + 1) // cols
    h = pad * 2 + rows * ch + (rows - 1) * gap
    body = []
    for i, (name, tag, desc, tech) in enumerate(PROJECTS):
        x = pad + (i % cols) * (cw + gap)
        y = pad + (i // cols) * (ch + gap)
        body.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="10" fill="{CARD}" stroke="{BORDER}"/>')
        body.append(f'<rect x="{x}" y="{y + 18}" width="3" height="40" rx="1.5" fill="{ACCENT}"/>')
        body.append(f'<text x="{x + 18}" y="{y + 32}" font-size="11" font-weight="700" letter-spacing="1" fill="{ACCENT}">{esc(tag)}</text>')
        body.append(f'<text x="{x + 18}" y="{y + 54}" font-size="16" font-weight="700" fill="{TEXT}">{esc(name)}</text>')
        for j, line in enumerate(textwrap.wrap(desc, 54)[:2]):
            body.append(f'<text x="{x + 18}" y="{y + 80 + j * 18}" font-size="13" fill="{MUTED}">{esc(line)}</text>')
        body.append(chips(x + 18, y + ch - 36, tech))
    return svg(h, "".join(body))


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets"
    for name, content in (("experience.svg", experience()), ("projects.svg", projects())):
        minidom.parseString(content)  # self-check: fails loudly on invalid XML (the bug that broke the banner)
        (out / name).write_text(content, encoding="utf-8")
        print("wrote", out / name)
