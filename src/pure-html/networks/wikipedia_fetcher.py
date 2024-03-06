import requests

from pathlib import Path

from utils.logger import logger
from parsers.webpage_content_extractor import WebpageContentExtractor


class WikipediaFetcher:
    def __init__(self, lang="en"):
        self.lang = lang
        self.url_head = "https://en.wikipedia.org/wiki/"
        self.output_folder = Path(__file__).parents[1] / "data" / "wikipedia"

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

    def fetch(self, title, overwrite=False, to_markdown=True):
        logger.note(f"> Fetching from Wikipedia: [{title}]")
        self.html_path = self.output_folder / f"{title}.html"

        if not overwrite and self.html_path.exists():
            logger.mesg(f"  > HTML exists: {self.html_path}")
            with open(self.html_path, "r", encoding="utf-8") as rf:
                self.html_str = rf.read()
        else:
            self.url = self.url_head + title
            req = requests.get(self.url, headers=self.headers)
            status_code = req.status_code
            if status_code == 200:
                logger.file(f"  - [{status_code}] {self.url}")
                self.html_str = req.text
                self.output_folder.mkdir(parents=True, exist_ok=True)
                with open(self.html_path, "w", encoding="utf-8") as wf:
                    wf.write(self.html_str)
                logger.success(f"  > HTML Saved at: {self.html_path}")
            else:
                if status_code == 404:
                    logger.err(f"{status_code} - Page not found : [{title}]")
                else:
                    logger.err(f"{status_code} Error")
                return (None, None)

        if to_markdown:
            return self.to_markdown(overwrite=overwrite)
        else:
            return (self.html_path, self.html_str)

    def to_markdown(self, overwrite=False):
        self.markdown_path = self.html_path.with_suffix(".md")

        if not overwrite and self.markdown_path.exists():
            logger.mesg(f"  > Markdown exists: {self.markdown_path}")
            with open(self.markdown_path, "r", encoding="utf-8") as rf:
                self.markdown_str = rf.read()
        else:
            webpage_content_extractor = WebpageContentExtractor()
            self.markdown_str = webpage_content_extractor.extract(self.html_path)
            with open(self.markdown_path, "w", encoding="utf-8") as wf:
                wf.write(self.markdown_str)
            logger.success(f"  > Mardown saved at: {self.markdown_path}")

        return (self.markdown_path, self.markdown_str)


if __name__ == "__main__":
    fetcher = WikipediaFetcher()
    title = "R._Daneel_Olivaw"
    path, content = fetcher.fetch(title, overwrite=True)

    logger.file(f"> [{path}]:")
    logger.line(content)

    # python -m networks.wikipedia_fetcher
