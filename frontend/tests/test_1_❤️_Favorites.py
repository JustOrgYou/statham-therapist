import mock

from streamlit.testing.v1 import AppTest

TEST_UUID = '2a3dace9-abe3-457d-959d-4a8269fdb1f5'
TEST_RESPONSES = ['Test Response']


@mock.patch("utils.get_user_id", return_value=TEST_UUID)
@mock.patch("utils.setup_cookies")
@mock.patch("utils.get_favorites", return_value=TEST_RESPONSES)
def test_favorites(get_favorites, setup_cookies, get_user_id):
    at = AppTest.from_file("../pages/1_❤️_Favorites.py").run()

    setup_cookies.assert_called_once_with()
    get_user_id.assert_called_once_with()
    get_favorites.assert_called_once_with(TEST_UUID)

    assert at.chat_message[0].name == "assistant"
    assert at.chat_message[0].markdown[0].value == TEST_RESPONSES[0]
