from urllib.request import urlopen
from html.parser import HTMLParser
from urllib.parse import urljoin


class Parser(HTMLParser):
    def __init__(self, url, tag):
        super().__init__()
        self.url = url
        self.tag = tag
        self.links = []
        self.get_links()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    complete_url = urljoin(self.url, value)
                    self.links.append(complete_url)

    def get_links(self):
        try:
            response = urlopen(self.url)
            html = response.read()
            print(f"{html}")
            self.feed(html.decode('utf-8'))
        except Exception as e:
            print(f"Error fetching HTML: {e}")


if __name__ == "__main__":
    url = "https://docs.python.org/3/library/html.parser.html"
    tag = ""

    parser = Parser(url, tag)

    links = parser.links
    for link in links:
        print(link)

