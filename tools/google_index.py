#!/usr/bin/env python3
"""구글 Indexing API 즉시 색인 통보.

구글은 IndexNow에 참여하지 않으므로 구글만 별도로 통보한다.

준비물(최초 1회):
  1) 구글 클라우드 콘솔에서 프로젝트 생성 → "Indexing API" 사용 설정.
  2) 서비스 계정 생성 → JSON 키 발급(service_account.json).
  3) 구글 서치콘솔에서 해당 서비스 계정 이메일을
     '소유자(Owner)' 권한으로 사이트에 추가.
  4) 의존성 설치:  pip install google-auth requests

사용법:
  # 사이트맵 전체 통보
  python tools/google_index.py --all --key service_account.json

  # 특정 URL 통보(글 올릴 때마다)
  python tools/google_index.py /magazine/new-post/ --key service_account.json

참고: Indexing API는 공식적으로 JobPosting·BroadcastEvent 대상 API입니다.
일반 페이지에도 통보는 가능하지만 색인이 보장되지는 않습니다. 안정적인
색인의 기본은 서치콘솔 + sitemap.xml 이며, 이 도구는 '통보 가속' 보조입니다.
"""
import os
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL  # noqa: E402

BASE = BASE_URL.rstrip("/")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]


def sitemap_urls():
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        sys.exit("sitemap.xml 이 없습니다. 먼저 `python3 build.py` 를 실행하세요.")
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [el.text.strip() for el in ET.parse(path).findall(".//s:loc", ns)]


def normalize(urls):
    out = []
    for u in urls:
        u = u.strip()
        if u.startswith("/"):
            u = BASE + u
        elif u and not u.startswith("http"):
            u = f"{BASE}/{u.lstrip('/')}"
        if u:
            out.append(u)
    return out


def main():
    argv = sys.argv[1:]
    if "--key" not in argv:
        sys.exit("서비스 계정 키 경로가 필요합니다: --key service_account.json")
    key_path = argv[argv.index("--key") + 1]
    dry = "--dry-run" in argv
    rest = [a for a in argv
            if a not in ("--all", "--dry-run", "--key", key_path)]
    urls = sitemap_urls() if ("--all" in argv or not rest) else normalize(rest)

    print(f"통보 URL {len(urls)}건 (구글 Indexing API)")
    for u in urls:
        print(f"  - {u}")
    if dry:
        print("\n[dry-run] 실제 전송하지 않았습니다.")
        return

    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        sys.exit("의존성 필요:  pip install google-auth requests")

    creds = service_account.Credentials.from_service_account_file(
        key_path, scopes=SCOPES)
    session = AuthorizedSession(creds)
    ok = 0
    for u in urls:
        r = session.post(ENDPOINT, json={"url": u, "type": "URL_UPDATED"})
        if r.status_code == 200:
            ok += 1
            print(f"[OK] {u}")
        else:
            print(f"[{r.status_code}] {u} → {r.text[:160]}")
    print(f"\n완료: {ok}/{len(urls)} 성공")


if __name__ == "__main__":
    main()
