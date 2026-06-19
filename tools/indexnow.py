#!/usr/bin/env python3
"""IndexNow 즉시 색인 통보 — 빙·네이버·얀덱스 등 IndexNow 참여 엔진.

IndexNow는 한 번 통보하면 참여 엔진 전체로 공유된다(빙·네이버·얀덱스·Seznam).
구글은 IndexNow 미참여이므로 tools/google_index.py 를 함께 사용한다.

사용법:
  # 사이트맵의 모든 URL을 일괄 통보(최초 등록 / 대량 갱신 시)
  python tools/indexnow.py --all

  # 특정 URL만 통보(글 1~수십 개 올렸을 때)
  python tools/indexnow.py https://dobong-massage1.pages.dev/magazine/new-post/
  python tools/indexnow.py /magazine/new-post/ /dobong-gu/chang-dong/

  # 통보 없이 전송될 내용만 확인
  python tools/indexnow.py --all --dry-run

전제: 빌드 시 생성된 {INDEXNOW_KEY}.txt 가 배포 도메인 루트에서 200으로
열려야 한다(예: https://도메인/<KEY>.txt). 배포 후 한 번 확인하면 된다.
"""
import json
import os
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL, INDEXNOW_KEY  # noqa: E402

BASE = BASE_URL.rstrip("/")
HOST = BASE.split("://", 1)[-1]
KEY_LOCATION = f"{BASE}/{INDEXNOW_KEY}.txt"
# IndexNow 단일 엔드포인트(참여 엔진끼리 자동 공유). 보조로 엔진별 엔드포인트도 둔다.
ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://searchadvisor.naver.com/indexnow",  # 네이버
    "https://www.bing.com/indexnow",             # 빙
]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sitemap_urls():
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        sys.exit("sitemap.xml 이 없습니다. 먼저 `python3 build.py` 를 실행하세요.")
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    tree = ET.parse(path)
    return [el.text.strip() for el in tree.findall(".//s:loc", ns)]


def normalize(urls):
    out = []
    for u in urls:
        u = u.strip()
        if not u:
            continue
        if u.startswith("/"):
            u = BASE + u
        elif not u.startswith("http"):
            u = f"{BASE}/{u.lstrip('/')}"
        out.append(u)
    return out


def submit(urls, dry_run=False):
    # IndexNow 권장: 한 요청당 최대 10,000 URL
    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    print(f"호스트: {HOST}")
    print(f"키 파일: {KEY_LOCATION}")
    print(f"통보 URL {len(urls)}건:")
    for u in urls:
        print(f"  - {u}")
    if dry_run:
        print("\n[dry-run] 실제 전송하지 않았습니다.")
        return
    for ep in ENDPOINTS:
        req = urllib.request.Request(
            ep, data=body,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                print(f"[OK] {ep} → {resp.status} {resp.reason}")
        except urllib.error.HTTPError as e:
            # 200/202 외에도 일부 엔진은 4xx로 키 검증 결과를 알려준다.
            print(f"[{e.code}] {ep} → {e.reason}")
        except Exception as e:  # noqa: BLE001
            print(f"[ERR] {ep} → {e}")


def main():
    args = [a for a in sys.argv[1:] if a not in ("--all", "--dry-run")]
    dry = "--dry-run" in sys.argv
    if "--all" in sys.argv or not args:
        urls = sitemap_urls()
    else:
        urls = normalize(args)
    if not urls:
        sys.exit("통보할 URL이 없습니다.")
    submit(urls, dry_run=dry)


if __name__ == "__main__":
    main()
