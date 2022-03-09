"""
Fuzzer Project
SWEN 331
Alan Chen(ac3018)

This file is responsible for guessing potentially unlinked pages
"""


def guess(args, browser):
    guessed_pages = set()
    browser.open(args.url)
    print("Guessed pages: ")
    # Read words into list
    with open(args.common_words, 'r') as f:
        words = f.read().split()

    # If no extensions.txt was passed
    if not args.extensions:
        ext = ".php"
        for word in words:
            page = args.url + "/" + word + ext
            try:
                browser.open(page)
            except:
                continue
            else:
                guessed_pages.add(page)
                print(page)

    else:
        with open(args.extensions, 'r') as f:
            extensions = f.read().split()

        for word in words:
            for extension in extensions:
                page = args.url + "/" + word + extension
                try:
                    browser.open(page)
                except:
                    continue
                else:
                    guessed_pages.add(page)
                    print(page)

    return guessed_pages
