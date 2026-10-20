import streamlit as st

# ==========================================
# 1. 페이지 기본 설정 (무조건 최상단에 위치)
# ==========================================
st.set_page_config(
    page_title="팀 프로젝트 메인",
    page_icon="🚀",
    layout="wide",                  # "centered" 또는 "wide"
    initial_sidebar_state="expanded" # 사이드바 초기 상태
)


# ==========================================
# 2. 공통 세션 상태(Session State) 초기화
# ==========================================
# 각 모듈에서 공통으로 사용할 변수를 미리 정의합니다.
def init_session_state():
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None
    if "is_logged_in" not in st.session_state:
        st.session_state["is_logged_in"] = False
    if "global_data" not in st.session_state:
        st.session_state["global_data"] = {}

init_session_state()


# ==========================================
# 3. 공통 사이드바 (필요 시)
# ==========================================
with st.sidebar:
    st.title("📌 Navigation")
    st.info("왼쪽 메뉴에서 원하는 기능을 선택하세요.")
    
    # 공통 인증/프로필 정보 등을 표시할 수 있음
    if st.session_state["is_logged_in"]:
        st.write(f"접속자: {st.session_state['user_id']}")


# ==========================================
# 4. 랜딩/메인 화면 구성
# ==========================================
def main():
    st.title("👋 팀 프로젝트 메인 대시보드")
    st.caption("프로젝트의 개요 및 사용 방법을 안내하는 페이지입니다.")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💡 프로젝트 소개")
        st.write("이 앱은 여러 모듈이 결합되어 작동하는 프로젝트입니다.")
    
    with col2:
        st.subheader("🚀 시작하기")
        st.write("사이드바의 메뉴를 통해 각 모듈 기능으로 이동할 수 있습니다.")


if __name__ == "__main__":
    main()