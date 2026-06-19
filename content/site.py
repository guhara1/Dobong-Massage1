# 사이트 공통 설정
# 배포 도메인 확정 후 BASE_URL 을 실제 도메인으로 변경하세요.
BASE_URL = "https://dobong-massage1.pages.dev"

BRAND = "바로GO"
PHONE = "0508-202-4719"
PHONE_DISPLAY = "0508-202-4719"

# 검색엔진 사이트 소유확인
NAVER_VERIFY = "69e52b66aed6583c48592132de886694c2b4f22c"
GOOGLE_VERIFY = ""  # 구글 서치콘솔 메타 인증값(있으면 입력)

# IndexNow 키 — 빌드 시 루트에 {KEY}.txt 파일로 생성된다.
# 빙·네이버·얀덱스 등 IndexNow 참여 엔진에 즉시 색인을 통보할 때 사용.
INDEXNOW_KEY = "e3a77121d24e6d3c7f3b4eb24afc3186"

# 사이트 갱신일(사이트맵 lastmod / RSS pubDate 기준)
BUILD_DATE = "2026-06-19"

# 상단 메뉴 — 하위 메뉴에는 키워드를 반복하지 않고 지역명·역명만 표시한다.
NAV = [
    ("홈", "/", []),
    ("도봉 출장마사지", "/massage/", [
        ("출장마사지 안내", "/massage/#service"),
        ("홈타이 안내", "/massage/#hometai"),
        ("전지역 방문 안내", "/massage/#coverage"),
        ("지하철역 인근 안내", "/massage/#stations"),
        ("예약 가능 시간", "/massage/#hours"),
        ("코스 선택 안내", "/massage/#course"),
        ("이용 전 확인사항", "/massage/#check"),
        ("위생·안전 안내", "/massage/#safety"),
        ("자주 묻는 질문", "/massage/#faq"),
    ]),
    ("지역별 안내", "/dobong-gu/", [
        ("도봉구 전체", "/dobong-gu/"),
        ("쌍문동", "/dobong-gu/ssangmun-dong/"),
        ("방학동", "/dobong-gu/banghak-dong/"),
        ("창동", "/dobong-gu/chang-dong/"),
        ("도봉동", "/dobong-gu/dobong-dong/"),
    ]),
    ("지하철역별 안내", "/dobong-gu/stations/", [
        ("역 전체", "/dobong-gu/stations/"),
        ("창동역", "/dobong-gu/stations/chang-dong-station/"),
        ("쌍문역", "/dobong-gu/stations/ssangmun-station/"),
        ("방학역", "/dobong-gu/stations/banghak-station/"),
        ("도봉역", "/dobong-gu/stations/dobong-station/"),
        ("도봉산역", "/dobong-gu/stations/dobongsan-station/"),
        ("녹천역", "/dobong-gu/stations/nokcheon-station/"),
        ("마들역 인접 생활권", "/dobong-gu/stations/madeul-nearby-area/"),
    ]),
    ("테마별 안내", "/themes/", [
        ("전체 테마", "/themes/"),
        ("스웨디시", "/themes/swedish/"),
        ("로미로미", "/themes/lomilomi/"),
        ("타이마사지", "/themes/thai/"),
        ("중국마사지", "/themes/chinese/"),
        ("아로마테라피", "/themes/aroma/"),
        ("홈케어", "/themes/homecare/"),
        ("호텔식마사지", "/themes/hotel-style/"),
        ("발마사지", "/themes/foot/"),
        ("스포츠·경락", "/themes/sports/"),
        ("스킨케어", "/themes/skincare/"),
        ("왁싱", "/themes/waxing/"),
        ("커플 관리", "/themes/couple/"),
        ("24시간", "/themes/24hours/"),
        ("수면 가능", "/themes/overnight/"),
    ]),
    ("코스안내", "/courses/", [
        ("전체 코스", "/courses/"),
        ("피로 회복 관리", "/courses/#recovery"),
        ("아로마 관리", "/courses/#aroma"),
        ("스포츠 관리", "/courses/#sports"),
        ("홈타이 코스", "/courses/#hometai"),
        ("커플·가족 방문 관리", "/courses/#couple"),
        ("기업·단체 방문 관리", "/courses/#group"),
        ("가격 안내", "/courses/#price"),
        ("코스 선택 가이드", "/courses/#guide"),
    ]),
    ("예약안내", "/reservation/", [
        ("예약 방법", "/reservation/#how"),
        ("예약 가능 시간", "/reservation/#hours"),
        ("방문 가능 장소", "/reservation/#place"),
        ("결제 안내", "/reservation/#payment"),
        ("변경·취소 안내", "/reservation/#change"),
        ("예약 전 체크사항", "/reservation/#check"),
    ]),
    ("이용가이드", "/guide/", [
        ("처음 이용하시는 분", "/guide/#first"),
        ("방문 전 준비사항", "/guide/#prepare"),
        ("위생 및 안전 기준", "/guide/#hygiene"),
        ("관리 후 주의사항", "/guide/#after"),
        ("금지행위 안내", "/guide/#prohibited"),
        ("이용 FAQ", "/guide/#faq"),
    ]),
    ("매거진", "/magazine/", [
        ("전체 글", "/magazine/"),
        ("마사지 비교 가이드", "/magazine/swedish-vs-thai/"),
        ("처음 이용 가이드", "/magazine/first-time-guide/"),
        ("수면과 마사지", "/magazine/sleep-and-massage/"),
        ("운동 후 회복", "/magazine/post-workout-timing/"),
        ("어깨·목 결림 관리", "/magazine/neck-shoulder-care/"),
        ("부모님 선물 가이드", "/magazine/parents-gift/"),
    ]),
    ("후기", "/reviews/", [
        ("전체 후기", "/reviews/"),
        ("지역별 후기", "/reviews/#area"),
        ("역세권 후기", "/reviews/#station"),
        ("후기 작성 안내", "/reviews/#write"),
    ]),
    ("고객센터", "/support/", [
        ("공지사항", "/support/#notice"),
        ("자주 묻는 질문", "/support/#faq"),
        ("1:1 문의", "/support/#contact"),
        ("제휴·기업 문의", "/support/#biz"),
        ("개인정보처리방침", "/support/privacy/"),
        ("이용약관", "/support/terms/"),
    ]),
]
