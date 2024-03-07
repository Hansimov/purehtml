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