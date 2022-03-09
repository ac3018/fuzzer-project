"""
Fuzzer Project
SWEN 331
Alan Chen(ac3018)
"""
import mechanicalsoup

import cookies
import link_crawling
import page_guessing
import parse_forms
import parsing_urls


def discover(args):
    browser = mechanicalsoup.StatefulBrowser(raise_on_404=True)
    if args.custom_auth is not None:
        setup = args.url + "/setup.php"
        security = args.url + "/security.php"

        # Navigating to {URL}/setup.php and creating/resetting DB

        browser.open(setup)
        browser.select_form()
        browser.submit_selected()

        # Navigating to login page
        browser.open(args.url)
        browser.select_form()

        # Logging in with admin and password
        browser["username"] = "admin"
        browser["password"] = "password"
        browser.submit_selected()

        # Changing security level to low
        browser.open(security)
        browser.select_form()
        browser["security"] = "low"
        print("Changing security to low")
        browser.submit_selected()

    else:
        print("No input found for custom-auth.")

    print("\n*** Page Guessing ***\n")
    guessed_pages = page_guessing.guess(args, browser)

    print("\n*** Link Crawling ***\n")
    discovered_links = link_crawling.crawl(args, browser)
    final_urls = discovered_links.union(guessed_pages)

    print("\n*** Parse URLs ***\n")
    print("Parsed URLs: ")
    for url in final_urls:
        print(url)
    param_dict = parsing_urls.parse(final_urls)

    print("\n*** Form Inputs ***\n")
    form_dict = parse_forms.parse(final_urls, browser)

    print("\n*** Cookies ***\n")
    cookies.get_cookies(browser)

    return param_dict, form_dict, browser