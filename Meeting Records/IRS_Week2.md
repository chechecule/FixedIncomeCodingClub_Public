<2023.06.17> <br>

Project Draft 설명 및 피드백 <br>
1) IRS 종가 크롤링(데일리 시장 가격)<br>
2) IRS 시장가에 없는 테너를 추가. 이는 판단하고자 하는 금리 시점에 따라 달라질 것 같아서 정해야함. 1M 또는 3M?<br>
3) 각 테너별 선형보간된 IRS 시장가를 이용해, 각 테너별 DF > Zero rate > implied forward CD금리 추정<br>
4) implied forward CD를 이용, 각 시점별 금리 인하/인상 또는 동결지속 기간에 대한 시장 컨센 파악할 수 있는 차트/테이블을 통해 가시화하기<br>

Tenor 판단 <br>
- 3개월이 적합할 듯<br>

시장 컨센서스 차트/테이블 <br>
- 예를 들어 산정된 수치가 20bp 정도면 25bp 인상을 하는 확률 vs 안 하는 확률로 표현 <br>
- 절반 내외의 어느 정도의 확률로 동결을 예상하고 있다 라는 식으로 표현이 될 듯<br>
- Fed Watch 에서도 확률이 분포되어 있어서 거기도 정확하지 않음 <br>

서울외국환 사이트에서 크롤링 왜 안 되는 건지  <br>

Day convention - 휴일일 경우 Trade date, payment date 조정이 필요하지 않나 <br>
- 신경쓸 필요가 거의 없음 결과적으로 큰 변수는 아닐 수 있음<br>
- 금통위 날, 대체공휴일, 휴일 다 감안하는 작업이라 난이도 상승, 현 시점에서 3개월 단위로 해도 무방할 듯 <br>

통화정책 기대감 반영 검토 기간?<br>
- 국고는 수급, IRS는 외국인 헷지 - 두개 반영 정도가 다를 것 같아서 보는 것<br>
- 왜 2년까지만 보냐면 3년이 되어버리면 다른 요인들이 반영될 가능성이 있음 <br>

자료 공유<br>
- 다빈: 작년 공부한 swap curve construction 자료, 우리은행 자료 공유 예정<br>
- 종학: 컨센 추정 엑셀시트 최종 공유 예정 (국고까지 포함)<br>
- 건순: 웹사이트 구축시 필요한 기술 스택<br>
- 모두: 지난 과제 수행 내역 업로드 <br>

GitHub <br>
- 코드는 알아서 자기 폴더에 올리면 쓰고 공통작업 폴더 또 만들면 됨 <br>
- Notion도 좋은데 코드 리뷰가 어려움. Github는 공통작업이 편하다는 장점<br>
 
다음 과제  <br>
- 다음주까지는 각자 종가 기준일자별로 크롤링 해오는 것을 구현해오는 것을 과제로  <br>
- 추가로 하자면 날짜를 오늘에서 바꿔가면서 어떻게 하는지도 해보기 <br>

웹사이트 구축시 필요한 기술 스택 (건순) <br>
- 파이썬 웹 프레임워크: https://fastapi.tiangolo.com/ko/ <br>
- JS SPA 프레임워크 : https://v2.ko.vuejs.org/v2/guide <br>
- vue 공부하시기전에, html, css, javascript 한번씩 공부가 필요합니다. 유튜브 무료코딩강의 아무거나 다 괜찮아요. <br>
- 서버 : AWS instance <br>
- 데이터베이스:Postgresql : https://www.postgresql.org <br>

정리  <br>
1. 스터디그룹 이름: Fixed Income Coding Club 결정  <br>
2. Github 만들었음  <br>
3. 이번주 과제: 각자 종가 기준일자별로 크롤링 (7/1 마무리 예정) <br>
4. 여행 일정: 재화, 기태 (6/24 불참), 다빈 (7/15 불참) <br>
5. 오프라인 회식  <br>
6. 나중에 웹사이트도 만들자  <br>