import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Parser:
    def __init__(self, url, tag, visited_links, limit_links=500):
        self.url = url
        self.tag = tag
        self.visited_links = visited_links
        self.page_sizes = {}
        self.limit_links = limit_links
        self.queue = [url]
        self.get_links()

    def get_links(self):
        while self.queue and len(self.visited_links) < self.limit_links:
            url = self.queue.pop(0)
            try:
                size = self.get_page_size(url)
                self.page_sizes[url] = size

                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')

                for tag_a in soup.find_all('a', href=True):
                    complete_url = urljoin(url, tag_a['href'])
                    if (self.tag in tag_a or self.tag in complete_url) and complete_url not in self.visited_links:
                        self.visited_links.append(complete_url)
                        self.queue.append(complete_url)

                        size = self.get_page_size(complete_url)
                        self.page_sizes[complete_url] = size

                        if len(self.visited_links) >= self.limit_links:
                            break

                for associated_resource_tag in soup.find_all(['img', 'script', 'link', 'audio', 'video', 'object'], src=True):
                    resource_url = urljoin(url, associated_resource_tag['src'])
                    resource_response = requests.get(resource_url)
                    resource_size = len(resource_response.content)
                    self.page_sizes[url] += resource_size

            except requests.RequestException as e:
                print(f"Error fetching HTML for {url}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred for {url}: {e}")

    def get_page_size(self, url):
        try:
            response = requests.get(url)
            return len(response.content)
        except requests.RequestException as e:
            print(f"Error fetching HTML for {url}: {e}")
            return 0

    def print_links(self):
        print(f"Traseul parcurs de tool este:")
        for i, link in enumerate(self.visited_links):
            size = self.page_sizes.get(link)
            print(f"{i+1}. {link} - Dimensiune: {size} bytes")


def get_limit_links():
    while True:
        try:
            limit = int(input("Introduceti limita de link-uri (implicit 500): "))
            if limit > 0:
                return limit
            else:
                print("Limita trebuie sa fie un numar intreg pozitiv...")
        except ValueError:
            print("Introduceti un numar intreg valid...")


if __name__ == "__main__":
    url = input("Introduceti link-ul paginii web: ")
    while True:
        try:
            requests.get(url).raise_for_status()
            break
        except requests.RequestException as e:
            print(f"Error fetching HTML: {e}")
            url = input("Introduceti un link valid: ")

    tag = input("Introduceti tag-ul: ")

    limit_links = get_limit_links()

    visited_links = [url]

    parser = Parser(url, tag, visited_links, limit_links)

    parser.print_links()
