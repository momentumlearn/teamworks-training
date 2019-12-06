from wiki import check_wiki_link


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
