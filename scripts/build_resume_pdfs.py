"""Build the public English and Persian resume PDFs for the GitHub profile."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TMP = ROOT / "tmp" / "pdfs"
OUTPUT = ROOT / "output" / "pdf"

CSS = r"""
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #d9e4e3; color: #173331; }
body { font-family: "Noto Sans", "DejaVu Sans", sans-serif; }
body.fa { font-family: "Noto Sans Arabic", "Noto Naskh Arabic", "DejaVu Sans", sans-serif; direction: rtl; }
.page { width: 210mm; height: 296mm; padding: 15mm 16mm 13mm; background: #f7fbfa; position: relative; overflow: hidden; page-break-after: always; break-after: page; }
.page:last-child { page-break-after: auto; }
.topline { position: absolute; inset: 0 0 auto; height: 5mm; background: linear-gradient(90deg,#0a6b63,#23ad9c 58%,#405ea8); }
.header { margin: 2mm -16mm 7mm; padding: 7mm 16mm 6mm; color: #eafffa; background: #092e31; display: grid; grid-template-columns: 1.3fr 1fr; gap: 8mm; align-items: end; }
.fa .header { grid-template-columns: 1.3fr 1fr; }
h1 { margin: 0 0 1mm; font-size: 25pt; line-height: 1.05; letter-spacing: -.4px; }
.fa h1 { font-size: 23pt; letter-spacing: 0; }
.role { color: #75f5df; font-weight: 700; font-size: 11pt; letter-spacing: .8px; text-transform: uppercase; }
.fa .role { letter-spacing: 0; }
.contact { font-size: 8.3pt; line-height: 1.75; text-align: right; color: #b7d9d5; }
.fa .contact { text-align: left; direction: ltr; }
h2 { margin: 0 0 3mm; color: #086d65; font-size: 13.5pt; line-height: 1.2; display: flex; align-items: center; gap: 2.5mm; }
h2::before { content: ""; display: inline-block; width: 4mm; height: 4mm; border-radius: 50%; background: #26b6a3; box-shadow: 0 0 0 1.5mm #d9f5ef; flex: 0 0 auto; }
.fa h2 { font-size: 14.5pt; }
h3 { margin: 0 0 1mm; font-size: 10.8pt; color: #163d3a; }
p { margin: 0 0 2.5mm; font-size: 9.2pt; line-height: 1.58; color: #375957; }
.fa p { font-size: 9.8pt; line-height: 1.75; }
.section { margin-bottom: 6mm; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; }
.grid-3 { display: grid; grid-template-columns: repeat(3,1fr); gap: 4mm; }
.card { padding: 4mm 4.5mm; border: .35mm solid #b8dcd7; border-radius: 3mm; background: #fff; break-inside: avoid; }
.card.accent { border-top: 1.4mm solid #25aa99; }
.meta { font-size: 8pt; color: #527a76; font-weight: 700; margin-bottom: 2mm; }
.pill-row { display: flex; flex-wrap: wrap; gap: 2mm; margin-top: 2mm; }
.pill { padding: 1.2mm 2.5mm; border-radius: 99px; background: #e2f4f0; color: #086d65; font-size: 7.7pt; font-weight: 700; }
ul { margin: 1.5mm 0 0; padding-left: 5mm; }
li { margin: 0 0 1.5mm; font-size: 8.7pt; line-height: 1.42; color: #365b58; }
.fa ul { padding-left: 0; padding-right: 5mm; }
.fa li { font-size: 9.3pt; line-height: 1.58; }
.compact li { margin-bottom: .9mm; font-size: 8.2pt; }
.fa .compact li { font-size: 8.9pt; }
.lead { font-size: 10pt; color: #244b48; }
.fa .lead { font-size: 10.5pt; }
.project-title { font-size: 18pt; color: #075d58; margin-bottom: 1mm; }
.project-subtitle { color: #536f99; font-weight: 700; font-size: 9pt; margin-bottom: 4mm; }
.focus { padding: 4mm 5mm; border-radius: 3mm; background: linear-gradient(110deg,#0b3a3b,#183c58); color: #e9fffa; }
.focus p, .focus li { color: #c9e7e3; }
.focus strong { color: #7ff5df; }
.skill-group { margin-bottom: 3.5mm; }
.skill-group h3 { color: #08766c; font-size: 10pt; }
.skill-line { font-size: 8.4pt; line-height: 1.55; color: #42615f; }
.ai-highlight { margin: 0 -1mm 3.5mm; padding: 2.2mm 3mm; border: .4mm solid #6f91df; border-radius: 2.5mm; background: linear-gradient(110deg,#e3f7f3,#eaf0ff); box-shadow: inset 1.2mm 0 #4387ff; }
.ai-highlight h3 { color: #405ea8; }
.fa .ai-highlight { box-shadow: inset -1.2mm 0 #4387ff; }
.fa .skill-line { font-size: 9.1pt; line-height: 1.7; }
.footer { position: absolute; left: 16mm; right: 16mm; bottom: 6mm; display: flex; justify-content: space-between; border-top: .3mm solid #c8dedb; padding-top: 2mm; color: #668985; font-size: 7.4pt; }
.fa .footer { direction: rtl; }
.page-no { color: #0b746a; font-weight: 700; direction: ltr; unicode-bidi: isolate; }
.tagline { font-family: "DejaVu Sans Mono", monospace; }
"""


def document(title: str, lang: str, pages: list[str]) -> str:
    page_html = "".join(
        f'<section class="page"><div class="topline"></div>{body}'
        f'<div class="footer"><span>Kourosh Mansouri · {title}</span><span class="page-no">{index} / {len(pages)}</span></div></section>'
        for index, body in enumerate(pages, 1)
    )
    body_class = "fa" if lang == "fa" else "en"
    direction = "rtl" if lang == "fa" else "ltr"
    return f'''<!doctype html><html lang="{lang}" dir="{direction}"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body class="{body_class}">{page_html}</body></html>'''


EN_HEADER = '''
<header class="header"><div><h1>Kourosh Mansouri</h1><div class="role">Junior Java Developer</div></div><div class="contact">Tehran, Iran<br>github.com/Kourosh-MD<br>linkedin.com/in/kourosh-mansouri-a6a1291b2</div></header>
'''

FA_HEADER = '''
<header class="header"><div><h1>کوروش منصوری</h1><div class="role">توسعه‌دهنده جونیور جاوا</div></div><div class="contact">Tehran, Iran<br>github.com/Kourosh-MD<br>linkedin.com/in/kourosh-mansouri-a6a1291b2</div></header>
'''

EN_PAGES = [
    EN_HEADER + '''
<section class="section"><h2>Professional Profile</h2><p class="lead">Computer Engineering student focused on Java backend development with Spring Boot. I strengthen my backend expertise through personal projects using REST APIs, JDBC and PostgreSQL.</p><p>Over 1.5 years in a technical environment, I gained hands-on experience with database CRUD, data operations, automated data ingestion, AI-agent workflows, product development and product design.</p><p>Strong in AI-assisted execution, prompt engineering, token-efficient context management and coordinating agents and services. Current goal: secure a professional opportunity as a Junior Java Developer.</p></section>
<section class="section"><h2>Professional Experience</h2><div class="card accent"><h3>Noavaran Hoosh Kavan</h3><div class="meta">1.5 years</div><div class="grid-2"><ul><li>Built AI-assisted data-ingestion workflows for Excel and other data sources.</li><li>Transformed and validated data into required database-ready formats.</li><li>Inserted and updated records and performed database CRUD operations.</li><li>Automated recurring data-entry and processing tasks.</li></ul><ul><li>Built agents for AI token usage and service lifecycle management.</li><li>Designed workflows that coordinate other agents and connected services.</li><li>Monitored service usage and surfaced charge, payment and renewal needs.</li><li>Contributed to product development, product design and website work.</li></ul></div><p>This experience combines AI-agent design, data automation, database operations, product thinking and practical systems work with Linux, VPN, networking and infrastructure tools.</p></div></section>
<div class="grid-2"><section class="card"><h2>Education</h2><h3>Computer Engineering - In Progress</h3><p>Islamic Azad University<br>Tehran, Iran</p></section><section class="card"><h2>Java Backend Direction</h2><div class="pill-row"><span class="pill">Java</span><span class="pill">Spring Boot</span><span class="pill">REST APIs</span><span class="pill">PostgreSQL</span><span class="pill">Maven</span><span class="pill">JDBC</span></div></section></div>
''',
    EN_HEADER + '''
<section class="section"><div class="project-title">ENAcademy</div><div class="project-subtitle">Personal Full-Stack Language-Learning Platform · Java 21 · Spring Boot · PostgreSQL · Next.js · Docker</div><p class="lead">A portfolio-scale personal project designed to demonstrate the development of a realistic, maintainable software product.</p></section>
<div class="grid-3 section"><div class="card accent"><h2>Backend</h2><ul class="compact"><li>Java 21 and Spring Boot backend</li><li>REST API design</li><li>Controller, Service and Repository layers</li><li>Business logic and workflows</li><li>PostgreSQL persistence and CRUD</li><li>Flyway database migrations</li><li>Input validation</li><li>Authentication and authorization</li><li>Practical Spring Security</li><li>Session and refresh-token handling</li><li>Database transactions</li><li>Redis rate limiting and temporary data</li><li>Standardized API errors</li><li>Logging and request correlation</li></ul></div><div class="card accent"><h2>Product Features</h2><ul class="compact"><li>User registration and account verification</li><li>Login and account recovery</li><li>Student and access management</li><li>Courses and educational content</li><li>Progress, score and vocabulary tracking</li><li>Timed tests with autosave</li><li>Test result calculation and storage</li><li>Product purchase and access controls</li><li>Invoice generation</li><li>Administration panel</li><li>Protected-content access</li></ul></div><div class="card accent"><h2>Engineering</h2><ul class="compact"><li>Docker and Docker Compose</li><li>Backend testing</li><li>Playwright end-to-end automation</li><li>GitHub Actions and CI</li><li>Application health checks</li><li>Load testing for 100 concurrent users</li><li>Architecture documentation</li><li>API and database documentation</li><li>Security documentation</li></ul></div></div>
<section class="focus"><h2 style="color:#7ff5df">Project Purpose</h2><p>Build a presentable, real-world application that demonstrates Java backend engineering, Spring Boot development, database design, security thinking, testing and operational awareness.</p></section>
''',
    EN_HEADER + '''
<section class="section"><h2>Technical Competencies</h2><div class="grid-2"><div class="card"><div class="skill-group"><h3>Core Java</h3><div class="skill-line">Java syntax · OOP · Collections · Generics · Streams · Exceptions · CRUD · layered design · maintainable code</div></div><div class="skill-group"><h3>JVM and Memory</h3><div class="skill-line">Heap and stack · garbage collection · JVM metrics · heap dumps · memory leaks · introductory JVM tuning</div></div><div class="skill-group"><h3>Backend and Database</h3><div class="skill-line">Spring Boot · REST · JDBC · PostgreSQL · Flyway · transactions · validation · Spring Security · Redis</div></div><div class="skill-group"><h3>Testing and Automation</h3><div class="skill-line">Backend testing · Playwright · end-to-end testing · request logging · health checks · load testing</div></div></div><div class="card"><div class="skill-group"><h3>DevOps and Systems</h3><div class="skill-line">Linux · Ubuntu · Docker · Docker Compose · GitHub Actions · CI · VPN · networking · troubleshooting</div></div><div class="skill-group"><h3>Web Development</h3><div class="skill-line">HTML · CSS · JavaScript · Node.js · Next.js · website maintenance · WordPress · RTL layouts</div></div><div class="skill-group"><h3>Tools and Workflow</h3><div class="skill-line">Git · GitHub · Maven · API design · debugging · documentation · request correlation</div></div><div class="skill-group ai-highlight"><h3>AI Agent Engineering &amp; Prompting</h3><div class="skill-line">Strong AI-assisted execution · prompt engineering · token and context management · Dify chatbot development · data-ingestion agents · multi-agent and service orchestration · lifecycle monitoring for charges, payments and renewals</div></div></div></div></section>
<section class="section"><h2>Professional Strengths</h2><div class="grid-2"><ul><li>Problem solving and technical troubleshooting</li><li>Strong AI-assisted execution and prompt engineering</li><li>Comfort with unfamiliar systems and tools</li><li>Understanding concepts beyond surface-level usage</li></ul><ul><li>Real-world operational awareness</li><li>Clear technical documentation</li><li>Interest in maintainable software</li><li>Efficient token and context management</li></ul></div></section>
<section class="focus"><h2 style="color:#7ff5df">Career Direction</h2><p><strong>Current target:</strong> Junior Java Developer</p><p class="tagline">Java → Spring Boot → REST APIs → PostgreSQL → Backend Architecture</p><p><strong>Long-term goal:</strong> expand frontend skills in JavaScript and Next.js and grow into a Full-Stack Developer.</p></section>
''',
]

FA_PAGES = [
    FA_HEADER + '''
<section class="section"><h2>خلاصه حرفه‌ای</h2><p class="lead">دانشجوی مهندسی کامپیوتر و متمرکز بر توسعه Java Backend با Spring Boot هستم. مهارت‌های Backend خود را از طریق پروژه‌های شخصی با REST API، JDBC و PostgreSQL تقویت کرده‌ام.</p><p>در ۱.۵ سال فعالیت در یک محیط فنی، تجربه عملی در عملیات پایگاه داده، CRUD، ورود خودکار داده، طراحی جریان‌های AI Agent، توسعه محصول و دیزاین محصول کسب کرده‌ام.</p><p>در استفاده مؤثر از AI، Prompt Engineering، مدیریت بهینه Token و Context و هماهنگ‌سازی Agentها و سرویس‌ها توانمند هستم. هدف فعلی من ورود به بازار کار به عنوان Junior Java Developer است.</p></section>
<section class="section"><h2>تجربه کاری</h2><div class="card accent"><h3>نوآوران هوش کاوان</h3><div class="meta">۱.۵ سال</div><div class="grid-2"><ul><li>طراحی فرایندهای ورود داده از Excel و سایر منابع با کمک AI Agent</li><li>تبدیل، پاک‌سازی و اعتبارسنجی داده‌ها در قالب مناسب پایگاه داده</li><li>درج و به‌روزرسانی رکوردها و انجام عملیات CRUD</li><li>خودکارسازی ورود و پردازش داده‌های تکراری</li></ul><ul><li>ساخت Agent برای مدیریت مصرف Token و چرخه سرویس‌ها</li><li>طراحی جریان‌های هماهنگ‌کننده Agentها و سرویس‌های دیگر</li><li>پایش مصرف سرویس و اعلام نیاز به شارژ، پرداخت یا تمدید</li><li>مشارکت در توسعه محصول، دیزاین محصول و امور وب‌سایت</li></ul></div><p>این تجربه ترکیبی از طراحی AI Agent، اتوماسیون داده، عملیات پایگاه داده، تفکر محصول و کار عملی با Linux، VPN، Networking و ابزارهای زیرساختی بوده است.</p></div></section>
<div class="grid-2"><section class="card"><h2>تحصیلات</h2><h3>مهندسی کامپیوتر - در حال تحصیل</h3><p>دانشگاه آزاد اسلامی<br>تهران، ایران</p></section><section class="card"><h2>مسیر Java Backend</h2><div class="pill-row"><span class="pill">Java</span><span class="pill">Spring Boot</span><span class="pill">REST APIs</span><span class="pill">PostgreSQL</span><span class="pill">Maven</span><span class="pill">JDBC</span></div></section></div>
''',
    FA_HEADER + '''
<section class="section"><div class="project-title">ENAcademy</div><div class="project-subtitle">پلتفرم شخصی آموزش زبان · Java 21 · Spring Boot · PostgreSQL · Next.js · Docker</div><p class="lead">پروژه Full-Stack در مقیاس Portfolio با هدف ساخت و ارائه یک نرم‌افزار واقعی، کامل و قابل نگهداری.</p></section>
<div class="grid-3 section"><div class="card accent"><h2>Backend</h2><ul class="compact"><li>توسعه با Java 21 و Spring Boot</li><li>طراحی REST API</li><li>معماری Controller، Service و Repository</li><li>منطق کسب‌وکار و Workflow</li><li>PostgreSQL، Persistence و CRUD</li><li>Migration با Flyway</li><li>Validation ورودی‌ها</li><li>Authentication و Authorization</li><li>Spring Security به‌صورت عملی</li><li>Session و Refresh Token</li><li>Transactionهای Database</li><li>Redis برای Rate Limiting</li><li>خطاهای استاندارد API</li><li>Logging و Request Correlation</li></ul></div><div class="card accent"><h2>قابلیت‌ها</h2><ul class="compact"><li>ثبت‌نام و تأیید حساب</li><li>ورود و بازیابی حساب</li><li>مدیریت دانش‌آموز و دسترسی‌ها</li><li>دوره‌ها و محتوای آموزشی</li><li>ذخیره Progress، امتیاز و Vocabulary</li><li>آزمون زمان‌دار با Autosave</li><li>محاسبه و ذخیره نتایج</li><li>خرید محصول و کنترل دسترسی</li><li>ایجاد Invoice</li><li>پنل مدیریت</li><li>دسترسی به محتوای محافظت‌شده</li></ul></div><div class="card accent"><h2>مهندسی و کیفیت</h2><ul class="compact"><li>Docker و Docker Compose</li><li>تست Backend</li><li>تست End-to-End با Playwright</li><li>GitHub Actions و CI</li><li>Health Check</li><li>Load Test برای ۱۰۰ کاربر هم‌زمان</li><li>مستندسازی معماری</li><li>مستندسازی API و Database</li><li>مستندسازی Security</li></ul></div></div>
<section class="focus"><h2 style="color:#7ff5df">هدف پروژه</h2><p>ساخت یک نرم‌افزار واقعی و قابل ارائه برای نمایش توانایی در مهندسی Backend با Java و Spring Boot، طراحی پایگاه داده، امنیت، تست و درک عملیاتی سیستم.</p></section>
''',
    FA_HEADER + '''
<section class="section"><h2>مهارت‌های فنی</h2><div class="grid-2"><div class="card"><div class="skill-group"><h3>Core Java</h3><div class="skill-line">Syntax · OOP · Collections · Generics · Streams · Exception Handling · CRUD · معماری لایه‌ای · کدنویسی قابل نگهداری</div></div><div class="skill-group"><h3>JVM و Memory</h3><div class="skill-line">Heap و Stack · Garbage Collection · JVM Metrics · Heap Dump · Memory Leak · آشنایی مقدماتی با JVM Tuning</div></div><div class="skill-group"><h3>Backend و Database</h3><div class="skill-line">Spring Boot · REST · JDBC · PostgreSQL · Flyway · Transaction · Validation · Spring Security · Redis</div></div><div class="skill-group"><h3>Testing و Automation</h3><div class="skill-line">Backend Testing · Playwright · E2E · Request Logging · Health Check · Load Testing</div></div></div><div class="card"><div class="skill-group"><h3>DevOps و سیستم</h3><div class="skill-line">Linux · Ubuntu · Docker · Docker Compose · GitHub Actions · CI · VPN · Networking · Troubleshooting</div></div><div class="skill-group"><h3>توسعه وب</h3><div class="skill-line">HTML · CSS · JavaScript · Node.js · Next.js · نگهداری وب‌سایت · WordPress · طراحی RTL</div></div><div class="skill-group"><h3>ابزار و Workflow</h3><div class="skill-line">Git · GitHub · Maven · API Design · Debugging · Documentation · Request Correlation</div></div><div class="skill-group ai-highlight"><h3>AI Agent، Prompt Engineering و Dify</h3><div class="skill-line">تعامل قدرتمند با AI · Prompt Engineering · مدیریت Token و Context · ساخت Chatbot با Dify · Agentهای ورود داده · هماهنگی Multi-Agent و سرویس‌ها · پایش چرخه شارژ، پرداخت و تمدید</div></div></div></div></section>
<section class="section"><h2>توانمندی‌های حرفه‌ای</h2><div class="grid-2"><ul><li>حل مسئله و عیب‌یابی فنی</li><li>یادگیری سریع و خودآموز</li><li>توانایی کار با سیستم‌ها و ابزارهای ناآشنا</li><li>درک مفاهیم فراتر از استفاده سطحی</li></ul><ul><li>شناخت محیط واقعی کار</li><li>مستندسازی فنی شفاف</li><li>علاقه به نرم‌افزار قابل نگهداری</li><li>تعهد به پیشرفت مستمر</li></ul></div></section>
<section class="focus"><h2 style="color:#7ff5df">مسیر حرفه‌ای</h2><p><strong>هدف فعلی:</strong> Junior Java Developer</p><p class="tagline">Java ← Spring Boot ← REST APIs ← PostgreSQL ← Backend Architecture</p><p><strong>هدف بلندمدت:</strong> توسعه مهارت‌های Frontend با JavaScript و Next.js و تبدیل شدن به Full-Stack Developer.</p></section>
''',
]


def build() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    documents = {
        "kourosh-mansouri-resume-en": document("English Resume", "en", EN_PAGES),
        "kourosh-mansouri-resume-fa": document("رزومه فارسی", "fa", FA_PAGES),
    }
    for stem, html in documents.items():
        source = TMP / f"{stem}.html"
        target = OUTPUT / f"{stem}.pdf"
        source.write_text(html, encoding="utf-8")
        subprocess.run(
            [
                "google-chrome",
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                "--no-pdf-header-footer",
                f"--print-to-pdf={target}",
                source.as_uri(),
            ],
            check=True,
        )
        source.unlink()
        print(f"Generated {target.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
