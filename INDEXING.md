# 색인(인덱싱) 가이드 — 네이버·구글·빙 빠른 등록

빌드(`python3 build.py`) 시 아래가 자동 생성됩니다.

| 파일 | 용도 |
|---|---|
| `sitemap.xml` | 색인 허용 43페이지 + `lastmod·changefreq·priority` |
| `rss.xml` | 피드 기반 발견 보조(네이버·구글) |
| `robots.txt` | 크롤 허용 + 사이트맵 위치 명시 |
| `<KEY>.txt` | IndexNow 키 파일(루트에서 열려야 함) |
| 메인 `<head>` | `naver-site-verification` 메타(소유확인) |

도메인: `https://dobong-massage1.pages.dev`
IndexNow 키: `e3a77121d24e6d3c7f3b4eb24afc3186` (`content/site.py` 에서 관리)

---

## 0. 배포 직후 1회 체크
```
https://dobong-massage1.pages.dev/e3a77121d24e6d3c7f3b4eb24afc3186.txt   → 200, 키값 표시
https://dobong-massage1.pages.dev/sitemap.xml                            → 200
https://dobong-massage1.pages.dev/rss.xml                                → 200
```
키 파일이 200으로 열려야 IndexNow 통보가 검증을 통과합니다.

## 1. 소유확인 + 사이트맵 등록 (최초 1회, 가장 중요)
- **네이버 서치어드바이저**: 사이트 등록 → 메인 메타로 소유확인(이미 삽입됨) →
  요청 탭에서 `sitemap.xml`, `rss.xml` 제출.
- **구글 서치콘솔**: 속성 추가 → 소유확인 → `sitemap.xml` 제출.
  (구글 메타 인증을 쓰면 `content/site.py` 의 `GOOGLE_VERIFY` 에 값 입력 후 재빌드.)
- **빙 웹마스터도구**: 사이트 추가 → `sitemap.xml` 제출(또는 구글에서 가져오기).

> 안정적 색인의 기본은 "서치콘솔/서치어드바이저 + 사이트맵"입니다.
> 아래 IndexNow·Indexing API는 그 위에 얹는 **즉시 통보(가속)** 입니다.

## 2. IndexNow — 빙·네이버·얀덱스 즉시 통보
한 번 통보하면 IndexNow 참여 엔진끼리 공유됩니다.
```bash
# 최초 일괄 통보(배포 + 키 파일 200 확인 후 실행)
python3 tools/indexnow.py --all

# 글/페이지를 새로 올렸을 때 해당 URL만
python3 tools/indexnow.py /magazine/new-post/ /dobong-gu/chang-dong/

# 전송 전 미리보기
python3 tools/indexnow.py --all --dry-run
```

## 3. 구글 Indexing API — 구글 즉시 통보 (선택)
구글은 IndexNow 미참여라 별도 통보합니다.
```bash
pip install google-auth requests
python3 tools/google_index.py --all --key service_account.json
python3 tools/google_index.py /magazine/new-post/ --key service_account.json
```
준비: 클라우드 콘솔에서 Indexing API 사용 설정 → 서비스 계정 JSON 키 발급 →
서치콘솔에 그 서비스 계정 이메일을 **소유자**로 추가.
(공식 대상은 JobPosting·BroadcastEvent이며 일반 페이지는 색인 보장이 아닌 통보 가속용입니다.)

## 4. 사이트맵 ping (레거시·보조)
구글·빙 모두 ping 엔드포인트를 폐지/비권장합니다. 호환용으로만 둡니다.
```bash
python3 tools/ping_sitemap.py
```

---

## 새 글 올릴 때 루틴
1. `content/` 수정 → `content/site.py` 의 `BUILD_DATE` 를 오늘 날짜로 갱신
2. `python3 build.py`
3. 커밋·푸시(배포)
4. `python3 tools/indexnow.py /새/URL/` (+ 필요 시 `tools/google_index.py`)
