"""
Fuzzer Project
SWEN 331
Alan Chen(ac3018)

This file is responsible for crawling all visible links within a webpage
"""
from urllib.parse import urljoin


def crawl(args, browser):

    print("Discovered links: ")

    discovered_links = set()
    unvisited_urls = set()

    unvisited_urls.add(args.url + "/")
    discovered_links.add(args.url + "/")
    while len(unvisited_urls) > 0:
        curr_url = unvisited_urls.pop()

        if "logout" not in curr_url and "pdf" not in curr_url:
            browser.open(curr_url)
            all_links = browser.links()
            for link in all_links:

                curr_link = urljoin(curr_url, link.get("href"))

                if (curr_link not in discovered_links) and (args.url in curr_link) and (
                        "logout" not in curr_link) and ("pdf" not in curr_link):
                    try:
                        browser.open(curr_link)
                        unvisited_urls.add(curr_link)
                        discovered_links.add(curr_link)
                    except:
                        continue

    for links in discovered_links:
        print(links)
    return discovered_links
