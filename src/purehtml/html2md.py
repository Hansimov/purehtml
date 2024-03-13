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

PROTECTED_TAGS = ["pre", "code"]

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
}
ENV_MARK_MAP = {
    "pre": "```",
}
PER_LINE_MARK_MAP = {
    "blockquote": ">",
}
ESCAPED_CHAR_MAP = {
    "*": "\*",
    "_": "\_",
}


class HTMLToMarkdownConverter:
    def __init__(self):
        pass

    def is_in_protected_tag(self, element):
        for element in element.parents:
            if element.name in PROTECTED_TAGS:
                return True
        return False

    def escape_html(self, html_str):
        # TODO: Do not escape inside protected tags,
        #   might call in element conversion functions
        for char, replaced in ESCAPED_CHAR_MAP.items():
            html_str = html_str.replace(char, replaced)
        return html_str

    def remove_empty_elements(self, soup):
        for element in soup.contents:
            if element.text.strip() == "":
                element.extract()

    def unwrap_tag(self, html_str, tag):
        patterns = [rf"^<{tag}.*?>", rf"</{tag}>$"]
        new_string = html_str.strip()

        for pattern in patterns:
            new_string = re.sub(pattern, "", new_string)
        return new_string

    def convert_unwrap_element(self, element):
        element.unwrap()

    def convert_group_element(self, element):
        element.insert_before("\n")
        element.insert_after("\n")
        element.unwrap()

    def convert_begin_element(self, element):
        mark = BEGIN_MARK_MAP[element.name]
        new_string = str(element).strip()
        new_string = self.unwrap_tag(new_string, element.name)
        new_string = re.sub("\n+", " ", new_string)
        new_string = new_string.strip()
        new_string = f"{mark} {new_string}"
        new_element = BeautifulSoup(new_string, "html.parser")
        element.replace_with(new_element)

    def convert_li_element(self, li, level=-1, idx=0):
        if li.parent.name == "ol":
            mark = f"{idx+1}."
        else:
            mark = "-"
        new_string = str(li).strip()
        new_string = self.unwrap_tag(new_string, li.name)
        new_string = re.sub("\n+", " ", new_string)
        new_string = new_string.strip()
        indent_str = "  " * level
        new_string = f"{indent_str}{mark} {new_string}"
        new_string = re.sub(rf"{mark}\s*•", f"{mark}", new_string)
        new_li = BeautifulSoup(new_string, "html.parser")
        return new_li

    def convert_list_element(self, element, level=-1):
        level += 1
        for idx, li in enumerate(element.find_all("li")):
            new_li = self.convert_li_element(li, idx=idx, level=level)
            for child in new_li.find_all(LIST_TAGS, recursive=False):
                self.convert_list_element(child, level=level)
            li.replace_with(new_li)
        element.insert_before("\n")
        element.insert_after("\n")
        element.unwrap()

    def convert_paired_element(self, element):
        mark = PAIRED_MARK_MAP[element.name]
        element.insert_before(mark)
        element.insert_after(mark)
        element.unwrap()

    def convert_per_line_element(self, element):
        mark = PER_LINE_MARK_MAP[element.name]
        new_string = str(element).strip()
        new_string = self.unwrap_tag(new_string, element.name)
        lines = new_string.split("\n")
        marked_lines = [f"{mark} {line}" for line in lines]
        new_string = "\n".join(marked_lines)
        new_string = f"\n{new_string}\n"
        new_element = BeautifulSoup(new_string, "html.parser")
        element.replace_with(new_element)

    def convert_new_line_element(self, element):
        element.insert_before("\n")
        element.insert_after("\n")

    def remove_extra_lines(self, s):
        return re.sub(r"\n{3,}", "\n\n", s)

    def soup2str(self, soup):
        s = str(soup)
        s = html.unescape(s)
        s = self.remove_extra_lines(s)
        return s

    def convert(self, html_str):
        html_str = self.escape_html(html_str)
        soup = BeautifulSoup(html_str, "html.parser")
        self.remove_empty_elements(soup)

        for element in soup.find_all(UNWRAP_TAGS):
            self.convert_unwrap_element(element)
        for element in soup.find_all(GROUP_TAGS):
            self.convert_group_element(element)
        for element in soup.find_all(BEGIN_MARK_MAP.keys()):
            self.convert_begin_element(element)
        for element in soup.find_all(LIST_TAGS):
            self.convert_list_element(element)
        for element in soup.find_all(PAIRED_MARK_MAP.keys()):
            self.convert_paired_element(element)
        for element in soup.find_all(PER_LINE_MARK_MAP.keys()):
            self.convert_per_line_element(element)
        for element in soup.find_all(NEW_LINE_TAGS):
            self.convert_new_line_element(element)

        md_str = self.soup2str(soup)
        return md_str


def html2md(html_str):
    converter = HTMLToMarkdownConverter()
    return converter.convert(html_str)
