import html
import re
import warnings

from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

# Markdown Cheat Sheet
# - https://www.markdownguide.org/cheat-sheet
# - https://www.markdownguide.org/basic-syntax

BODY_TAGS = ["html", "body"]
LINK_TAGS = ["a"]
GROUP_TAGS = ["div", "section", "p"]
TABLE_TAGS = ["table"]
LIST_TAGS = ["ul", "ol"]
DEF_TAGS = ["dl"]
CODE_TAGS = ["pre", "code"]
MATH_TAGS = ["math"]

UNWRAP_TAGS = BODY_TAGS + LINK_TAGS
NEW_LINE_TAGS = TABLE_TAGS
PROTECTED_TAGS = CODE_TAGS

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

    def is_protected(self, element):
        return self.is_in_tags(element, PROTECTED_TAGS)

    def is_in_tags(self, element, tags):
        if element.name in tags:
            return True
        for element in element.parents:
            if element.name in tags:
                return True
        return False

    def is_contain_tags(self, element, tags):
        if element.name in tags:
            return True
        for element in element.descendants:
            if element.name in tags:
                return True
        return False

    def is_related_tags(self, element, tags):
        return self.is_in_tags(element, tags) or self.is_contain_tags(element, tags)

    def check_protected_tag(func):
        def wrapper(self, element, *args, **kwargs):
            try:
                if self.is_protected(element):
                    return
                return func(self, element, *args, **kwargs)
            except Exception as e:
                print(f"{e}:")
                print(element.name)

        return wrapper

    def escape_html(self, html_str):
        for char, replaced in ESCAPED_CHAR_MAP.items():
            html_str = html_str.replace(char, replaced)
        return html_str

    def escape_element(self, element):
        if element.string:
            new_string = str(element.string)
            new_string = self.escape_html(new_string)
            element.string.replace_with(new_string)

    def escape_soup(self, soup):
        for element in soup.find_all(True):
            if not self.is_related_tags(element, CODE_TAGS):
                self.escape_element(element)

    def remove_empty_elements(self, soup):
        for element in soup.contents:
            if (
                not self.is_in_tags(element, CODE_TAGS + MATH_TAGS + TABLE_TAGS)
                and element.text.strip() == ""
            ):
                element.extract()

    def unwrap_tag(self, html_str, tag):
        patterns = [rf"^<{tag}.*?>", rf"</{tag}>$"]
        new_string = html_str.strip()

        for pattern in patterns:
            new_string = re.sub(pattern, "", new_string)
        return new_string

    @check_protected_tag
    def convert_unwrap_element(self, element):
        element.unwrap()

    @check_protected_tag
    def convert_group_element(self, element):
        element.insert_before("\n")
        element.insert_after("\n")
        element.unwrap()

    @check_protected_tag
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

    @check_protected_tag
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

    @check_protected_tag
    def convert_paired_element(self, element):
        mark = PAIRED_MARK_MAP[element.name]
        new_string = str(element)
        new_string = self.unwrap_tag(new_string, element.name)
        leading_spaces = " " * (len(new_string) - len(new_string.lstrip()))
        trailing_spaces = " " * (len(new_string) - len(new_string.rstrip()))
        new_string = new_string.strip()
        new_string = f"{leading_spaces}{mark}{new_string}{mark}{trailing_spaces}"
        new_element = BeautifulSoup(new_string, "html.parser")
        element.replace_with(new_element)

    @check_protected_tag
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

    @check_protected_tag
    def convert_new_line_element(self, element):
        element.insert_before("\n")
        element.insert_after("\n")

    def convert_code_element(self, element):
        if element.parent.name == "pre":
            element.unwrap()
        else:
            mark = "`"
            element.insert_before(mark)
            element.insert_after(mark)
            element.unwrap()

    def convert_pre_element(self, element):
        mark = "```"
        new_string = str(element)
        new_string = self.unwrap_tag(new_string, element.name)
        new_string = new_string.strip()
        new_string = f"\n{mark}\n{new_string}\n{mark}\n"
        new_element = BeautifulSoup(new_string, "html.parser")
        element.replace_with(new_element)

    def convert_dd_element(self, dd):
        new_string = str(dd).strip()
        for tag in ["<dt>", "<dd>"]:
            new_string = new_string.replace(tag, f"{tag}\n\n")
        for tag in ["</dt>", "</dd>"]:
            new_string = re.sub(rf"\s*{tag}", f"\n{tag}", new_string)
        new_dd = BeautifulSoup(new_string, "html.parser")
        return new_dd

    @check_protected_tag
    def convert_def_element(self, element):
        for dd in element.find_all(["dt", "dd"]):
            new_dd = self.convert_dd_element(dd)
            for child in new_dd.find_all(DEF_TAGS, recursive=False):
                self.convert_def_element(child)
            dd.replace_with(new_dd)

    def remove_extra_lines(self, s):
        return re.sub(r"\n{3,}", "\n\n", s)

    def soup2str(self, soup):
        s = str(soup)
        s = html.unescape(s)
        s = self.remove_extra_lines(s)
        return s

    def convert(self, html_str):
        soup = BeautifulSoup(html_str, "html.parser")
        self.remove_empty_elements(soup)
        self.escape_soup(soup)

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
        for element in soup.find_all("code"):
            self.convert_code_element(element)
        for element in soup.find_all("pre"):
            self.convert_pre_element(element)
        for element in soup.find_all(DEF_TAGS):
            self.convert_def_element(element)

        md_str = self.soup2str(soup)
        return md_str


def html2md(html_str):
    converter = HTMLToMarkdownConverter()
    return converter.convert(html_str)
