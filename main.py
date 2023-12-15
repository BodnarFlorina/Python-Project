from urllib.request import urlopen
from html.parser import HTMLParser
from urllib.parse import urljoin


class Parser(HTMLParser):
    def __init__(self, url, tag, visited_links):
        super().__init__()
        self.url = url
        self.tag = tag
        self.links = []
        self.visited_links = visited_links
        self.get_links()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    complete_url = urljoin(self.url, value)
                    if self.tag in complete_url and complete_url not in self.visited_links:
                        print(complete_url)
                        self.visited_links.append(complete_url)
                        self.links.append(complete_url)
                        parser = Parser(complete_url, self.tag, self.visited_links)

    def get_links(self):
        try:
            response = urlopen(self.url)
            html = response.read()
            # print(f"{html}")
            self.feed(html.decode('utf-8'))
        except Exception as e:
            print(f"Error fetching HTML: {e}")

    def print_links(self):
        print(f"Traseul parcurs de tool este:")
        for i, link in enumerate(self.visited_links):
            print(f"{i+1}. {link}")


if __name__ == "__main__":
    url = "https://docs.python.org/3/library/html.parser.html"
    tag = "html.parser"

    visited_links = [url]

    parser = Parser(url, tag, visited_links)

    # links = parser.links
    # for link in links:
    #     print(link)

    parser.print_links()

