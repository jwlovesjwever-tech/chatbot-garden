import streamlit as st
from openai import OpenAI

# 앱 타이틀 및 설명
st.title("👗 OOTD 챗봇 (Outfit Of The Day)")
st.write("""
OpenAI GPT-4o-mini 기반 OOTD 챗봇입니다. 오늘의 날씨, 기분, 일정 등을 입력하면 상황에 맞는 옷차림을 추천해주고 대화를 이어갑니다.
""")

# .streamlit/secrets.toml의 OPENAI_API_KEY 사용
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)

# 대화 세션 상태 관리
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "너는 패션 전문가이자 친근한 챗봇이야. 사용자의 날씨, 기분, 일정, 스타일 선호 등을 참고해 오늘의 옷차림(Outfit Of The Day, OOTD)을 구체적으로 추천해주고, 대화를 자연스럽게 이어가."
        )}
    ]

# 기존 대화 메시지 출력
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
user_input = st.chat_input("오늘의 날씨, 기분, 일정 등을 입력해보세요!")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # GPT-4o-mini로 답변 생성
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
            if m["role"] != "system" or m["content"]
        ],
        stream=True,
    )

    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
