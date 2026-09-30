import streamlit as st
from google import genai
from database import save_activity, get_activities

api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

st.title("朝活AI")
st.write("朝の30分で、今日やることを1つ決めるAIです。")

task = st.text_input("今日やりたいことを入力してください")
st.write("入力内容：", task)

# 状態を初期化
if "activity" not in st.session_state:
    st.session_state.activity = None

if "decision" not in st.session_state:
    st.session_state.decision = None

if "task" not in st.session_state:
    st.session_state.task = None

# 履歴を取得
activities = get_activities()

if activities:
    recent_info = ""

    for activity in activities:
        recent_info += f"""
- 朝活：{activity[1]}
- 内容：{activity[2]}
- 実行結果：{activity[4]}
- 満足度：{activity[5]}
"""
else:
    recent_info = "なし"

# AIに決めてもらう
if st.button("AIに決めてもらう"):
    if task:

        prompt = f"""
# 役割
あなたは「朝活AI」です。
ユーザーが朝の30分で実行できる活動を1つ決めるアシスタントです。

# ユーザーの入力
「{task}」

# 判断ルール
- ユーザーが入力した「やりたいこと」をできるだけ尊重する
- 必ず30分以内で完了できる範囲まで小さくする
- 30分を超える可能性がある場合は、30分で区切れる1回分の作業にする
- 「勉強する」「作業する」「考える」などの抽象的な内容だけで終わらせず、実際に何をするのかが分かる具体的な行動にする
- 行動には、可能な限り「対象」「作業内容」「完了する量」を含める
- 特別な道具、材料、食材などを新たに用意する必要がある行動は避ける
- 今いる場所ですぐに開始できる行動を優先する
- 準備や買い物が必要な場合は、それ自体を朝活の内容にするのではなく、現在すぐに実行できる別の行動にする
- ユーザーが朝起きて、そのまま実行に移せる内容にする
- 複数の候補を提示せず、1つだけ決める
- 無理なく実行できる規模にする
- ステップは実行順に2〜4個程度にする
- 達成条件は、何をしたら完了なのか明確にする

# 最近の朝活
{recent_info}

# 最近の朝活の扱い
- 最近の朝活とまったく同じ内容を繰り返さない
- 最近の朝活と目的・作業内容がほぼ同じものもできるだけ避ける
- 過去の朝活を参考にしつつ、ユーザーの今日の入力を最優先する

# 出力ルール
- 挨拶や説明などの余計な文章を入れない
- 以下の形式を厳守する

今日の朝活：〜〜をする

ステップ：
1. 〜〜〜
2. 〜〜〜
3. 〜〜〜

達成条件：〜〜〜
"""

        try:
            interaction = client.interactions.create(
                model="gemini-3.6-flash",
                input=prompt
            )

            description = interaction.output_text

        except Exception as e:
            st.error(f"AIの処理でエラーが発生しました: {e}")
            st.stop()

        # AIが決めた内容を保存
        st.session_state.task = task
        st.session_state.activity = {
            "task": task,
            "description": description
        }

        st.session_state.decision = None

    else:
        st.warning("今日やりたいことを入力してください。")


# 決められたタスクを表示
if st.session_state.task:
    st.write(st.session_state.activity["description"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("やる"):
            st.session_state.decision = "やる"

    with col2:
        if st.button("やらない"):
            st.session_state.decision = "やらない"

            try:
                save_activity(
                    st.session_state.activity["task"],
                    st.session_state.activity["description"],
                    "やらない"
                )
                st.success("記録しました")

            except Exception as e:
                st.error(f"記録の保存でエラーが発生しました: {e}")


# 結果を表示
if st.session_state.decision == "やる":

    st.write("朝活を実行したら、結果を記録してください。")

    result = st.radio(
        "実行結果",
        ["やった", "やらなかった"]
    )

    if result == "やった":

        satisfaction = st.radio(
            "今日の朝活の満足度は？",
            [1, 2, 3, 4, 5],
            horizontal=True
        )

        if st.button("記録する"):

            try:
                save_activity(
                    st.session_state.activity["task"],
                    st.session_state.activity["description"],
                    "やる",
                    "やった",
                    satisfaction
                )

                st.success("記録しました！")

            except Exception as e:
                st.error(f"記録の保存でエラーが発生しました: {e}")

    elif result == "やらなかった":

        if st.button("記録する"):

            try:
                save_activity(
                    st.session_state.activity["task"],
                    st.session_state.activity["description"],
                    "やる",
                    "やらなかった"
                )

                st.success("記録しました！")

            except Exception as e:
                st.error(f"記録の保存でエラーが発生しました: {e}")


# 最近の活動履歴を表示
with st.expander("最近の朝活"):

    activities = get_activities()

    for activity in activities:

        created_at, task, description, decision, result, satisfaction = activity

        st.write(f"📅 {created_at}")
        st.write(f"入力：{task}")
        st.write(description)
        st.write(f"判断：{decision}")

        if result:
            st.write(f"結果：{result}")

        if satisfaction:
            st.write(f"満足度：{satisfaction} / 5")

        st.divider()
