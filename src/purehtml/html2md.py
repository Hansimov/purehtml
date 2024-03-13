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

ESCAPED_CHAR_MAP = {
    "*": "\*",
    "_": "\_",
}


def html2md(html_str):

    for char, replaced in ESCAPED_CHAR_MAP.items():
        html_str = html_str.replace(char, replaced)

    soup = BeautifulSoup(html_str, "html.parser")

    try:
        for element in soup.contents:
            if element.text.strip() == "":
                element.extract()
        for element in soup.find_all(UNWRAP_TAGS):
            element.unwrap()
        for element in soup.find_all(BEGIN_MARK_MAP.keys()):
            mark = BEGIN_MARK_MAP[element.name]
            if element.name == "li":
                if element.parent.name == "ol":
                    mark = "1."
                else:
                    mark = "-"
            new_string = str(element).strip()
            replaced_map = {
                rf"^<{element.name}.*?>": "",
                rf"</{element.name}>$": "",
                "\n+": " ",
            }
            for pattern, replaced in replaced_map.items():
                new_string = re.sub(pattern, replaced, new_string)
            new_string = new_string.strip()
            new_string = f"{mark} {new_string}"
            new_string = re.sub(rf"{mark}\s*•", f"{mark}", new_string)
            element.replace_with(BeautifulSoup(new_string, "html.parser"))
        for element in soup.find_all(GROUP_TAGS + LIST_BEGIN_TAGS):
            element.insert_before("\n")
            element.insert_after("\n")
            element.unwrap()
        for element in soup.find_all(PAIRED_MARK_MAP.keys()):
            mark = PAIRED_MARK_MAP[element.name]
            element.insert_before(mark)
            element.insert_after(mark)
            element.unwrap()
        for element in soup.find_all(PER_LINE_MARK_MAP.keys()):
            mark = PER_LINE_MARK_MAP[element.name]
            lines = str(element).split("\n")
            marked_lines = [f"{mark} {line}" for line in lines]
            new_string = "\n".join(marked_lines)
            element.replace_with(BeautifulSoup(new_string, "html.parser"))
        for element in soup.find_all(NEW_LINE_TAGS):
            element.insert_before("\n")
            element.insert_after("\n")
    except Exception as e:
        print(f"x {e}")
        print(element)

    md_str = str(soup)
    md_str = re.sub(r"\n{3,}", "\n\n", md_str)
    return md_str
