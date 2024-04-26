import uuid
import utils

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate


st.set_page_config(page_title="Statham therapist – Chat", page_icon="💬")

utils.setup_cookies()

st.header("Chat with Statham now!")
st.caption("“The wolf is weaker than the tiger, but does not perform in the circus.”")


DEFAULT_TEMPLATE = """
The following is a conversation between a human and an Jason Statham Therapist. \
You should act as Jason Statham Therapist.
In response to the whining of patients, you will tell the story of how your arm \
was torn off, and then you sewed it on with another.
Or in response to sadness, you will say something like: \
“The wolf is weaker than the tiger, but does not perform in the circus.”
These answers just examples, DO NOT answer with them on each question. Try to act as a mad therapist.

Current conversation:
{history}
Human: {input}
AI:"""
PROMPT = PromptTemplate(input_variables=["history", "input"], template=DEFAULT_TEMPLATE)


class StathamChatbot:
    def setup_chain(_self):
        if "chain" not in st.session_state:
            memory = ConversationBufferMemory()
            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, streaming=True)
            st.session_state["chain"] = ConversationChain(
                prompt=PROMPT,
                llm=llm,
                memory=memory,
                verbose=True,
            )

        return st.session_state["chain"]

    @utils.enable_chat_history
    def main(self):
        chain = self.setup_chain()
        user_query = st.chat_input(placeholder="Ask me anything!")
        request_id = uuid.uuid4()

        if user_query:
            st.session_state["messages"].append({"id": request_id, "role": "user", "content": user_query})
            utils.display_msg({
                "id": request_id,
                "role": "user",
                "content": user_query
            })
            with st.chat_message("assistant"):
                st_cb = utils.StreamHandler(st.empty())
                result = chain.invoke(
                    {"input": user_query},
                    {"callbacks": [st_cb]}
                )
                response = result["response"]
                response_id = uuid.uuid4()
                st.session_state["messages"].append({"id": response_id, "role": "assistant", "content": response})
                utils.favorites_button(response_id, response)


if __name__ == "__main__":
    obj = StathamChatbot()
    obj.main()
