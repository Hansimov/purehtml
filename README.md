# PureHTML
Purify HTML by filtering tags and classes

## Install

```sh
pip install --upgrade purehtml
```

## Usage

```python
from purehtml import purify_html_files
from pathlib import Path

html_root = Path(__file__).parent / "samples"
html_paths = list(html_root.glob("*.html"))
html_path_and_purified_content_list = purify_html_files(html_paths)
for item in html_path_and_purified_content_list:
    html_path = item["html_path"]
    purified_content = item["purified_content"]
    print(html_path)
    print(purified_content)
```

## What params should I choose in different scenarios?

### Params
Here are the params of `purify_html_files()`:

- **verbose**: `bool` (default `False`)
  - `True`: Output to console
  - **`False`**: No output to console
- **output_format**: `str` (default `"html"`)
  - **`"html"`**: Output HTML format (`.html.pure`)
  - `"markdown"`: Output markdown format (`.md`)
- **keep_href**: `bool` (default `False`)
  - `True`: Keep `href` in `<a>` tags, and keep `src` in `<img>` tags
    - This is useful for detailed information retrieval
  - **`False`**: Do not keep `href` and `src`
- **keep_format_tags**: `bool` (default `True`)
  - `True`: Keep format tags
    - such as: `<sub>`, `<sup>`, `<b>`, `<strong>`, `<em>`, `<a>`, `<i>`, `<u>`, `mark`, `del`, `cite`, `blockquote`
    - This is useful for rendering HTML
  - `False`: Remove format tags
- **keep_group_tags**: `bool` (default `True`)
  - **`True`**: Keep group tags: `<div>`, `<section>`, `<details>`
    - This is useful for hierarchical processing, such as grouping texts in RAG
  - `False`: Remove group tags
- **math_style**: `str` (default `"latex"`)
  - **`"latex"`**: Convert math tag to latex string
    - This is useful for LLM and RAG
  - `"latex_in_tag"`: Wrap above latex string with tag
    - `<div>` for block, `<span>` for inline
    - This is useful for hierarchical processing
  - `"html"`: Keep math formulas in mathml format
    - This is useful for rendering HTML

### For: LLM, RAG, text chunking and embedding

Hierarchical:

```python
results = purify_html_files(
    html_paths,
    verbose=False,
    output_format="html",
    keep_href=False,
    keep_format_tags=False,
    keep_group_tags=True,
    math_style="latex_in_tag",
)
```

Flat:

```python
results = purify_html_files(
    html_paths,
    verbose=False,
    output_format="html",
    keep_href=False,
    keep_format_tags=False,
    keep_group_tags=False,  # <--
    math_style="latex",     # <--
)
```

### For: HTML rendering

With links:

```python
results = purify_html_files(
    html_paths,
    verbose=False,
    output_format="html",
    keep_href=True,         # <--
    keep_format_tags=True,  # <--
    keep_group_tags=True,   # <--
    math_style="html",      # <--
)
```

Without links: (This is the default config in dev)

```python
results = purify_html_files(
    html_paths,
    verbose=False,
    output_format="html",
    keep_href=False,        # <--
    keep_format_tags=True,
    keep_group_tags=True,
    math_style="html",
)
```

Even without any format:

```python
results = purify_html_files(
    html_paths,
    verbose=False,
    output_format="html",
    keep_href=False,
    keep_format_tags=False, # <--
    keep_group_tags=True,
    math_style="html",
)
```