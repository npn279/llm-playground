import sys
import os
from time import sleep
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import logging
logging.basicConfig(level=logging.INFO)
import streamlit as st
from core import llm_openai, llm_gemini


SYSTEM_PROMPT = "You are a helpful assistant."

def reset_chat():
    st.session_state["messages"] = [{"role": "system", "content": SYSTEM_PROMPT},]

with st.sidebar:
    st.title("LLMs Playground")

    st.button("New Chat", type="primary", use_container_width=True, on_click=reset_chat)

    st.title("Settings")

    model = st.selectbox(
        'Model',
        ('Gemini-1.0-pro', 'GPT-3.5-Turbo', )
    )

    temperature = st.slider(
        label='Temperature', 
        min_value=0.0,
        max_value=1.0,
        value=0.9,
        step=0.05
    )

    if model == 'GPT-3.5-Turbo':
        MAX_TOKENS = 4096
    elif model == 'Gemini-1.0-pro':
        MAX_TOKENS = 2048
    else:
        MAX_TOKENS = 1024

    max_tokens = st.slider(
        label='Max tokens', 
        min_value=0,
        max_value=MAX_TOKENS,
        value=MAX_TOKENS,
        step=16
    )

    system_msg = st.text_area(
        label='System Prompt',
    )

    if system_msg:
        SYSTEM_PROMPT = system_msg

    logging.info(f"Selected model: {model}\nTemperature: {temperature}")

st.header("LLMs Playground", divider='rainbow')

# Chat
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": SYSTEM_PROMPT},]
    

for i in range(1, len(st.session_state.messages)):
    st.chat_message(st.session_state.messages[i]["role"]).markdown(st.session_state.messages[i]["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if model == 'Gemini-1.0-pro':
        response = llm_gemini.generate(messages=st.session_state.messages, stream=True)
        def get_chunks():
            for chunk in response:
                yield chunk.text

        msg = st.chat_message("assistant").write_stream(get_chunks)

    else:    
        response = llm_openai.generate(messages=st.session_state.messages, stream=True)
        msg = st.chat_message("assistant").write_stream(response)


    st.session_state.messages.append({"role": "assistant", "content": msg})
    logging.info(st.session_state.messages) 

