import requests as rq
from html.parser import HTMLParser
import re

from concurrent.futures import ThreadPoolExecutor
from clint.textui import progress, colored, puts

class LinkSuffixParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.is_h2: bool = False
        self.links: dict = {}
        self.last_header: str = None

    def handle_data(self, data):
            if self.is_h2 == True:
                self.last_header = ' '.join(data.split()[1:])
                self.links[self.last_header] = []
                self.is_h2 = False

    def handle_starttag(self, tag, attrs):
        lst: list = []
        if tag == 'h2':
            self.is_h2 = True

        elif tag == 'a':
            for attr in attrs:
                if 'href' in attr and attr[1].startswith("https://archive.org/"):
                    if 'DLC' in attr[1]:
                        k: str = f"{self.last_header} DLC"
                        if k not in self.links.keys():
                            self.links[k] = []
                        self.links[k].append(attr[1].split('/')[4])

                    else: self.links[self.last_header].append(attr[1].split('/')[4])

class GameLinkParser(HTMLParser):
    def __init__(self, console: str, base_link: str):
        HTMLParser.__init__(self)
        self.console: str = console
        self.base_link: str = base_link
        self.is_download_link: bool = False
        self.games: dict = {}
        self.last_link: str = None

    def handle_data(self, data):
        if self.is_download_link == True:
            self.games[f"[{self.console}] {data}"] = f"{self.base_link}/{self.last_link}"
            self.is_download_link = False

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if 'href' in attr and re.match(r"^.*(\.zip|\.rar|\.7z)", attr[1]):
                    self.last_link = attr[1]
                    self.is_download_link = True

def scrape_archive_links() -> dict:
    all_archive_links: dict = {}

    puts(colored.cyan("[*] Parsing archive.org links"))

    companies: list = ["microsoft", "sony", "nintendo", "sega", "misc"]
    for company in companies:
        link: str = f"https://r-roms.github.io/megathread/{company}/"
        body = rq.get(link).content.decode('utf-8')
        parser = LinkSuffixParser()
        parser.feed(body)

        all_archive_links.update(parser.links)

    return all_archive_links

def scrape_game_links() -> dict:
    links_suffixes: dict = scrape_archive_links()

    archive_dict: dict = {}
    pat : str = r"\">.*(\.zip|\.rar|\.7z)<"

    threads: list = []

    def threaded_scrape(console: str, suffix: str):
        link: str = f"https://archive.org/download/{suffix}"
        html: str = rq.get(link).content.decode("utf-8")
        parser = GameLinkParser(console, link)

        parser.feed(html)
        archive_dict.update(parser.games)

    puts(colored.cyan("[*] Getting games list"))
    with ThreadPoolExecutor(max_workers=55) as executor:
        for console, suffixes in links_suffixes.items():
                for suffix in suffixes:
                    threads.append(executor.submit(threaded_scrape, console, suffix))

    return archive_dict


def dl_file(url: str, filename: str, path: str):
    puts(colored.cyan("[*] Starting download"))
    r = rq.get(url, stream=True)
    with open(f"{path}/{filename}", 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024 ** 2), expected_size=(total_length/(1024 ** 2)) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()