def check_wiki_link(candidate):
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
