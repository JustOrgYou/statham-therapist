import uuid
import mock
from fastapi.testclient import TestClient

from app.main import app
from app.dependencies import get_db

client = TestClient(app)


class Database():
    def add_favorite(self, user_id: str, response: str):
        pass

    def get_favorites(self, user_id: str):
        return []

    def close(self):
        pass


def test_healthcheck():
    resp = client.get("/healthcheck")
    assert resp.status_code == 200


def mock_get_db(db: Database):
    def get_db():
        try:
            yield db
        finally:
            db.close()

    return get_db


def test_get_favorites(mocker):
    db = Database()
    close_spy = mocker.spy(db, "close")
    get_favorites_spy = mocker.spy(db, "get_favorites")

    app.dependency_overrides[get_db] = mock_get_db(db)

    user_id = str(uuid.uuid4())
    resp = client.get("/favorites", params={"user_id": user_id})

    assert resp.status_code == 200
    assert resp.json() == []

    get_favorites_spy.assert_has_calls([
        mock.call(user_id),
    ])
    close_spy.assert_called_once_with()

    app.dependency_overrides[get_db] = get_db


def test_add_favorite(mocker):
    db = Database()
    close_spy = mocker.spy(db, "close")
    add_favorite_spy = mocker.spy(db, "add_favorite")

    app.dependency_overrides[get_db] = mock_get_db(db)

    user_id = str(uuid.uuid4())
    response = "Test response"

    resp = client.post(
        "/favorites",
        data={"user_id": user_id, "response": response}
    )

    assert resp.status_code == 200
    assert resp.json() == {"user_id": user_id, "response": response}

    add_favorite_spy.assert_has_calls([
        mock.call(user_id, response),
    ])
    close_spy.assert_called_once_with()

    app.dependency_overrides[get_db] = get_db
