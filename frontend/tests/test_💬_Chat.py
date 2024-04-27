import mock

from streamlit.testing.v1 import AppTest

TEST_UUID = '2a3dace9-abe3-457d-959d-4a8269fdb1f5'
TEST_RESPONSES = ['Test Response']


def enable_chat_history(func):
    def execute(*args, **kwargs):
        func(*args, **kwargs)

    return execute


@mock.patch("utils.setup_cookies")
@mock.patch("💬_Chat.StathamChatbot.setup_chain")
@mock.patch("utils.enable_chat_history", enable_chat_history)
def test_chat(_, setup_cookies):

    AppTest.from_file("../💬_Chat.py").run()

    setup_cookies.assert_called_once_with()
