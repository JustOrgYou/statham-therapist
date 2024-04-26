import utils

import streamlit as st


st.set_page_config(page_title="Statham therapist – Saved", page_icon="❤️")

utils.setup_cookies()

st.header("Look ~~best~~ worst answers from Jason here!")
st.caption("“One day me arm was torn off, and then it sewed it on with another...”")

user_id = utils.get_user_id()

for response in utils.get_favorites(user_id):
    with st.chat_message("assistant"):
        st.write(response)
