import streamlit as st
from datetime import datetime, timedelta

# ===== 설정 (여기만 고치면 됨) =====
CLASS_START = "10:00"      # 수업 시작 시각 (HH:MM)
ON_TIME_MIN = 10           # 시작 후 N분까지 출석
LATE_MIN = 30              # 시작 후 N분까지 지각, 초과하면 결석
OPEN_BEFORE_MIN = 10       # 시작 N분 전부터 출석 가능
# ===================================

if "records" not in st.session_state:
    st.session_state.records = {}  # 학번 -> (상태, 시각)


def judge(sid: str, now: datetime):
    """학번과 현재 시각으로 출석 판정. (상태, 메시지) 반환"""
    # 1) 형식: 숫자 8자리
    if not sid.isdigit() or len(sid) != 8:
        return "오류", "학번은 숫자 8자리여야 합니다."

    # 2) 중복 출석
    if sid in st.session_state.records:
        status, t = st.session_state.records[sid]
        return "중복", f"이미 {t}에 '{status}' 처리되었습니다."

    # 3) 시간 판정
    h, m = map(int, CLASS_START.split(":"))
    start = now.replace(hour=h, minute=m, second=0, microsecond=0)
    diff = (now - start).total_seconds() / 60

    if diff < -OPEN_BEFORE_MIN:
        return "오류", f"아직 출석 시간이 아닙니다. ({OPEN_BEFORE_MIN}분 전부터 가능)"
    if diff <= ON_TIME_MIN:
        status = "출석"
    elif diff <= LATE_MIN:
        status = "지각"
    else:
        status = "결석"

    st.session_state.records[sid] = (status, now.strftime("%H:%M:%S"))
    return status, f"{sid} '{status}' 처리되었습니다."


st.title("출석봇")

# 테스트용 시각 조작
with st.sidebar:
    use_fake = st.checkbox("테스트용 시각 사용")
    fake_time = st.time_input("가상 현재 시각", value=datetime.now().time())

now = datetime.now()
if use_fake:
    now = now.replace(hour=fake_time.hour, minute=fake_time.minute, second=0)

st.caption(f"현재 시각: {now.strftime('%H:%M:%S')} / 수업 시작: {CLASS_START}")

sid = st.text_input("학번 8자리", max_chars=8).strip()

if st.button("출석하기"):
    status, msg = judge(sid, now)
    if status in ("출석",):
        st.success(msg)
    elif status in ("지각", "중복"):
        st.warning(msg)
    else:
        st.error(msg)

st.subheader("출석 현황")
if st.session_state.records:
    st.table(
        [
            {"학번": s, "상태": v[0], "시각": v[1]}
            for s, v in st.session_state.records.items()
        ]
    )
else:
    st.info("아직 출석한 사람이 없습니다.")