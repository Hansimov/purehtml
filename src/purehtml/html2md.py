import html
import re

from bs4 import BeautifulSoup

# Markdown Cheat Sheet
# - https://www.markdownguide.org/cheat-sheet
# - https://www.markdownguide.org/basic-syntax

UNWRAP_TAGS = ["html", "a"]

GROUP_TAGS = ["div", "section", "p"]
LIST_TAGS = ["ul", "ol"]

NEW_LINE_TAGS = ["table"]

BEGIN_MARK_MAP = {
    "h1": "#",
    "h2": "##",
    "h3": "###",
    "h4": "####",
    "h5": "#####",
    "h6": "######",
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


def unwrap_tag(html_str, tag):
    patterns = [rf"^<{tag}.*?>", rf"</{tag}>$"]
    new_string = html_str.strip()

    for pattern in patterns:
        new_string = re.sub(pattern, "", new_string)
    return new_string


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
        for element in soup.find_all(GROUP_TAGS):
            element.insert_before("\n")
            element.insert_after("\n")
            element.unwrap()
        for element in soup.find_all(BEGIN_MARK_MAP.keys()):
            mark = BEGIN_MARK_MAP[element.name]
            new_string = str(element).strip()
            new_string = unwrap_tag(new_string, element.name)
            new_string = re.sub("\n+", " ", new_string)
            new_string = new_string.strip()
            new_string = f"{mark} {new_string}"
            new_element = BeautifulSoup(new_string, "html.parser")
            element.replace_with(new_element)
        for element in soup.find_all(LIST_TAGS):
            for idx, li in enumerate(element.find_all("li")):
                if li.parent.name == "ol":
                    mark = f"{idx+1}."
                else:
                    mark = "-"
                new_string = str(li).strip()
                new_string = unwrap_tag(new_string, li.name)
                new_string = re.sub("\n+", " ", new_string)
                new_string = new_string.strip()
                indent_level = -1
                for parent in li.parents:
                    if parent.name in LIST_TAGS:
                        indent_level += 1
                indent_str = "  " * indent_level
                new_string = f"{indent_str}{mark} {new_string}"
                new_string = re.sub(rf"{mark}\s*•", f"{mark}", new_string)
                new_li = BeautifulSoup(new_string, "html.parser")
                li.replace_with(new_li)
        for element in soup.find_all(LIST_TAGS):
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
            new_string = str(element).strip()
            new_string = unwrap_tag(new_string, element.name)
            lines = new_string.split("\n")
            marked_lines = [f"{mark} {line}" for line in lines]
            new_string = "\n".join(marked_lines)
            new_string = f"\n{new_string}\n"
            new_element = BeautifulSoup(new_string, "html.parser")
            element.replace_with(new_element)
        for element in soup.find_all(NEW_LINE_TAGS):
            element.insert_before("\n")
            element.insert_after("\n")
    except Exception as e:
        print(f"x {e}")
        print(element)

    md_str = str(soup)
    md_str = html.unescape(md_str)
    md_str = re.sub(r"\n{3,}", "\n\n", md_str)
    return md_str
