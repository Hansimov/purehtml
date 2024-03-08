# remove whole element with these tags
COMMON_REMOVE_TAGS = ["script", "style", "button", "link"]

# keep env tags (do not unwrap)
HEADER_TAGS = ["title", "h1", "h2", "h3", "h4", "h5", "h6"]
LIST_TAGS = ["ul", "ol", "li", "dl", "dt", "dd"]
TABLE_TAGS = ["table", "tr", "td", "th"]
PARA_TAGS = ["section", "div", "p", "code", "pre", "blockquote", "details"]
KEEP_ENV_TAGS = [*HEADER_TAGS, *LIST_TAGS, *TABLE_TAGS, *PARA_TAGS]

# keep format tags (do not unwrap)
POS_TAGS = ["sub", "sup"]
FONT_TAGS = ["b", "strong", "em"]
MARK_TAGS = ["i", "u", "s", "strike", "mark", "ins", "del", "cite"]
KEEP_FORMAT_TAGS = [*POS_TAGS, *FONT_TAGS, *MARK_TAGS]

COMMON_REMOVE_CLASSES = [
    "sidebar",
    "footer",
    "related",
    "comment",
    "topbar",
    "offcanvas",
    "navbar",
]
COM_163_REMOVE_CLASSES = [
    "post_((top)|(side)|(recommends)|(crumb)|(statement)|(next)|(jubao))",
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

# ===================================== #

REMOVE_TAGS = [*COMMON_REMOVE_TAGS, *WIKIPEDIA_REMOVE_TAGS]
REMOVE_CLASSES = [
    *COMMON_REMOVE_CLASSES,
    *COM_163_REMOVE_CLASSES,
    *WIKIPEDIA_REMOVE_CLASSES,
    *DOC_PYTHON_REMOVE_CLASSES,
]
# UNWRAP_TAGS = [*COMMON_UNWRAP_TAGS]
