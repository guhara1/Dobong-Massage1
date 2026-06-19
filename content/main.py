# 메인 페이지 — 허브 역할. 모든 키워드를 밀어 넣지 않고 상세 페이지로 연결한다.
from .site import BASE_URL, BRAND, PHONE, PHONE_DISPLAY
from .pricing import PRICING

_JSONLD = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "HealthAndBeautyBusiness",
  "name": "{BRAND}",
  "telephone": "{PHONE}",
  "url": "{BASE_URL}/",
  "image": "{BASE_URL}/assets/og-image.png",
  "description": "도봉구 전지역 방문 출장마사지·홈타이 예약 안내",
  "areaServed": {{
    "@type": "AdministrativeArea",
    "name": "서울특별시 도봉구"
  }},
  "openingHours": "Mo-Su 00:00-24:00",
  "priceRange": "₩90,000 - ₩180,000"
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "도봉구 전지역 방문이 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "예약 시간, 정확한 위치, 배정 상황에 따라 가능 여부가 달라집니다. 지역별 안내 페이지에서 쌍문동, 방학동, 창동, 도봉동 기준으로 확인할 수 있습니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "창동역이나 쌍문역 근처도 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "주요 역세권은 역 상세 페이지에서 주변 생활권과 함께 안내합니다. 정확한 가능 여부는 예약 시 위치를 기준으로 확인합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "쌍문1동과 쌍문2동은 왜 따로 없나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "쌍문1동부터 쌍문4동까지는 쌍문동 대표 페이지에서 통합 안내하여 중복 페이지 위험을 줄입니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "당일 예약도 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "가능할 수 있지만 저녁 시간대와 주말은 문의가 많을 수 있어 사전 예약을 권장합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "테마별 관리는 어디에서 확인하나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "스웨디시, 타이마사지, 홈케어 등 테마별 안내 페이지에서 특징과 추천 대상을 확인할 수 있습니다."
      }}
    }}
  ]
}}
</script>
"""

_HERO = f"""<section class="hero">
  <div class="hero-inner">
    <p class="hero-badge">Premium Visiting Spa · 도봉구 전지역</p>
    <h1>도봉구 출장마사지 · 도봉구 홈타이<br>지역별 예약 안내</h1>
    <p class="hero-lead">샵까지 갈 필요 없이, 계신 곳에서 받는 방문형 관리 서비스.<br>자택·오피스텔·숙소 어디든 전화 한 통이면 예약이 끝납니다.</p>
    <div class="hero-actions">
      <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
      <a class="hero-btn" href="/courses/">코스 안내 보기</a>
    </div>
    <ul class="hero-stats">
      <li><strong>4개</strong><span>대표 지역</span></li>
      <li><strong>7개</strong><span>역세권 안내</span></li>
      <li><strong>14개</strong><span>관리 테마</span></li>
      <li><strong>24시간</strong><span>예약 상담</span></li>
    </ul>
  </div>
</section>
"""

_BODY = f"""
<section id="service">
<h2>도봉구에서 출장마사지를 찾을 때 먼저 확인할 기준</h2>
<p>도봉구 출장마사지를 찾는 분들은 보통 현재 위치에서 가까운 방문 가능 지역을 먼저 확인합니다. 이 페이지는 도봉구 출장마사지와 도봉구 홈타이 예약을 위한 가능 지역, 예약 절차, 코스 선택 기준, 이용 전 확인사항을 한곳에 정리한 허브입니다. 더 자세한 내용은 지역별·지하철역별·테마별 안내 페이지에서 확인하실 수 있습니다. {BRAND}는 예약 확인부터 방문형 관리까지 정해진 절차에 따라 진행하며, 처음 이용하시는 분도 어렵지 않게 예약할 수 있도록 각 단계를 명확하게 안내해 드립니다.</p>
</section>

<section id="difference">
<h2>쌍문동·방학동·창동·도봉동 생활권 차이</h2>
<p>도봉구는 서울 북부에 있는 자치구로, 창동역을 중심으로 한 교통 생활권, 쌍문역과 쌍문동 주거 생활권, 방학역과 도봉구청 주변 생활권, 도봉역·도봉산역을 중심으로 한 북부 생활권이 함께 있는 지역입니다. 그래서 도봉구 사이트는 단순히 '도봉 전지역 가능'만 적는 방식보다 대표동과 역세권을 나누어 안내하는 구조가 정확합니다. 같은 도봉구라도 동마다 주거 형태와 생활 리듬이 달라 방문 시간대나 추가 이동비 기준이 조금씩 다르기 때문입니다.</p>
</section>

<section id="coverage">
<h2>대표동별 방문 가능 지역 안내</h2>
<p>도봉구 지역 안내는 쌍문동, 방학동, 창동, 도봉동 네 개 대표동을 중심으로 구성합니다. 쌍문1동부터 쌍문4동, 방학1동부터 방학3동, 창1동부터 창5동, 도봉1동과 도봉2동처럼 숫자로 나뉜 행정동은 별도 페이지를 만들지 않고 각 대표동 페이지에서 통합해 안내합니다. 번호 동을 잘게 쪼개면 본문이 비슷해질 위험이 크기 때문에, 대표동으로 묶고 각 페이지 안에서 세부 생활권을 설명하는 방식이 더 안전합니다.</p>
</section>

<section id="areas">
<h2>지역별 안내</h2>
<p>지역별 안내는 도봉구 대표동 기준으로 구성됩니다. 각 페이지에서는 해당 생활권의 특징, 가까운 역세권, 방문 전 확인사항, 예약 가능 시간, 어울리는 테마를 동마다 고유한 내용으로 설명합니다. 아래에서 거주하시거나 머무시는 동을 선택해 주세요.</p>
<ul class="card-grid">
<li><a href="/dobong-gu/ssangmun-dong/">쌍문동</a></li>
<li><a href="/dobong-gu/banghak-dong/">방학동</a></li>
<li><a href="/dobong-gu/chang-dong/">창동</a></li>
<li><a href="/dobong-gu/dobong-dong/">도봉동</a></li>
</ul>
<p>도봉구 전체 구조가 궁금하시면 <a href="/dobong-gu/">도봉구 전체 안내</a>에서 한눈에 확인하실 수 있습니다.</p>
</section>

<section id="stations">
<h2>창동역·쌍문역·방학역·도봉산역 역세권 안내</h2>
<p>지하철역별 안내는 도봉구를 지나는 1·4·7호선 주요 역세권을 기준으로 구성합니다. 각 역 페이지에서는 인근 생활권, 주변 대표동, 예약 가능 시간, 방문 전 준비사항을 설명하며, 출구별 페이지나 역과 테마를 조합한 페이지는 만들지 않습니다. 창동역과 도봉산역처럼 환승 성격이 있는 역도 노선별로 쪼개지 않고 페이지는 하나로 운영합니다.</p>
<ul class="card-grid">
<li><a href="/dobong-gu/stations/chang-dong-station/">창동역</a></li>
<li><a href="/dobong-gu/stations/ssangmun-station/">쌍문역</a></li>
<li><a href="/dobong-gu/stations/banghak-station/">방학역</a></li>
<li><a href="/dobong-gu/stations/dobong-station/">도봉역</a></li>
<li><a href="/dobong-gu/stations/dobongsan-station/">도봉산역</a></li>
<li><a href="/dobong-gu/stations/nokcheon-station/">녹천역</a></li>
<li><a href="/dobong-gu/stations/madeul-nearby-area/">마들역 인접 생활권</a></li>
</ul>
</section>

<section id="themes">
<h2>테마별 관리 안내</h2>
<p>테마별 안내에서는 관리 유형별 특징, 추천 대상, 예약 전 확인사항을 설명합니다. 테마는 각각 독립 페이지로 운영하며, 지역 페이지와 역 페이지에서는 관련 테마로 연결만 해 드립니다. 특정 역과 테마를 조합한 페이지는 운영하지 않으니, 원하시는 관리 유형을 먼저 고른 뒤 예약 시 위치를 알려주시면 됩니다.</p>
<ul class="card-grid">
<li><a href="/themes/swedish/">스웨디시</a></li>
<li><a href="/themes/lomilomi/">로미로미</a></li>
<li><a href="/themes/thai/">타이마사지</a></li>
<li><a href="/themes/chinese/">중국마사지</a></li>
<li><a href="/themes/aroma/">아로마테라피</a></li>
<li><a href="/themes/homecare/">홈케어</a></li>
<li><a href="/themes/hotel-style/">호텔식마사지</a></li>
<li><a href="/themes/foot/">발마사지</a></li>
<li><a href="/themes/sports/">스포츠·경락</a></li>
<li><a href="/themes/skincare/">스킨케어</a></li>
<li><a href="/themes/waxing/">왁싱</a></li>
<li><a href="/themes/couple/">커플 관리</a></li>
<li><a href="/themes/24hours/">24시간</a></li>
<li><a href="/themes/overnight/">수면 가능</a></li>
</ul>
</section>

<section id="course">
<h2>코스 선택 안내</h2>
<p>코스는 이용 목적과 그날의 컨디션에 따라 선택하시는 것이 좋습니다. 누적된 피로를 풀고 싶은 분, 편안한 휴식이 필요한 분, 운동 후 근육 이완이 필요한 분, 숙소로 방문을 원하시는 분, 커플이 함께 받고 싶은 분 등 상황에 맞는 선택 기준을 <a href="/courses/">코스안내</a> 페이지에서 자세히 다룹니다. 고민되시면 예약 전화에서 상태를 말씀해 주세요. 함께 정해 드립니다.</p>
</section>

<section id="check">
<h2>도봉구 홈타이 예약 전 확인사항</h2>
<p>도봉구 출장마사지 예약 전에는 방문 가능 지역, 예약 가능 시간, 추가 이동비, 결제 방식, 취소 기준, 개인정보 처리 기준을 먼저 확인해야 합니다. 창동역과 쌍문역처럼 접근성이 좋은 지역도 있지만, 도봉산역 인근이나 도봉동 북부 생활권은 차량 이동 기준이 달라질 수 있습니다. 정확한 주소, 공동현관 출입 방법, 주차 가능 여부, 조용한 공간 확보 여부를 미리 알려주시면 방문이 한층 매끄럽습니다. 준비사항 전체는 <a href="/guide/">이용가이드</a>에, 예약 절차는 <a href="/reservation/">예약안내</a>에 정리되어 있습니다.</p>
</section>

<section id="dedup">
<h2>도봉구 페이지 중복 방지 운영 기준</h2>
<p>이 사이트는 쌍문1동·방학2동·창4동·도봉1동처럼 번호 동을 개별 페이지로 만들지 않습니다. 대신 쌍문동·방학동·창동·도봉동 대표 페이지 안에서 세부 생활권으로 설명해 중복 콘텐츠 위험을 줄입니다. 창동역은 1·4호선 환승 성격이 있어도 하나의 URL로, 도봉산역은 1·7호선 환승 성격을 하나의 페이지에서 설명합니다. 창동 아레나나 GTX-C 창동역 같은 예정 이슈도 단독 페이지를 늘리지 않고 창동·창동역 본문에서 보조 설명으로 다룹니다. 지역명만 바꾼 동일 문장은 사용하지 않으며, 모든 안내는 방문형 관리 서비스를 위한 신뢰형 정보로 작성합니다.</p>
</section>

<section id="safety">
<h2>도봉구 출장마사지 사이트 이용 방법</h2>
<p>건전하고 안전한 방문형 관리를 위해 위생 기준, 예약 정보 확인, 개인정보 보호, 금지행위 안내를 명확히 제공합니다. 도봉구 홈타이는 자택, 숙소, 사무실 인근에서 예약 가능 여부를 확인한 뒤 이용하는 방문형 관리 서비스이며, 불법적이거나 선정적인 요청은 어떤 경우에도 진행하지 않습니다. 예약 정보는 관리 목적 외에 사용하지 않습니다. 거주 지역 기준이 편하시면 지역별 안내를, 가까운 역 기준이 익숙하시면 역세권 안내를 먼저 확인해 주세요.</p>
</section>

<section id="faq">
<h2>자주 묻는 질문</h2>
<div class="faq-item">
<h3>도봉구 전지역 방문이 가능한가요?</h3>
<p>예약 시간, 정확한 위치, 배정 상황에 따라 가능 여부가 달라집니다. 지역별 안내 페이지에서 쌍문동, 방학동, 창동, 도봉동 기준으로 확인할 수 있습니다.</p>
</div>
<div class="faq-item">
<h3>창동역이나 쌍문역 근처도 가능한가요?</h3>
<p>주요 역세권은 역 상세 페이지에서 주변 생활권과 함께 안내합니다. 정확한 가능 여부는 예약 시 위치를 기준으로 확인합니다.</p>
</div>
<div class="faq-item">
<h3>쌍문1동과 창4동은 왜 따로 없나요?</h3>
<p>번호 행정동은 쌍문동·방학동·창동·도봉동 대표 페이지에서 통합 안내하여 중복 페이지 위험을 줄입니다.</p>
</div>
<div class="faq-item">
<h3>당일 예약도 가능한가요?</h3>
<p>가능할 수 있지만 저녁 시간대와 주말은 문의가 많을 수 있어 사전 예약을 권장합니다.</p>
</div>
<div class="faq-item">
<h3>테마별 관리는 어디에서 확인하나요?</h3>
<p>스웨디시, 타이마사지, 홈케어 등 테마별 안내 페이지에서 특징과 추천 대상을 확인할 수 있습니다.</p>
</div>
</section>

{PRICING}
<section id="contact" class="cta">
<h2>예약문의</h2>
<p>도봉구 방문형 관리 예약과 상담은 전화로 가장 빠르게 진행됩니다. 위치와 희망 시간을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

PAGE = {
    "path": "",
    "title": "도봉구 출장마사지｜창동·쌍문·방학·도봉 홈타이 지역 안내",
    "desc": "도봉구 출장마사지·홈타이 예약 전 창동, 쌍문동, 방학동, 도봉동 생활권을 확인하세요.",
    "h1": "도봉구 출장마사지 · 도봉구 홈타이 지역별 예약 안내",
    "body": _BODY,
    "extra_head": _JSONLD,
    "breadcrumb": [],
    "hero": _HERO,
}
