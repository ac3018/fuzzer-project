"""
Fuzzer Project
SWEN 331
Alan Chen(ac3018)

This file is responsible for discovering inputs as form parameters
"""


def parse(urls, browser):
    forms = {}
    for url in urls:
        browser.open(url)
        forms[url] = browser.page.find_all("form")
        for form in forms[url]:
            print("Form inputs for page: " + url)
            print("Form method: " + form["method"])
            for tag in browser.select_form(form).form.descendants:
                if tag.name == "input":
                    print()
                    if "name" in tag.attrs:
                        print("Tag name: " + tag["name"])
                    if "value" in tag.attrs:
                        print("Tag value: " + tag["value"])
    return forms
