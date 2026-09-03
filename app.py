import streamlit as st

st.title("朝活AI")
st.write("朝の30分で、今日やることを1つ決めるAIです。")

task = st.text_input("今日やりたいことを入力してください")
st.write("入力内容：", task)

# 状態を初期化
if "result" not in st.session_state:
    st.session_state.result = None

if "task" not in st.session_state:
    st.session_state.task = None

# AIに決めてもらう
if st.button("AIに決めてもらう"):
    st.session_state.task = "Pythonを30分勉強する"
    st.session_state.result = None

# 決められたタスクを表示
if st.session_state.task:
    st.write(f"今日の朝活は「{st.session_state.task}」です。")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("やる"):
            st.session_state.result = "やる"

    with col2:
        if st.button("やらない"):
            st.session_state.result = "やらない"

# 結果を表示
if st.session_state.result:
    st.write(f"「{st.session_state.result}」を選びました。")