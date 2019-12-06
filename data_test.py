from data import Database, DBObject
import pytest


class Widget(DBObject):
    table_name = "widgets"

    def __init__(self, name=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name

    @classmethod
    def create_table_sql(cls):
        return """
        CREATE TABLE widgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
        """

    def save_sql(self):
        if self.id:
            return "UPDATE widgets SET name = ? WHERE id = ?", [
                self.name, self.id
            ]

        return "INSERT INTO WIDGETS (name) VALUES (?)", [self.name]

    def validate(self):
        if not self.name:
            return False
        return True


@pytest.fixture
def db():
    database = Database(":memory:")
    database.create_table(Widget)
    return database


def test_creating_widget():
    widget = Widget(name="Test")
    assert widget.id is None
    assert widget.name == "Test"


def test_saving_widget_to_db(db):
    widget = Widget(name="Test")
    db.save(widget)
    assert widget.id is not None


def test_invalid_widget_cannot_be_saved(db):
    widget = Widget()
    was_saved = db.save(widget)
    assert not was_saved
    assert widget.id is None


def test_retrieving_widget_from_db(db):
    widget = Widget(name="Test")
    db.save(widget)

    widgets = db.select(Widget, "WHERE id = ?", [widget.id])
    assert widgets[0].id == widget.id
    assert widgets[0].name == widget.name


def test_deleting_widget_from_db(db):
    widget = Widget(name="Test")
    db.save(widget)

    db.delete(widget)

    widgets = db.select(Widget, "WHERE id = ?", [widget.id])
    assert widgets == []
