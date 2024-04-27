import uuid
import mock
from app.database import Database


class Connection:
    def __init__(self, cursor):
        self.curr = cursor

    def cursor(self):
        return self.curr

    def commit(self):
        pass

    def execute(self, sql, args=None):
        pass

    def close(self):
        pass


class Cursor:
    def execute(self, sql, args=None):
        pass

    def fetchone(self):
        pass

    def fetchall(self):
        pass

    lastrowid = 0


def test_init(mocker):
    connect = mocker.stub()
    mocker.patch("sqlite3.connect", connect)

    Database("favorites.db")

    connect.assert_called_once_with("favorites.db")


def test_create_tables(mocker):
    cursor = Cursor()

    def connect(path):
        return Connection(cursor)

    mocker.patch("sqlite3.connect", connect)
    spy = mocker.spy(cursor, "execute")

    Database("favorites.db")

    spy.assert_has_calls([
        mock.call("""
        CREATE TABLE IF NOT EXISTS favorites (
            user_id UUID NOT NULL,
            response TEXT NOT NULL
        );"""),
    ])


def test_add_favorite(mocker):
    cursor = Cursor()

    def connect(path):
        return Connection(cursor)

    mocker.patch("sqlite3.connect", connect)

    db = Database("favorites.db")

    spy = mocker.spy(cursor, "execute")

    user_id = str(uuid.uuid4())
    test_response = "Test response"

    db.add_favorite(user_id, test_response)

    spy.assert_has_calls([
        mock.call("""
        INSERT INTO favorites (user_id, response) VALUES (?, ?)
        """, (user_id, test_response)),
    ])


def test_get_favorites(mocker):
    cursor = Cursor()

    def connect(path):
        return Connection(cursor)

    mocker.patch("sqlite3.connect", connect)

    db = Database("favorites.db")

    user_id = str(uuid.uuid4())

    spy = mocker.spy(cursor, "execute")
    db.get_favorites(user_id)

    spy.assert_has_calls([
        mock.call("""
        SELECT response
        FROM favorites
        WHERE user_id = ?
        """, (user_id,))
    ])


def test_close(mocker):
    cursor = Cursor()
    connection = Connection(cursor)

    def connect(path):
        return connection

    mocker.patch("sqlite3.connect", connect)

    db = Database("favorites.db")

    spy = mocker.spy(connection, "close")

    db.close()

    spy.assert_called_once_with()
