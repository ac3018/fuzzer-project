"""
Fuzzer Project
SWEN 331
Alan Chen(ac3018)

This file is responsible for returning all cookies of a browser
"""


def get_cookies(browser):
    for cookie in browser.get_cookiejar():
        print(cookie)