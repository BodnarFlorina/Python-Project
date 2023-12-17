from urllib.request import urlopen
from html.parser import HTMLParser
from urllib.parse import urljoin
from collections import deque

class Parser(HTMLParser):
    def __init__(self, url, tag, visited_links):
        super().__init__()
        self.url = url
        self.tag = tag
        self.links = []
        self.visited_links = visited_links
        self.limit_links = 500
        self.queue = deque([url])
        self.get_links()

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and len(self.visited_links) < self.limit_links:
            for attr, value in attrs:
                if attr == 'href':
                    complete_url = urljoin(self.url, value)
                    if self.tag in complete_url and complete_url not in self.visited_links:
                        self.visited_links.append(complete_url)
                        self.links.append(complete_url)
                        self.queue.append(complete_url)

                        if len(self.visited_links) >= self.limit_links:
                            break

    def get_links(self):
        while self.queue and len(self.visited_links) < self.limit_links:
            url = self.queue.popleft()
            try:
                response = urlopen(url)
                html = response.read()
                # print(f"{html}")
                self.feed(html.decode('utf-8'))
            except Exception as e:
                print(f"Error fetching HTML for {url}: {e}")

    def print_links(self):
        print(f"Traseul parcurs de tool este:")
        for i, link in enumerate(self.visited_links):
            print(f"{i+1}. {link}")


if __name__ == "__main__":
    url = input("Introduceti link-ul paginii web: ")
    while True:
        try:
            urlopen(url)
            break
        except Exception as e:
            print(f"Error fetching HTML: {e}")
            url = input("Introduceti un link valid: ")

    tag = input("Introduceti tag-ul: ")

    # url = "https://docs.python.org/3/library/html.parser.html"
    # tag = "html.parser"

    visited_links = [url]

    parser = Parser(url, tag, visited_links)

    parser.print_links()
