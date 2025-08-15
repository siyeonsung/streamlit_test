

import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# 앱 제목 출력
st.title("3️⃣ 🔒 비공개 Google Sheet 연결")

st.write("secrets keys:", list(st.secrets.keys()))

# 서비스 계정 설정 안내
st.info(
    "🔐 시트에 ‘공개 설정 없이’ 안전하게 접근하려면 서비스 계정을 사용해야 합니다.\n"
    "📎 서비스 계정 이메일을 시트에 ‘뷰어’ 또는 ‘편집자’로 공유하세요."
)

# Google API 접근 범위(SCOPES) 설정
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",  # 구글 스프레드시트 읽기/쓰기
    "https://www.googleapis.com/auth/drive"          # 구글 드라이브 접근
]

# secrets.toml에 저장된 서비스 계정 정보로 인증 객체 생성
credentials = Credentials.from_service_account_info(
    st.secrets["google_service_account"],  # 서비스 계정 JSON 데이터
    scopes=SCOPES
)

# gspread를 이용해 구글 시트 API 인증
gc = gspread.authorize(credentials)

# secrets.toml에 저장된 시트 키로 구글 시트 열기
spreadsheet = gc.open_by_key(st.secrets["pw"]["gsheet_key"])

# "datainput" 워크시트 선택
sheet_input = spreadsheet.worksheet("시트1")

# 데이터 추가 함수 정의
def append_input_data(name, feedback):
    """
    Google Sheet의 'datainput' 워크시트에 한 행(name, feedback) 추가
    """
    sheet_input.append_row([name, feedback])

# 입력 폼 생성
with st.form("input_form"):
    name = st.text_input("이름")            # 이름 입력
    feedback = st.text_area("피드백")       # 피드백 입력
    submitted = st.form_submit_button("제출")

    if submitted:
        # 이름과 피드백이 모두 입력된 경우
        if name and feedback:
            append_input_data(name, feedback)     # 시트에 데이터 저장
            st.success("✅ 저장 완료")             # 성공 메시지
        else:
            st.warning("⚠️ 모든 필드를 입력해 주세요.")  # 경고 메시지

# 구분선
st.markdown("---")
st.subheader("📊 지금까지 제출된 데이터")

# Google Sheet의 모든 데이터 읽어서 DataFrame 변환
df = pd.DataFrame(sheet_input.get_all_records())

# 새로고침 버튼 클릭 시 캐시 삭제 → 최신 데이터 반영
if st.button("새로고침 🔄"):
    st.cache_data.clear()

# 피드백 컬럼 데이터 화면에 표시
st.write(df['피드백'])
