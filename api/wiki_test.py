from .wiki import check_wiki_link, check_wiki_word


def test_bad_links():
    assert check_wiki_link("") is None
    assert check_wiki_link("Hello") is None
    assert check_wiki_link("[[Hello") is None
    assert check_wiki_link("[Hello]") is None
    assert check_wiki_link("[Hello]]") is None
    assert check_wiki_link("[[]]") is None
    assert check_wiki_link("[[Hello|]]") is None
    assert check_wiki_link("[[|]]") is None
    assert check_wiki_link("[[|Hello]]") is None


def test_good_links():
    assert check_wiki_link("[[Hello]]") == {"label": "Hello", "target": "Hello"}
    assert check_wiki_link("[[Hello|Hi]]") == {"label": "Hello", "target": "Hi"}


def test_bad_wiki_words():
    assert check_wiki_word("") is None
    assert check_wiki_word("Test") is None
    assert check_wiki_word("testWord") is None
    assert check_wiki_word("Test Word") is None
    assert check_wiki_word("1TestWord") is None
    assert check_wiki_word("Test-Word") is None


def test_good_wiki_words():
    assert check_wiki_word("TestWord") == {
        "label": "TestWord",
        "target": "TestWord"
    }
    assert check_wiki_word("TestWord1") == {
        "label": "TestWord1",
        "target": "TestWord1"
    }
