"""Generate the animated resume panel from config.json."""

from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "assets" / "resume.svg"

OUTER = "#0b1d20"
BG = "#071416"
PANEL = "#0a2928"
HAIR = "#168f82"
TEAL = "#43ead3"
MINT = "#83ffe8"
BLUE = "#4387ff"
PURPLE = "#9b6cff"
YELLOW = "#f2dc56"
ORANGE = "#ff6b48"
GREEN = "#56f73a"
TEXT = "#dcfff7"
MUTED = "#79aaa4"


def clean(value: object, limit: int = 90) -> str:
    text = " ".join(str(value or "").split())
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return escape(text)


def generate(config: dict) -> str:
    resume = config.get("resume", {})
    summary = list(resume.get("summary", []))[:5]
    education = resume.get("education", {})
    objective = list(resume.get("career_objective", []))[:3]
    github = str(config.get("website", "https://github.com/Kourosh-MD")).replace("https://", "").rstrip("/")
    linkedin = str(resume.get("linkedin", "")).replace("https://www.", "").replace("https://", "").rstrip("/")
    stack = list(resume.get("core_stack", []))[:5]
    additional = list(resume.get("additional_skills", []))[:11]
    languages = list(resume.get("languages", []))[:3]
    colors = [TEAL, BLUE, PURPLE, YELLOW, GREEN, ORANGE]

    summary_nodes = "".join(
        f'<text x="67" y="{190 + index * 25}" class="copy">{clean(line, 108)}</text>'
        for index, line in enumerate(summary)
    )
    stack_nodes = "".join(
        f'<g class="skill skill-{index}" transform="translate({66 + (index % 3) * 154} {632 + (index // 3) * 46})">'
        f'<rect width="138" height="34" rx="17" fill="#0d3636" stroke="#238f83"/>'
        f'<circle cx="18" cy="17" r="4" fill="{colors[index]}"/>'
        f'<text x="31" y="21" class="skill-text">{clean(skill, 16)}</text></g>'
        for index, skill in enumerate(stack)
    )
    objective_nodes = "".join(
        f'<text x="476" y="{410 + index * 29}" class="copy">{clean(line, 55)}</text>'
        for index, line in enumerate(objective)
    )
    additional_nodes = "".join(
        f'<g class="skill skill-{index}" transform="translate({66 + (index % 4) * 119} {807 + (index // 4) * 42})">'
        f'<rect width="108" height="30" rx="15" fill="#0d3636" stroke="#238f83"/>'
        f'<circle cx="16" cy="15" r="4" fill="{colors[index % len(colors)]}"/>'
        f'<text x="28" y="19" class="skill-text">{clean(skill, 13)}</text></g>'
        for index, skill in enumerate(additional)
    )
    language_nodes = "".join(
        f'<g class="language-row row-{index}" transform="translate(602 {810 + index * 61})">'
        f'<text x="0" y="0" class="language-name">{clean(item.get("name", ""), 18)}</text>'
        f'<text x="225" y="0" text-anchor="end" class="language-level">{clean(item.get("level", ""), 18)}</text>'
        f'<rect x="0" y="15" width="225" height="5" rx="3" fill="#1c4644"/>'
        f'<rect x="0" y="15" width="{225 if index == 0 else 184}" height="5" rx="3" fill="{MINT if index == 0 else BLUE}" class="language-bar"/></g>'
        for index, item in enumerate(languages)
    )

    css = """
.title{font:700 34px 'Trebuchet MS',sans-serif;fill:#dcfff7}
.headline{font:700 13px ui-monospace,Consolas,monospace;fill:#83ffe8;letter-spacing:1.4px}
.section{font:700 15px 'Trebuchet MS',sans-serif;fill:#dcfff7}
.label{font:700 9px 'Trebuchet MS',sans-serif;fill:#43ead3;letter-spacing:1.6px}
.copy{font:13px 'Trebuchet MS',sans-serif;fill:#79aaa4}
.education-main{font:700 15px 'Trebuchet MS',sans-serif;fill:#dcfff7}
.education-sub{font:12px 'Trebuchet MS',sans-serif;fill:#79aaa4}
.skill-text{font:700 11px 'Trebuchet MS',sans-serif;fill:#dcfff7}
.language-name{font:700 13px 'Trebuchet MS',sans-serif;fill:#dcfff7}
.language-level{font:700 10px ui-monospace,Consolas,monospace;fill:#83ffe8;letter-spacing:1px}
.mono{font:10px ui-monospace,Consolas,monospace;fill:#79aaa4}
.link{font:11px ui-monospace,Consolas,monospace;fill:#79aaa4}
.panel{opacity:0;animation:panelIn .75s cubic-bezier(.32,.72,0,1) forwards}
.panel-1{animation-delay:.1s}.panel-2{animation-delay:.2s}.panel-3{animation-delay:.3s}.panel-4{animation-delay:.4s}.panel-5{animation-delay:.5s}.panel-6{animation-delay:.6s}
.cursor{animation:blink 1s step-end infinite}.scan{animation:scan 5.5s linear infinite}
.skill{opacity:0;animation:chipIn .45s cubic-bezier(.32,.72,0,1) forwards}
.skill-0{animation-delay:.55s}.skill-1{animation-delay:.65s}.skill-2{animation-delay:.75s}
.skill-3{animation-delay:.85s}.skill-4{animation-delay:.95s}.skill-5{animation-delay:1.05s}.skill-6{animation-delay:1.15s}.skill-7{animation-delay:1.25s}.skill-8{animation-delay:1.35s}.skill-9{animation-delay:1.45s}.skill-10{animation-delay:1.55s}
.language-bar{transform-origin:left;animation:grow .9s .85s cubic-bezier(.32,.72,0,1) both}
.language-row{opacity:0;animation:fadeIn .6s forwards}.row-0{animation-delay:.7s}.row-1{animation-delay:.9s}
@keyframes panelIn{from{opacity:0;transform:translateY(13px)}to{opacity:1;transform:translateY(0)}}
@keyframes chipIn{from{opacity:0}to{opacity:1}}
@keyframes fadeIn{to{opacity:1}}@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes blink{0%,48%{opacity:1}49%,100%{opacity:0}}
@keyframes scan{from{transform:translateY(-40px)}to{transform:translateY(980px)}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.panel,.skill,.language-row{opacity:1!important}}
"""

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="960" viewBox="0 0 900 960" role="img" aria-label="Expanded animated resume for {clean(config.get('name', 'Kourosh Mansouri'))}">
<defs>
  <linearGradient id="resume-shell" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0b625b"/><stop offset=".54" stop-color="#0c393c"/><stop offset="1" stop-color="#2b4f88"/></linearGradient>
  <linearGradient id="scan-line" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{TEAL}" stop-opacity="0"/><stop offset=".5" stop-color="{MINT}" stop-opacity=".25"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></linearGradient>
  <clipPath id="resume-clip"><rect x="18" y="18" width="864" height="924" rx="18"/></clipPath>
  <style>{css}</style>
</defs>
<rect width="900" height="960" rx="24" fill="{OUTER}"/>
<rect x="6" y="6" width="888" height="948" rx="20" fill="url(#resume-shell)" stroke="{HAIR}"/>
<rect x="18" y="18" width="864" height="924" rx="18" fill="{BG}" stroke="#1a7269"/>
<circle cx="38" cy="37" r="5" fill="#ff665d"/><circle cx="56" cy="37" r="5" fill="#f5c451"/><circle cx="74" cy="37" r="5" fill="#46d468"/>
<text x="450" y="41" text-anchor="middle" class="mono">kourosh@resume: ~$ ./profile --junior-java</text><rect x="701" y="30" width="7" height="14" fill="{MINT}" class="cursor"/>
<text x="44" y="91" class="title">{clean(config.get('name', 'Kourosh Mansouri'))}</text>
<text x="46" y="115" class="headline">{clean(str(resume.get('headline', config.get('role', 'Developer'))).upper())} · {clean(str(config.get('location', 'Tehran, Iran')).upper())}</text>
<path d="M44 128H856" stroke="#1b5d58"/><circle cx="844" cy="91" r="14" fill="#0d3636" stroke="{TEAL}"/><path d="M838 91l4 4 8-9" fill="none" stroke="{MINT}" stroke-width="2"/>
<g class="panel panel-1"><rect x="44" y="147" width="812" height="190" rx="18" fill="{PANEL}" stroke="#1c8277"/><text x="66" y="176" class="section">About Me</text><text x="832" y="176" text-anchor="end" class="label">PROFILE.SUMMARY</text>{summary_nodes}</g>
<g class="panel panel-2"><rect x="44" y="355" width="390" height="210" rx="18" fill="{PANEL}" stroke="#1c8277"/><text x="66" y="388" class="section">Education</text><text x="408" y="388" text-anchor="end" class="label">ACTIVE</text><circle cx="73" cy="428" r="7" fill="{MINT}"/><path d="M73 435V522" stroke="#26786f" stroke-width="2"/><text x="96" y="432" class="education-main">{clean(education.get('program', 'Computer Engineering'), 43)}</text><text x="96" y="466" class="education-sub">{clean(education.get('institution', 'Islamic Azad University'), 46)}</text><text x="96" y="493" class="education-sub">{clean(education.get('location', config.get('location', '')), 46)}</text><text x="96" y="530" class="label">CURRENTLY STUDYING</text></g>
<g class="panel panel-3"><rect x="452" y="355" width="404" height="210" rx="18" fill="{PANEL}" stroke="#1c8277"/><text x="476" y="388" class="section">Career Objective</text><text x="832" y="388" text-anchor="end" class="label">TARGET.ROLE</text>{objective_nodes}<text x="476" y="493" class="label">PROFILE LINKS</text><text x="476" y="520" class="link">{clean(github, 51)}</text><text x="476" y="546" class="link">{clean(linkedin, 51)}</text></g>
<g class="panel panel-4"><rect x="44" y="583" width="812" height="145" rx="18" fill="{PANEL}" stroke="#1c8277"/><text x="66" y="616" class="section">Java Backend Toolkit</text><text x="832" y="616" text-anchor="end" class="label">PRIMARY FOCUS</text>{stack_nodes}</g>
<g class="panel panel-5"><rect x="44" y="746" width="510" height="181" rx="18" fill="{PANEL}" stroke="#1c8277"/><text x="66" y="779" class="section">Additional Skills &amp; Tools</text><text x="526" y="779" text-anchor="end" class="label">EXTENDED STACK</text>{additional_nodes}</g>
<g class="panel panel-6"><rect x="574" y="746" width="282" height="181" rx="18" fill="{PANEL}" stroke="#1c8277"/><text x="596" y="779" class="section">Languages</text><text x="832" y="779" text-anchor="end" class="label">COMMUNICATION</text>{language_nodes}</g>
<g clip-path="url(#resume-clip)" opacity=".55"><rect x="18" y="0" width="864" height="2" fill="url(#scan-line)" class="scan"/></g>
<text x="849" y="939" text-anchor="end" class="mono">{clean(config.get('status', 'Coding · Learning'), 62)}</text>
</svg>'''


def main() -> int:
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(generate(config), encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)} for {config.get('name', 'profile')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
