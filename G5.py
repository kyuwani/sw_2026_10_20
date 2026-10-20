
import streamlit as st
import random

st.set_page_config(
    page_title="고장난 계산기",
    page_icon="🧮"
)

# 실제 계산 함수
def calculate(a, b, op):
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b


# 게임 초기화
def reset_game():
    operators = ["+", "-", "*"]

    # 기존 연산과 다른 연산으로 변경
    # + → -, - → *, * → + 처럼 순환 변경
    patterns = [
        ["-", "*", "+"],
        ["*", "+", "-"]
    ]

    changed = random.choice(patterns)

    st.session_state.rules = dict(
        zip(operators, changed)
    )

    # 문제 3개 생성
    problems = []
    used = set()

    while len(problems) < 3:
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(operators)

        if (a, b, op) in used:
            continue

        used.add((a, b, op))

        real_op = st.session_state.rules[op]
        answer = calculate(a, b, real_op)

        problems.append({
            "a": a,
            "b": b,
            "op": op,
            "answer": answer
        })

    st.session_state.problems = problems
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.graded = [False, False, False]
    st.session_state.results = [None, None, None]
    st.session_state.finished = False


# 최초 실행
if "problems" not in st.session_state:
    reset_game()


# 화면 제목
st.title("🧮 고장난 계산기")

st.write(
    "고장난 계산기의 바뀐 연산 규칙을 확인하고 "
    "문제를 풀어보세요!"
)

st.divider()


# 연산 규칙 표시
st.subheader("🔧 고장난 계산기의 연산 규칙")

symbols = {
    "+": "➕",
    "-": "➖",
    "*": "✖️"
}

for original, changed in st.session_state.rules.items():
    st.info(
        f"{symbols[original]} 버튼 → "
        f"실제로는 {symbols[changed]} 연산"
    )

st.divider()


# 문제 풀이 화면
if not st.session_state.finished:

    idx = st.session_state.current
    problem = st.session_state.problems[idx]

    st.subheader(f"📝 문제 {idx + 1} / 3")

    display_op = symbols[problem["op"]]

    st.markdown(
        f"### {problem['a']} {display_op} "
        f"{problem['b']} = ?"
    )

    st.write("바뀐 연산 규칙을 적용해서 계산하세요.")

    user_answer = st.number_input(
        "정답을 입력하세요",
        step=1,
        value=0,
        key=f"answer_{idx}",
        disabled=st.session_state.graded[idx]
    )

    # 아직 채점하지 않은 문제
    if not st.session_state.graded[idx]:

        if st.button("정답 제출", type="primary"):

            correct = (
                user_answer == problem["answer"]
            )

            st.session_state.graded[idx] = True
            st.session_state.results[idx] = correct

            if correct:
                st.session_state.score += 1

            st.rerun()

    # 이미 채점한 문제
    else:

        if st.session_state.results[idx]:
            st.success("✅ 정답입니다!")

        else:
            st.error(
                f"❌ 오답입니다! "
                f"정답은 {problem['answer']}입니다."
            )

        if idx < 2:
            if st.button("다음 문제 ➡️"):
                st.session_state.current += 1
                st.rerun()

        else:
            if st.button("결과 확인 🏆"):
                st.session_state.finished = True
                st.rerun()

    st.divider()

    st.write(
        f"현재 점수: {st.session_state.score}점"
    )


# 결과 화면
else:

    st.subheader("🏆 게임 결과")

    st.metric(
        "최종 점수",
        f"{st.session_state.score} / 3점"
    )

    if st.session_state.score == 3:
        st.success(
            "🎉 축하합니다! 모든 문제를 맞혔습니다!"
        )
        st.balloons()

    else:
        st.warning(
            "아쉽습니다! 다시 도전해 보세요."
        )

    if st.button("🔄 다시 시작", type="primary"):
        reset_game()
        st.rerun()
