
import streamlit as st
import random
import time

st.set_page_config(page_title="기말 범위 기억하기")

WORDS = [
    "파이썬", "알고리즘", "데이터베이스",
    "운영체제", "네트워크", "인공지능",
    "보안", "프로그래밍", "자료구조",
    "컴퓨터", "소프트웨어", "인터넷"
]

# 게임 초기화
def reset_game():
    st.session_state.answers = random.sample(WORDS, 3)
    wrong_words = [
        word for word in WORDS
        if word not in st.session_state.answers
    ]
    st.session_state.options = random.sample(
        st.session_state.answers + random.sample(wrong_words, 6), 9
    )
    st.session_state.selected = []
    st.session_state.stage = "ready"
    st.session_state.start_time = None


if "stage" not in st.session_state:
    reset_game()

st.title("기말 범위 기억하기")

# 시작 화면
if st.session_state.stage == "ready":
    st.write("단어 3개를 5초 동안 기억하세요.")

    if st.button("게임 시작"):
        st.session_state.stage = "show"
        st.session_state.start_time = time.time()
        st.rerun()

# 단어 공개
elif st.session_state.stage == "show":
    st.subheader("다음 단어를 기억하세요!")

    for word in st.session_state.answers:
        st.success(word)

    time.sleep(5)

    st.session_state.stage = "quiz"
    st.rerun()

# 정답 선택
elif st.session_state.stage == "quiz":
    st.subheader("기억나는 단어 3개를 선택하세요.")
    st.write(f"선택한 정답: {len(st.session_state.selected)}/3")

    cols = st.columns(3)

    for i, word in enumerate(st.session_state.options):
        with cols[i % 3]:
            if word in st.session_state.selected:
                st.button(
                    f"✅ {word}",
                    key=word,
                    disabled=True,
                    use_container_width=True
                )
            else:
                if st.button(
                    word,
                    key=word,
                    use_container_width=True
                ):
                    if word in st.session_state.answers:
                        st.session_state.selected.append(word)

                        if len(st.session_state.selected) == 3:
                            st.session_state.stage = "complete"

                        st.rerun()
                    else:
                        st.error("틀렸습니다! 다시 선택하세요.")

# 완료 화면
elif st.session_state.stage == "complete":
    st.success("축하합니다! 정답 3개를 모두 기억했습니다!")
    st.balloons()

    if st.button("다시 시작"):
        reset_game()
        st.rerun()
