from data import DBObject
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


@pytest.fixture(autouse=True)
def db():
    DBObject.set_database(":memory:")
    Widget.create_table()


def test_creating_widget():
    widget = Widget(name="Test")
    assert widget.id is None
    assert widget.name == "Test"


def test_saving_widget_to_db():
    widget = Widget(name="Test")
    widget.save()
    assert widget.id is not None


def test_invalid_widget_cannot_be_saved():
    widget = Widget()
    was_saved = widget.save()
    assert not was_saved
    assert widget.id is None


def test_retrieving_widget_from_db():
    widget = Widget(name="Test")
    widget.save()

    widgets = Widget.select("WHERE id = ?", [widget.id])
    assert widgets[0].id == widget.id
    assert widgets[0].name == widget.name


def test_deleting_widget_from_db():
    widget = Widget(name="Test")
    widget.save()
    widget.delete()

    widgets = Widget.select("WHERE id = ?", [widget.id])
    assert widgets == []
