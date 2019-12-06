import string


def check_wiki_link(candidate):
    """
    Given a string, detect if it is a valid wiki link. A wiki link should
    start with two square brackets, have either text for the label and
    target or have the label and target separated by a vertical pipe, and
    end with two square brackets. Examples:

    * [[Link text]]
    * [[Link label|Link target]]
    """

    if not (candidate[:2] == "[[" and candidate[-2:] == "]]"):
        return None

    text = candidate[2:-2]
    if "|" in text:
        label, target = text.split("|", 1)
    else:
        label = text
        target = text

    if not label or not target:
        return None

    return {"label": label, "target": target}


def check_wiki_word(candidate):
    valid_characters = string.ascii_letters + string.digits

    # TODO
