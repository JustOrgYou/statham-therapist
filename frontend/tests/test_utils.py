import os
import mock
import utils
import uuid


BACKEND_URL = os.environ.get("BACKEND_URL")
TEST_UUID = '2a3dace9-abe3-457d-959d-4a8269fdb1f5'


@mock.patch("utils.CookieManager")
@mock.patch("streamlit.stop")
def test_setup_cookies_not_ready(stop, MockCookieManager):
    MockCookieManager.return_value.ready.return_value = False

    utils.setup_cookies()

    assert MockCookieManager.called
    assert stop.called


@mock.patch("utils.CookieManager")
@mock.patch("streamlit.stop")
def test_setup_cookies_ready(stop, MockCookieManager):
    MockCookieManager.return_value.ready.return_value = True

    utils.setup_cookies()

    assert MockCookieManager.called
    assert not stop.called


@mock.patch("requests.get")
def test_get_favorites(mocked_get):
    user_id = str(uuid.uuid4())

    utils.get_favorites(user_id)

    mocked_get.assert_called_once_with(
        f"{BACKEND_URL}/favorites",
        params={"user_id": user_id}
    )


@mock.patch("requests.post")
def test_add_favorite(mocked_post):
    user_id = str(uuid.uuid4())
    response = "Test Response"

    utils.add_favorite(user_id, response)

    mocked_post.assert_called_once_with(
        f"{BACKEND_URL}/favorites",
        data={"user_id": user_id, "response": response}
    )


@mock.patch("utils.CookieManager")
def test_get_user_id_contains(MockCookieManager):
    MockCookieManager.return_value.ready.return_value = True
    MockCookieManager.return_value.__contains__.return_value = True
    MockCookieManager.return_value.__getitem__.return_value = TEST_UUID

    utils.setup_cookies()
    assert MockCookieManager.called

    user_id = utils.get_user_id()

    assert user_id == TEST_UUID

    MockCookieManager.return_value.__contains__.assert_called_once_with("user_id")
    MockCookieManager.return_value.__getitem__.assert_called_once_with("user_id")


@mock.patch("utils.CookieManager")
def test_get_user_id_not_contains(MockCookieManager):
    MockCookieManager.return_value.ready.return_value = True
    MockCookieManager.return_value.__contains__.return_value = False

    utils.setup_cookies()
    assert MockCookieManager.called

    user_id = utils.get_user_id()

    assert user_id != TEST_UUID

    MockCookieManager.return_value.__contains__.assert_called_once_with("user_id")
    assert MockCookieManager.return_value.__setitem__.call_count == 1


@mock.patch("utils.display_msg")
def test_enable_chat_history_has_session(mock_display_msg, mocker):
    MockedSession = mocker.MagicMock()

    mocker.patch('streamlit.session_state', return_value=MockedSession)

    test_message = {"id": uuid.uuid4(), "saved": True, "role": "user", "content": "Test message"}

    utils.st.session_state.__contains__.return_value = True
    utils.st.session_state.__getitem__.return_value = [test_message]

    stub = mocker.stub()

    decorated_stub = utils.enable_chat_history(stub)

    test_arg = "Test Arg"
    test_kwarg = "Test Kwarg"

    decorated_stub(test_arg, test_kwarg=test_kwarg)

    stub.assert_called_once_with(test_arg, test_kwarg=test_kwarg)

    utils.st.session_state.__contains__.assert_called_once_with("messages")
    utils.st.session_state.__getitem__.assert_called_once_with("messages")
    mock_display_msg.assert_called_once_with(test_message)


@mock.patch("uuid.uuid4", return_value=TEST_UUID)
@mock.patch("utils.display_msg")
def test_enable_chat_history_no_session(mock_display_msg, _, mocker):
    MockedSession = mocker.MagicMock()

    mocker.patch('streamlit.session_state', return_value=MockedSession)

    init_message = {"id": uuid.uuid4(), "saved": True, "role": "assistant", "content": "How can I help you?"}

    utils.st.session_state.__contains__.return_value = False
    utils.st.session_state.__getitem__.return_value = [init_message]

    stub = mocker.stub()

    decorated_stub = utils.enable_chat_history(stub)

    test_arg = "Test Arg"
    test_kwarg = "Test Kwarg"

    decorated_stub(test_arg, test_kwarg=test_kwarg)

    stub.assert_called_once_with(test_arg, test_kwarg=test_kwarg)

    utils.st.session_state.__contains__.assert_called_once_with("messages")
    utils.st.session_state.__setitem__.assert_called_once_with("messages", [init_message])
    mock_display_msg.assert_called_once_with(init_message)


@mock.patch("streamlit.chat_message")
@mock.patch("streamlit.write")
@mock.patch("utils.favorites_button")
def test_display_message_assistant(mock_favorites_button, mock_write, mock_chat_message):
    test_message = {"id": TEST_UUID, "role": "assistant", "content": "Test message"}

    utils.display_msg(test_message)

    mock_favorites_button.assert_called_once_with(TEST_UUID, test_message["content"])
    mock_write.assert_called_once_with(test_message["content"])
    mock_chat_message.assert_called_once_with(test_message["role"])


@mock.patch("streamlit.chat_message")
@mock.patch("streamlit.write")
@mock.patch("utils.favorites_button")
def test_display_message_assistant_saved(mock_favorites_button, mock_write, mock_chat_message):
    test_message = {"id": TEST_UUID, "saved": True, "role": "assistant", "content": "Test message"}

    utils.display_msg(test_message)

    assert mock_favorites_button.call_count == 0
    mock_write.assert_called_once_with(test_message["content"])
    mock_chat_message.assert_called_once_with(test_message["role"])


@mock.patch("streamlit.chat_message")
@mock.patch("streamlit.write")
@mock.patch("utils.favorites_button")
def test_display_message_user(mock_favorites_button, mock_write, mock_chat_message):
    test_message = {"id": TEST_UUID, "role": "user", "content": "Test message"}

    utils.display_msg(test_message)

    assert mock_favorites_button.call_count == 0
    mock_write.assert_called_once_with(test_message["content"])
    mock_chat_message.assert_called_once_with(test_message["role"])


def test_stream_handler(mocker):
    mock_container = mocker.MagicMock()
    initial_text = "Test"

    handler = utils.StreamHandler(mock_container, initial_text)
    handler.on_llm_new_token(" Token")

    mock_container.markdown.assert_called_once_with("Test Token")


def test_favorites_button(mocker):
    empty_mock = mocker.MagicMock()
    empty_mock.button.return_value = False

    mocker.patch('streamlit.empty', return_value=empty_mock)

    utils.favorites_button(TEST_UUID, "Test")

    empty_mock.button.assert_called_once_with("Save ❤️", key=TEST_UUID)


@mock.patch("utils.add_favorite")
@mock.patch("streamlit.toast")
@mock.patch("utils.get_user_id", return_value=TEST_UUID)
def test_favorites_button_clicked(_, mocked_toast, mocked_add_favorite, mocker):
    MockedSession = mocker.MagicMock()

    mocker.patch('streamlit.session_state', return_value=MockedSession)

    empty_mock = mocker.MagicMock()
    empty_mock.button.return_value = True

    mocker.patch('streamlit.empty', return_value=empty_mock)

    test_response = "Test"

    utils.favorites_button(TEST_UUID, test_response)

    empty_mock.button.assert_called_once_with("Save ❤️", key=TEST_UUID)

    mocked_toast.assert_called_once_with("Response saved to favorites!", icon="❤️")
    empty_mock.empty.assert_called_once_with()
    mocked_add_favorite.assert_called_once_with(TEST_UUID, test_response)
