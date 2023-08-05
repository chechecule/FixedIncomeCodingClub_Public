from API.FSC import wrappers

#wrappers를 가져옴.

print("reset1")
print("reset1")
#결과값 구분

a = wrappers.getBondData(basDt="20230803")
#데이터 가져오기

print("reset2")
print("reset2")

#a.columns
#인덱스값 보기 위해서

#print("reset3")
#print("reset3")

#a[["basDt", "scrsItmsKcdNm", "bondIsurNm", "sicNm", "kisScrsItmsKcdNm", "kbpScrsItmsKcdNm", "niceScrsItmsKcdNm"]]

'''
basDt	기준일자
scrsItmsKcdNm	유가증권종목종류코드명
bondIsurNm	채권발행인명
'''

'''
resultCode	결과코드	2	1	00	결과코드
resultMsg	결과메시지	50	1	NORMAL SERVICE.	결과메시지
numOfRows	한 페이지 결과 수	4	1	1	한 페이지 결과 수
pageNo	페이지 번호	4	1	1	페이지 번호
totalCount	전체 결과 수	10	1	897	전체 결과 수
basDt	기준일자	8	1	20220926	작업 또는 거래의 기준이 되는 일자(년월일)
crno	법인등록번호	13	1	1101350000937	법인등록번호
bondIsurNm	채권발행인명	100	1	한국산업은행	채권을 발행한 발행 회사의 명칭
bondIssuDt	채권발행일자	8	0	20111121	채권을 발행한 일자
scrsItmsKcd	유가증권종목종류코드	4	0	1105	해당 유가증권의 종목종류(ex, 우선주, 보통주)를 관리하는 코드
scrsItmsKcdNm	유가증권종목종류코드명	100	0	금융채	해당 유가증권의 종목종류(ex, 우선주, 보통주)를 관리하는 코드의 명칭
isinCd	ISIN코드	12	0	KR31020191B6	국제 채권 식별 번호. 유가증권(채권)의 국제인증 고유번호
isinCdNm	ISIN코드명	200	0	산금채11신이1500-11-21-1(INTN)(콜)	유가증권 국제인증 고유번호 코드 이름
bondIssuFrmtNm	채권발행형태명	100	0	공사채등록	채권 발행 형태에 대한 명칭
bondExprDt	채권만기일자	8	0	20261121	채권의 만기일자(상환된 경우, 상환 일자)
bondIssuCurCd	채권발행통화코드	3	0	KRW	채권발행시 해당 채권의 각국 통화를 관리하는 코드
bondIssuCurCdNm	채권발행통화코드명	100	0	KRW	채권발행시 해당 채권의 각국 통화를 관리하는 코드의 명칭
bondPymtAmt	채권납입금액	22,3	0	50000000000	채권에 대한 납입금액
bondIssuAmt	채권발행금액	18,3	0	50000000000	채권에 대한 최초발행금액
bondSrfcInrt	채권표면이율	15,10	0	5.1	채권에 대한 표면 이자율
irtChngDcd	금리변동구분코드	1	0	1	변동금리, 고정금리등 금리를 구분하는 코드
irtChngDcdNm	금리변동구분코드명	100	0	고정	변동금리, 고정금리등 금리를 구분하는 코드의 명칭
bondIntTcd	채권이자유형코드	1	0	4	채권별 이자 유형이 이표채인지, 할인채인지등을 관리하는 코드
bondIntTcdNm	채권이자유형코드명	100	0	단리채	채권별 이자 유형이 이표채인지, 할인채인지등을 관리하는 코드의 명칭
'''