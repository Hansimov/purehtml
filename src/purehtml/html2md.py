import re

from bs4 import BeautifulSoup

# Markdown Cheat Sheet
# - https://www.markdownguide.org/cheat-sheet
# - https://www.markdownguide.org/basic-syntax

UNWRAP_TAGS = ["html", "a"]

GROUP_TAGS = ["div", "section", "p"]
LIST_BEGIN_TAGS = ["ul", "ol"]

NEW_LINE_TAGS = ["table"]

BEGIN_MARK_MAP = {
    "h1": "#",
    "h2": "##",
    "h3": "###",
    "h4": "####",
    "h5": "#####",
    "h6": "######",
    "li": "-",
    "ol": "1.",
}
PAIRED_MARK_MAP = {
    "b": "**",
    "strong": "**",
    "title": "**",
    "i": "*",
    "em": "*",
    "strike": "~~",
    "s": "~~",
    "del": "~~",
    "code": "`",
    "pre": "```",
}
PER_LINE_MARK_MAP = {
    "blockquote": ">",
}


def html2md(html_str):
    soup = BeautifulSoup(html_str, "html.parser")
    for element in soup.contents:
        if element.text.strip() == "":
            element.extract()

    for element in soup.find_all():
        try:
            if element.name in UNWRAP_TAGS:
                element.unwrap()
            elif element.name in GROUP_TAGS + LIST_BEGIN_TAGS:
                element.insert_before("\n")
                element.insert_after("\n")
                element.unwrap()
            elif element.name in BEGIN_MARK_MAP:
                mark = BEGIN_MARK_MAP[element.name]
                element.insert_before(mark + " ")
                element.unwrap()
            elif element.name in PAIRED_MARK_MAP:
                mark = PAIRED_MARK_MAP[element.name]
                element.insert_before(mark)
                element.insert_after(mark)
                element.unwrap()
            elif element.name in PER_LINE_MARK_MAP:
                mark = PER_LINE_MARK_MAP[element.name]
                lines = str(element).split("\n")
                marked_lines = [f"{mark} {line}" for line in lines]
                new_string = "\n".join(marked_lines)
                element.replace_with(BeautifulSoup(new_string, "html.parser"))
            elif element.name in NEW_LINE_TAGS:
                element.insert_before("\n")
                element.insert_after("\n")
            else:
                pass
        except Exception as e:
            print(f"x {e}")
            print(element)
            continue

    md_str = str(soup)
    md_str = re.sub(r"\n{3,}", "\n\n", md_str)
    return md_str
