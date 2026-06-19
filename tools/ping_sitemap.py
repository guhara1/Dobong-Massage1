#!/usr/bin/env python3
"""사이트맵 ping (레거시) — 보조용.

주의: 구글은 2023년 6월 sitemap ping 엔드포인트를 폐지했고, 빙도 IndexNow
사용을 권장합니다. 따라서 이 스크립트는 '보조/호환' 목적이며, 실제 색인
가속은 tools/indexnow.py(빙·네이버)와 tools/google_index.py(구글),
그리고 서치콘솔 sitemap 등록이 담당합니다.

사용법:
  python tools/ping_sitemap.py
"""
import os
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL  # noqa: E402

SITEMAP = BASE_URL.rstrip("/") + "/sitemap.xml"
# 레거시 ping 엔드포인트(동작이 보장되지 않음).
TARGETS = [
    ("Google(레거시)", "https://www.google.com/ping?sitemap="),
    ("Bing(레거시)", "https://www.bing.com/ping?sitemap="),
]


def main():
    enc = urllib.parse.quote(SITEMAP, safe="")
    print(f"사이트맵: {SITEMAP}\n")
    for name, base in TARGETS:
        url = base + enc
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                print(f"[{r.status}] {name}")
        except Exception as e:  # noqa: BLE001
            print(f"[실패] {name} → {e}")
    print("\n참고: ping은 레거시입니다. 색인 통보는 indexnow.py / google_index.py 를 쓰세요.")


if __name__ == "__main__":
    main()
