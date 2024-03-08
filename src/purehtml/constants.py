COMMON_REMOVE_TAGS = ["script", "style", "button", "link"]

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

REMOVE_TAGS = [*COMMON_REMOVE_TAGS, *WIKIPEDIA_REMOVE_TAGS]
REMOVE_CLASSES = [
    *COMMON_REMOVE_CLASSES,
    *COM_163_REMOVE_CLASSES,
    *WIKIPEDIA_REMOVE_CLASSES,
    *DOC_PYTHON_REMOVE_CLASSES,
]
