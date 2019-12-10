# Demo: Detect wiki links. A wiki link looks like:
# * [[Name of page]]
# * [[Link text|Name of page]]

# Create a function that takes text and returns:
# * None if not a link
# * { label: <link text>, target: <name of page> } if a link


def check_wiki_link(candidate):
    if not isinstance(candidate, str):
        return None

    if not (candidate[0:2] == "[[" and candidate[-2:] == "]]"):
        return None

    link_text = candidate[2:-2]

    if not link_text:
        return None

    if "|" in link_text:
        label, target = link_text.split("|", maxsplit=1)
        if not label or not target:
            return None
    else:
        label = link_text
        target = link_text

    return {"label": label, "target": target}


# There is one more way to create a wiki link. The classic way is to have a
# camel-cased word like NameOfPage. Create a new function check_wiki_word(text).
# It should follow the same rules as check_wiki_link(text).
def check_wiki_word(candidate):
    pass
