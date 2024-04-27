import mock
import app
import app.dependencies


@mock.patch("app.dependencies.Database")
def test_get_db(MockDatabase):
    for db in app.dependencies.get_db():
        assert MockDatabase.called

    db.close.assert_called_once_with()
