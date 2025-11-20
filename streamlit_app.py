import streamlit as st
from openai import OpenAI


# 앱 타이틀 및 설명
st.title("👗 OOTD 챗봇 (Outfit Of The Day)")

# 시스템 프롬프트 입력창 및 적용 버튼
DEFAULT_SYSTEM_PROMPT = (
    "너는 패션 전문가이자 친근한 챗봇이야. 사용자의 날씨, 기분, 일정, 스타일 선호 등을 참고해 오늘의 옷차림(Outfit Of The Day, OOTD)을 구체적으로 추천해주고, 대화를 자연스럽게 이어가."
)
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT

with st.form(key="system_prompt_form"):
    new_prompt = st.text_area(
        "시스템 프롬프트 수정 (아래 프롬프트는 챗봇의 성격을 결정합니다)",
        value=st.session_state.system_prompt,
        placeholder=DEFAULT_SYSTEM_PROMPT,
        height=100,
    )
    submitted = st.form_submit_button("적용하기")
    if submitted:
        st.session_state.system_prompt = new_prompt.strip() if new_prompt.strip() else DEFAULT_SYSTEM_PROMPT
        # 기존 대화 초기화 (시스템 프롬프트 변경 시)
        st.session_state.messages = [
            {"role": "system", "content": st.session_state.system_prompt}
        ]
        st.success("시스템 프롬프트가 적용되었습니다. 새로운 대화를 시작하세요.")

st.write("""
OpenAI GPT-4o-mini 기반 OOTD 챗봇입니다. 오늘의 날씨, 기분, 일정 등을 입력하면 상황에 맞는 옷차림을 추천해주고 대화를 이어갑니다.
""")

# .streamlit/secrets.toml의 OPENAI_API_KEY 사용
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)

# 대화 세션 상태 관리
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": st.session_state.system_prompt}
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
