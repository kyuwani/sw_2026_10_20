import streamlit as st

st.title("✅ O/X 퀴즈")

question = "지구는 둥글다?"
st.subheader(f"문제：{question}")

col1, col2 = st.columns(2)
with col1:
    o_btn = st.button("O")
with col2:
    x_btn = st.button("X")

if o_btn:
    st.success("정답입니다!")
if x_btn:
    st.error("틀렸어요")