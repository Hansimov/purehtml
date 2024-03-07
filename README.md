# Pure-HTML
Purify HTML by filtering tags and classes

## Install

```sh
pip install --upgrade pure-html
```

## Usage

```python
from pure_html import batch_purify_html
from pathlib import Path

html_root = Path(__file__).parent / "samples"
html_paths = list(html_root.glob("*.html"))
html_path_and_purified_content_list = batch_purify_html(html_paths)
for item in html_path_and_purified_content_list:
    html_path = item["html_path"]
    purified_content = item["purified_content"]
    print(html_path)
    print(purified_content)
```