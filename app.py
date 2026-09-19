import streamlit as st
from google import genai

api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

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
    if task:

        prompt = f"""
あなたは「朝活AI」です。

ユーザーは、朝の30分を使って何か1つやりたいことを入力します。

ユーザーの入力：
「{task}」

以下のルールに従って、今日の朝活を1つだけ決めてください。

- 必ず30分以内で完了できる内容にする
- ユーザーが入力した「やりたいこと」をできるだけ尊重する
- 今日すぐ実行できる具体的な行動にする
- 複数の候補を出さない
- 挨拶や余計な説明を入れない
- ステップは実行順に2〜4個程度にする
- 達成条件は「何をしたら完了なのか」が明確になるようにする
- 朝の30分で無理なく達成できる内容にする

回答は必ず以下の形式だけで出力してください。

今日の朝活：〜〜をする

ステップ：
1. 〜〜〜
2. 〜〜〜
3. 〜〜〜

達成条件：〜〜〜
"""

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        st.session_state.task = interaction.output_text
        st.session_state.result = None

    else:
        st.warning("今日やりたいことを入力してください。")



# 決められたタスクを表示
if st.session_state.task:
    st.write(st.session_state.task)

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