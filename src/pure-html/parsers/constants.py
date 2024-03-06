COMMON_IGNORE_TAGS = ["script", "style", "button"]

COMMON_IGNORE_CLASSES = [
    "sidebar",
    "footer",
    "related",
    "comment",
    "topbar",
    "offcanvas",
    "navbar",
]
COM_163_IGNORE_CLASSES = [
    "post_((top)|(side)|(recommends)|(crumb)|(statement)|(next)|(jubao))",
    "ntes-.*nav",
    "nav-bottom",
]
WIKIPEDIA_IGNORE_TAGS = [
    "nav",
]
WIKIPEDIA_IGNORE_CLASSES = [
    "mw-jump-link",
    "language-list",
    "p-lang-btn",
    "(vector-)((header)|(column)|(sticky-pinned)|(dropdown-content)|(page-toolbar)|(body-before-content))",
    "navbox",
    "catlinks",
]

WIKIPEDIA_IGNORE_WORDS = [
    "\[edit\]",
]

IGNORE_TAGS = [*COMMON_IGNORE_TAGS, *WIKIPEDIA_IGNORE_TAGS]
IGNORE_CLASSES = [
    *COMMON_IGNORE_CLASSES,
    *COM_163_IGNORE_CLASSES,
    *WIKIPEDIA_IGNORE_CLASSES,
]
IGNORE_WORDS = [*WIKIPEDIA_IGNORE_WORDS]
