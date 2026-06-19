#!/usr/bin/env python3
"""바로GO 도봉구 출장마사지 — 정적 사이트 빌드 스크립트.

content/ 패키지의 페이지 정의를 읽어 정적 HTML을 생성한다.

규칙(자동 적용):
  - 본문 텍스트 2,000자 미만 페이지는 robots noindex 처리
  - sitemap.xml 에는 index 허용 페이지만 포함
  - 지역+역+테마 조합 경로는 생성 자체가 불가능한 구조
"""
import html
import os
import re
import shutil
import sys
from datetime import datetime, timezone, timedelta
from email.utils import format_datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import PAGES
from content.site import (BASE_URL, BRAND, BUILD_DATE, GOOGLE_VERIFY,
                          INDEXNOW_KEY, NAV, NAVER_VERIFY, PHONE, PHONE_DISPLAY)

ROOT = os.path.dirname(os.path.abspath(__file__))
MIN_INDEX_CHARS = 2000


def text_length(body_html: str) -> int:
    """태그를 제거한 본문 글자수(공백 포함, 연속 공백은 1자).
    공통 요금 블록은 페이지 고유 본문이 아니므로 측정에서 제외한다."""
    text = re.sub(r'<section class="pricing">.*?</section>', " ", body_html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


def render_nav(current_path: str) -> str:
    items = []
    for label, href, children in NAV:
        active = " is-active" if href == "/" + current_path else ""
        if children:
            sub = "".join(
                f'<li><a href="{c_href}">{c_label}</a></li>'
                for c_label, c_href in children
            )
            items.append(
                f'<li class="nav-item has-sub{active}">'
                f'<a href="{href}">{label}</a>'
                f'<ul class="sub-menu">{sub}</ul></li>'
            )
        else:
            items.append(
                f'<li class="nav-item{active}"><a href="{href}">{label}</a></li>'
            )
    return "".join(items)


def render_breadcrumb(crumbs) -> str:
    if not crumbs:
        return ""
    parts = ['<nav class="breadcrumb" aria-label="현재 위치"><ol>']
    parts.append('<li><a href="/">홈</a></li>')
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            parts.append(f"<li><span>{label}</span></li>")
    parts.append("</ol></nav>")
    return "".join(parts)


def inject_toc(body: str):
    """본문 섹션(h2)에 id를 보장하고 좌측 목차 데이터를 만든다."""
    items = []
    counter = [0]

    def repl(m):
        attrs, title = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            sid = idm.group(1)
            opening = f"<section{attrs}>"
        else:
            counter[0] += 1
            sid = f"sec-{counter[0]}"
            opening = f'<section id="{sid}"{attrs}>'
        label = re.sub(r"<[^>]+>", "", title).strip()
        items.append((sid, label))
        return f"{opening}<h2>{title}</h2>"

    body = re.sub(r"<section([^>]*)>\s*<h2>(.*?)</h2>", repl, body, flags=re.S)
    return body, items


def render_toc(items) -> str:
    if len(items) < 3:
        return ""
    links = "".join(
        f'<li><a href="#{sid}">{label}</a></li>' for sid, label in items
    )
    return (
        '<aside class="page-toc"><nav aria-label="페이지 목차">'
        '<p class="toc-title">목차</p>'
        f"<ul>{links}</ul></nav></aside>"
    )


# ── 롱테일 키워드 내부링크 ─────────────────────────────────────────────
# 페이지마다 문맥에 맞는 이웃 페이지를 골라 롱테일 앵커텍스트로 연결한다.
# 같은 블록을 전 페이지에 복사하지 않고, 경로별로 다른 조합을 노출해
# 중복·과최적화 신호를 피하면서 내부링크를 강화한다.
LT_ANCHOR = {
    "/dobong-gu/": "도봉구 출장마사지 지역별 예약 안내",
    "/dobong-gu/ssangmun-dong/": "쌍문동 출장마사지·홈타이 방문 안내",
    "/dobong-gu/banghak-dong/": "방학동 출장마사지 도봉구청 생활권 안내",
    "/dobong-gu/chang-dong/": "창동 출장마사지 창동역·녹천역 생활권 안내",
    "/dobong-gu/dobong-dong/": "도봉동 출장마사지 도봉산역 생활권 안내",
    "/dobong-gu/stations/": "도봉구 역세권별 출장마사지 안내",
    "/dobong-gu/stations/chang-dong-station/": "창동역 출장마사지 환승 생활권 안내",
    "/dobong-gu/stations/ssangmun-station/": "쌍문역 출장마사지 주거권 방문 안내",
    "/dobong-gu/stations/banghak-station/": "방학역 출장마사지 도봉구청 인근 안내",
    "/dobong-gu/stations/dobong-station/": "도봉역 출장마사지 도봉동 주거권 안내",
    "/dobong-gu/stations/dobongsan-station/": "도봉산역 출장마사지 도봉산 입구 안내",
    "/dobong-gu/stations/nokcheon-station/": "녹천역 출장마사지 창동·월계 경계 안내",
    "/dobong-gu/stations/madeul-nearby-area/": "마들역 인접 생활권 출장마사지 안내",
    "/themes/": "도봉구 출장마사지 테마별 관리 안내",
    "/themes/swedish/": "도봉구 스웨디시 출장마사지 홈타이 안내",
    "/themes/thai/": "도봉구 타이마사지 출장 방문 안내",
    "/themes/aroma/": "도봉구 아로마 출장마사지 홈타이 안내",
    "/themes/homecare/": "도봉구 홈타이 홈케어 방문 관리 안내",
    "/themes/foot/": "도봉구 발마사지 출장 방문 안내",
    "/themes/sports/": "도봉구 스포츠·경락 출장마사지 안내",
    "/themes/24hours/": "도봉구 24시간 출장마사지 심야 예약 안내",
    "/themes/overnight/": "도봉구 숙박 가능 출장마사지 안내",
    "/reservation/": "도봉구 출장마사지 예약 방법 안내",
    "/guide/": "도봉구 출장마사지 이용 전 확인사항 안내",
    "/courses/": "도봉구 출장마사지 코스·요금 안내",
    "/massage/": "도봉 출장마사지 이용 절차 안내",
}

_DONGS = ["ssangmun-dong", "banghak-dong", "chang-dong", "dobong-dong"]
_STATIONS = ["chang-dong-station", "ssangmun-station", "banghak-station",
             "dobong-station", "dobongsan-station", "nokcheon-station",
             "madeul-nearby-area"]
_KEY_THEMES = ["swedish", "thai", "aroma", "homecare", "foot", "sports",
               "24hours", "overnight"]
_DONG_STATIONS = {
    "ssangmun-dong": ["ssangmun-station"],
    "banghak-dong": ["banghak-station"],
    "chang-dong": ["chang-dong-station", "nokcheon-station"],
    "dobong-dong": ["dobong-station", "dobongsan-station"],
}
_STATION_DONG = {
    "chang-dong-station": "chang-dong", "ssangmun-station": "ssangmun-dong",
    "banghak-station": "banghak-dong", "dobong-station": "dobong-dong",
    "dobongsan-station": "dobong-dong", "nokcheon-station": "chang-dong",
    "madeul-nearby-area": "dobong-dong",
}


def related_for(path: str):
    cur = "/" + path if path else "/"
    items = []

    def add(h):
        if h != cur and h in LT_ANCHOR and h not in items:
            items.append(h)

    if path == "":  # 메인
        for h in ["/dobong-gu/", "/dobong-gu/ssangmun-dong/", "/dobong-gu/banghak-dong/",
                  "/dobong-gu/chang-dong/", "/dobong-gu/dobong-dong/",
                  "/dobong-gu/stations/chang-dong-station/",
                  "/dobong-gu/stations/dobongsan-station/",
                  "/themes/swedish/", "/themes/homecare/", "/reservation/"]:
            add(h)
    elif path == "dobong-gu/":  # 지역 허브
        for d in _DONGS:
            add(f"/dobong-gu/{d}/")
        add("/dobong-gu/stations/"); add("/themes/"); add("/reservation/"); add("/guide/")
    elif path.startswith("dobong-gu/stations/") and path != "dobong-gu/stations/":  # 역 상세
        st = path.split("/")[2]
        idx = _STATIONS.index(st)
        add(f"/dobong-gu/{_STATION_DONG[st]}/")
        for k in range(1, 4):
            add(f"/dobong-gu/stations/{_STATIONS[(idx + k) % len(_STATIONS)]}/")
        add("/dobong-gu/stations/")
        add(f"/themes/{_KEY_THEMES[idx % len(_KEY_THEMES)]}/")
        add("/reservation/"); add("/guide/")
    elif path == "dobong-gu/stations/":  # 역 허브
        for st in _STATIONS[:6]:
            add(f"/dobong-gu/stations/{st}/")
        add("/dobong-gu/"); add("/reservation/")
    elif path.startswith("dobong-gu/") and path.count("/") == 2:  # 대표 동
        dong = path.split("/")[1]
        di = _DONGS.index(dong)
        for d in _DONGS:
            if d != dong:
                add(f"/dobong-gu/{d}/")
        for stt in _DONG_STATIONS.get(dong, []):
            add(f"/dobong-gu/stations/{stt}/")
        add("/dobong-gu/")
        add(f"/themes/{_KEY_THEMES[di % len(_KEY_THEMES)]}/")
        add(f"/themes/{_KEY_THEMES[(di + 4) % len(_KEY_THEMES)]}/")
        add("/reservation/"); add("/guide/")
    elif path == "themes/":  # 테마 허브
        for t in _KEY_THEMES:
            add(f"/themes/{t}/")
        add("/dobong-gu/"); add("/reservation/")
    elif path.startswith("themes/") and path != "themes/":  # 테마 상세
        cnt = sum(ord(c) for c in path)
        for k in range(len(_KEY_THEMES)):
            add(f"/themes/{_KEY_THEMES[(cnt + k) % len(_KEY_THEMES)]}/")
            if len(items) >= 4:
                break
        add("/themes/"); add("/dobong-gu/"); add("/reservation/"); add("/guide/")
    else:  # 안내·매거진·고객센터 등
        cnt = sum(ord(c) for c in path)
        add("/dobong-gu/"); add("/dobong-gu/stations/")
        add(f"/dobong-gu/{_DONGS[cnt % 4]}/")
        add(f"/dobong-gu/{_DONGS[(cnt + 2) % 4]}/")
        add(f"/themes/{_KEY_THEMES[cnt % len(_KEY_THEMES)]}/")
        add(f"/themes/{_KEY_THEMES[(cnt + 3) % len(_KEY_THEMES)]}/")
        add("/reservation/"); add("/guide/"); add("/courses/")
    return items[:8]


def render_related(path: str) -> str:
    if path in ("support/privacy/", "support/terms/"):
        return ""
    hrefs = related_for(path)
    if len(hrefs) < 3:
        return ""
    lis = "".join(
        f'<li><a href="{h}">{LT_ANCHOR[h]}</a></li>' for h in hrefs
    )
    return (
        '<nav class="related-links" aria-label="관련 안내">'
        '<p class="related-title">함께 보면 좋은 도봉구 출장마사지·홈타이 안내</p>'
        f"<ul>{lis}</ul></nav>"
    )


def render_page(page: dict) -> str:
    path = page["path"]
    title = page["title"]
    desc = page["desc"]
    h1 = page["h1"]
    body = page["body"]
    crumbs = page.get("breadcrumb") or []
    extra_head = page.get("extra_head", "")
    hero = page.get("hero", "")

    chars = text_length(body)
    noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
    robots = (
        '<meta name="robots" content="noindex,follow">'
        if noindex
        else '<meta name="robots" content="index,follow">'
    )
    canonical = BASE_URL.rstrip("/") + "/" + path

    # 히어로가 있는 페이지(메인)는 H1을 히어로 안에서 출력한다.
    if hero:
        page_head = hero
    else:
        page_head = ""

    h1_html = "" if hero else f"<h1>{h1}</h1>"

    body, toc_items = inject_toc(body)
    toc_html = render_toc(toc_items)
    layout_cls = "page-layout has-toc" if toc_html else "page-layout"
    related_html = render_related(path)

    verify_lines = []
    if NAVER_VERIFY:
        verify_lines.append(
            f'<meta name="naver-site-verification" content="{NAVER_VERIFY}">'
        )
    if GOOGLE_VERIFY:
        verify_lines.append(
            f'<meta name="google-site-verification" content="{GOOGLE_VERIFY}">'
        )
    site_verify = ("\n".join(verify_lines) + "\n") if verify_lines else ""

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
{site_verify}<link rel="canonical" href="{canonical}">
<link rel="alternate" type="application/rss+xml" title="{BRAND} 도봉구 출장마사지·홈타이 안내" href="{BASE_URL.rstrip('/')}/rss.xml">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#0a1120">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
{extra_head}</head>
<body>
<header class="site-header">
  <div class="header-accent" aria-hidden="true"></div>
  <div class="header-top">
    <div class="header-inner">
      <a class="brand" href="/"><span class="brand-mark">바</span> <span class="brand-text">{BRAND}</span></a>
      <p class="header-tagline"><span class="tag-gem">◆</span> 도봉구 전지역 방문 관리 <span class="tag-gem">◆</span> 24시간 상담</p>
      <a class="header-call" href="tel:{PHONE}"><span class="call-label">예약전화</span> {PHONE_DISPLAY}</a>
      <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="main-nav" aria-label="주 메뉴">
    <div class="nav-inner"><ul class="nav-list">{render_nav(path)}</ul></div>
  </nav>
</header>
{page_head}<main class="site-main">
  <div class="container {layout_cls}">
    {toc_html}
    <article class="page-content">
      {render_breadcrumb(crumbs)}
      {h1_html}
      {body}
      {related_html}
    </article>
  </div>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <p class="footer-brand">{BRAND}</p>
      <p class="footer-desc">도봉구 전지역 방문 출장마사지·홈타이 안내 사이트입니다. 모든 서비스는 안내된 관리 범위와 위생·안전 기준 안에서만 제공됩니다.</p>
      <address class="footer-contact">
        <span class="footer-contact-row"><span class="footer-label">예약전화</span> <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></span>
        <span class="footer-contact-row"><span class="footer-label">상담시간</span> 연중무휴 24시간</span>
        <span class="footer-contact-row"><span class="footer-label">서비스 지역</span> 서울특별시 도봉구 전지역</span>
      </address>
    </div>
    <nav class="footer-col" aria-label="서비스 안내">
      <p class="footer-title">서비스</p>
      <ul>
        <li><a href="/massage/">도봉 출장마사지</a></li>
        <li><a href="/dobong-gu/">지역별 안내</a></li>
        <li><a href="/dobong-gu/stations/">지하철역별 안내</a></li>
        <li><a href="/themes/">테마별 안내</a></li>
        <li><a href="/courses/">코스안내</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="이용 안내">
      <p class="footer-title">이용 안내</p>
      <ul>
        <li><a href="/reservation/">예약안내</a></li>
        <li><a href="/guide/">이용가이드</a></li>
        <li><a href="/reviews/">이용 후기</a></li>
        <li><a href="/support/">고객센터</a></li>
        <li><a href="/support/#faq">자주 묻는 질문</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="정책 및 기준">
      <p class="footer-title">정책</p>
      <ul>
        <li><a href="/about/">운영자 소개</a></li>
        <li><a href="/support/privacy/">개인정보처리방침</a></li>
        <li><a href="/support/terms/">이용약관</a></li>
        <li><a href="/guide/#hygiene">위생·안전 기준</a></li>
        <li><a href="/guide/#prohibited">금지행위 안내</a></li>
        <li><a href="/support/#biz">제휴·기업 문의</a></li>
      </ul>
    </nav>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p class="footer-copy">&copy; {BRAND}. All rights reserved.</p>
      <p class="footer-note">건전한 방문 관리 서비스를 운영하며, 불법적인 요청은 어떤 경우에도 응하지 않습니다.</p>
      <div class="footer-cta-group">
        <a class="footer-cta-btn" href="https://t.me/googleseolab" target="_blank" rel="noopener nofollow"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71l-4.14-3.05-1.99 1.93c-.23.23-.42.42-.86.42z"/></svg> 웹사이트 제작문의</a>
        <a class="footer-cta-btn" href="https://t.me/googleseolab" target="_blank" rel="noopener nofollow"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71l-4.14-3.05-1.99 1.93c-.23.23-.42.42-.86.42z"/></svg> 제휴문의</a>
      </div>
    </div>
  </div>
</footer>
<a class="call-fab" href="tel:{PHONE}" aria-label="전화 예약 {PHONE_DISPLAY}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-fab-label">예약 전화</span>
</a>
<script src="/assets/nav.js"></script>
</body>
</html>
"""


def _priority(path: str):
    """sitemap 우선순위·갱신주기 — 메인 > 허브 > 일반."""
    if path == "":
        return "1.0", "daily"
    if path in ("dobong-gu/", "dobong-gu/stations/", "themes/", "magazine/",
                "massage/", "reservation/"):
        return "0.8", "weekly"
    return "0.6", "weekly"


def build() -> None:
    report = []
    pages_meta = []  # 색인 허용 페이지: (path, title, desc)

    for page in PAGES:
        path = page["path"]  # "" 또는 "dobong-gu/ssangmun-dong/" 형태
        out_dir = os.path.join(ROOT, path)
        os.makedirs(out_dir, exist_ok=True)
        html_out = render_page(page)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_out)

        chars = text_length(page["body"])
        noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
        if not noindex:
            pages_meta.append((path, page["title"], page["desc"]))
        report.append((path or "/", chars, "noindex" if noindex else "index"))

    base = BASE_URL.rstrip("/")

    # sitemap.xml (lastmod·changefreq·priority 포함 — 색인 속도 향상)
    rows = []
    for path, _title, _desc in pages_meta:
        pr, cf = _priority(path)
        rows.append(
            f"  <url><loc>{base}/{path}</loc>"
            f"<lastmod>{BUILD_DATE}</lastmod>"
            f"<changefreq>{cf}</changefreq>"
            f"<priority>{pr}</priority></url>"
        )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(rows) + "\n</urlset>\n"
        )

    # rss.xml (네이버·구글 등 피드 기반 발견 보조)
    kst = timezone(timedelta(hours=9))
    try:
        pub_dt = datetime.strptime(BUILD_DATE, "%Y-%m-%d").replace(
            hour=9, tzinfo=kst)
    except ValueError:
        pub_dt = datetime.now(kst)
    pub_rfc = format_datetime(pub_dt)
    items = []
    for path, title, desc in pages_meta:
        loc = f"{base}/{path}"
        items.append(
            "<item>"
            f"<title>{html.escape(title)}</title>"
            f"<link>{loc}</link>"
            f'<guid isPermaLink="true">{loc}</guid>'
            f"<pubDate>{pub_rfc}</pubDate>"
            f"<description>{html.escape(desc)}</description>"
            "</item>"
        )
    with open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0"><channel>\n'
            f"<title>{html.escape(BRAND)} 도봉구 출장마사지·홈타이 안내</title>\n"
            f"<link>{base}/</link>\n"
            "<description>도봉구 출장마사지·홈타이 지역별·역세권별 방문 관리 안내</description>\n"
            "<language>ko</language>\n"
            f"<lastBuildDate>{pub_rfc}</lastBuildDate>\n"
            f'<atom:link xmlns:atom="http://www.w3.org/2005/Atom" '
            f'href="{base}/rss.xml" rel="self" type="application/rss+xml"/>\n'
            + "\n".join(items)
            + "\n</channel></rss>\n"
        )

    # IndexNow 키 파일 — 루트에서 {KEY}.txt 로 접근 가능해야 한다.
    with open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w",
              encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

    # robots.txt (사이트맵·RSS 명시)
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(
            "User-agent: *\nAllow: /\n\n"
            f"Sitemap: {base}/sitemap.xml\n"
        )

    # .nojekyll (GitHub Pages)
    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    width = max(len(p) for p, _, _ in report)
    print(f"{'PATH'.ljust(width)}  CHARS  ROBOTS")
    for p, c, r in sorted(report):
        flag = "" if (r == "noindex" or MIN_INDEX_CHARS <= c <= 2500) else "  ⚠"
        print(f"{p.ljust(width)}  {str(c).rjust(5)}  {r}{flag}")
    print(f"\n{len(report)} pages built, {len(pages_meta)} in sitemap/rss.")


if __name__ == "__main__":
    build()
