# remove whole element with these tags
COMMON_REMOVE_TAGS = ["script", "style", "button", "link"]

# keep env tags (not unwrap)
HEADER_TAGS = ["title", "h1", "h2", "h3", "h4", "h5", "h6"]
LIST_TAGS = ["ul", "ol", "li", "dl", "dt", "dd"]
TABLE_TAGS = ["table", "tr", "td", "th"]
PARA_TAGS = ["p", "pre", "code", "math"]
ENV_TAGS = [*HEADER_TAGS, *LIST_TAGS, *TABLE_TAGS, *PARA_TAGS]

# keep group tags (not unwrap)
GROUP_TAGS = ["section", "div", "details"]

# keep format tags (not unwrap)
POS_TAGS = ["sub", "sup"]
FONT_TAGS = ["b", "strong", "em"]
MARK_TAGS = ["a", "i", "u", "s", "strike", "mark", "ins", "del", "cite", "blockquote"]
FORMAT_TAGS = [*POS_TAGS, *FONT_TAGS, *MARK_TAGS]

# protect tags (no preprocessing)
PROTECT_TAGS = ["math"]

# https://developer.mozilla.org/en-US/docs/Web/MathML/Element
MATH_TAGS = "math maction menclose merror mfenced mfrac mi mmultiscripts mn mo mover mpadded mphantom mroot mrow ms mspace msqrt mstyle msub msubsup msup mtable mtd mtext mtr munder munderover semantics".split()

COMMON_REMOVE_CLASSES = [
    "(?<!has)sidebar",
    "footer",
    "related",
    "comment",
    "topbar",
    "offcanvas",
    "navbar",
]
COM_163_REMOVE_CLASSES = [
    "(post_)((top)|(side)|(recommends)|(crumb)|(statement)|(next)|(jubao))",
    "ntes-.*nav",
    "nav-bottom",
]
WIKIPEDIA_REMOVE_TAGS = [
    "nav",
]
WIKIPEDIA_REMOVE_CLASSES = [
    "(mw-)((jump-link)|(editsection))",
    "language-list",
    "p-lang-btn",
    "(vector-)((header)|(column)|(sticky-pinned)|(dropdown-content)|(page-toolbar)|(body-before-content))",
    "navbox",
    "catlinks",
]
DOC_PYTHON_REMOVE_CLASSES = ["headerlink"]
AZURE_REMOVE_CLASSES = [
    "visually-hidden",
    "unsupported-browser",
    "article-header-page-actions",
    "feedback",
    "ms--additional-resources",
]

# ===================================== #

REMOVE_TAGS = [*COMMON_REMOVE_TAGS, *WIKIPEDIA_REMOVE_TAGS]
REMOVE_CLASSES = [
    *COMMON_REMOVE_CLASSES,
    *COM_163_REMOVE_CLASSES,
    *WIKIPEDIA_REMOVE_CLASSES,
    *DOC_PYTHON_REMOVE_CLASSES,
    *AZURE_REMOVE_CLASSES,
]
