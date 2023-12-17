from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser
from urllib.parse import urljoin


class Parser(HTMLParser):
    def __init__(self, url, tag, visited_links, limit_links=500):
        super().__init__()
        self.url = url
        self.tag = tag
        self.links = []
        self.visited_links = visited_links
        self.limit_links = limit_links
        self.queue = [url]
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
            url = self.queue.pop(0)
            try:
                request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urlopen(request)
                html = response.read()
                # print(f"{html}")
                self.feed(html.decode('utf-8'))
            except HTTPError as e:
                print(f"HTTPError fetching HTML for {url}: {e}")
            except URLError as e:
                print(f"URLError fetching HTML for {url}: {e}")
            except Exception as e:
                print(f"Error fetching HTML for {url}: {e}")

    def print_links(self):
        print(f"Traseul parcurs de tool este:")
        for i, link in enumerate(self.visited_links):
            print(f"{i+1}. {link}")


def get_limit_links():
    while True:
        try:
            limit = int(input("Introduceti limita de link-uri (implicit 500): "))
            if limit > 0:
                return limit
            else:
                print("Limita trebuie sa fie un numar intreg pozitiv...")
        except ValueError:
            print("Introduceti un numar intreg valid.")


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

    limit_links = get_limit_links()

    visited_links = [url]

    parser = Parser(url, tag, visited_links, limit_links)

    parser.print_links()

    # url = "https://docs.python.org/3/library/html.parser.html"
    # tag = "html.parser"
