import streamlit as st

if "todos" not in st.session_state:
    st.session_state.todos = []

st.title("✅ 할 일 목록")

new_todo = st.text_input("새 할 일을 입력하세요")
if st.button("추가") and new_todo.strip():
    st.session_state.todos.append(new_todo)

st.subheader("현재 할 일 목록")
for item in st.session_state.todos:
    st.write(f"- {item}")

if st.button("초기화"):
    st.session_state.todos = []
    st.rerun()