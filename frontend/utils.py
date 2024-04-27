import uuid
import os
import requests as r
import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from streamlit_cookies_manager import CookieManager

BACKEND_URL = os.environ.get("BACKEND_URL")

cookies = None


def setup_cookies():
    global cookies
    cookies = CookieManager()

    if not cookies.ready():
        st.stop()


def enable_chat_history(func):
    if os.environ.get("OPENAI_API_KEY"):
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"id": uuid.uuid4(), "saved": True, "role": "assistant", "content": "How can I help you?"}
            ]
        for msg in st.session_state["messages"]:
            display_msg(msg)

    def execute(*args, **kwargs):
        func(*args, **kwargs)

    return execute


def display_msg(msg):
    author = msg["role"]
    content = msg["content"]
    user_id = msg["id"]

    with st.chat_message(author):
        st.write(content)

        if author == "assistant" and "saved" not in msg:
            favorites_button(user_id, msg["content"])


def favorites_button(id, response):
    button = st.empty()
    if button.button("Save ❤️", key=id):
        user_id = get_user_id()
        st.toast("Response saved to favorites!", icon="❤️")
        st.session_state["messages"] = [
            {**m, "saved": True} if m["id"] == id else m for m in st.session_state["messages"]
        ]
        add_favorite(user_id, response)
        button.empty()


def get_user_id():
    if "user_id" not in cookies:
        user_id = str(uuid.uuid4())
        cookies["user_id"] = user_id
        return user_id

    return cookies["user_id"]


def get_favorites(user_id: str):
    return r.get(f"{BACKEND_URL}/favorites", params={"user_id": user_id}).json()


def add_favorite(user_id: str, response: str):
    r.post(f"{BACKEND_URL}/favorites", data={
        "user_id": user_id,
        "response": response
    })


class StreamHandler(BaseCallbackHandler):

    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)
