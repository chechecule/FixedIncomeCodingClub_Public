# src/KbondSearch/regex_base.py

import re 

# extracts 22.10.02 or 23.1.13
dt_ext = re.compile(r"[\d]{1,2}.[\d]{1,2}.[\d]{1,2}")

# extracts 22-1, or 23-12
ty_ext = re.compile(r"[\d]{2}-[\d]{1,2}")

# extracts 

# extracts abbreviations of ty and msb
abbr_ext_bond = re.compile(
	r"([국당]|[국전]|[통당]|[통딱]|[구통]|[구구통])"
)

abbr_ext_buy = re.compile(
	r"([사자]|[사고]|[+])"
)

abbr_ext_sell = re.compile(
	r"([팔자]|[팔고]|[대치]|[-])"
)

# 회사이름 추출
# 주말 이자관련 추출
# 섹터 추출
# newline 기준으로 짜르기 


