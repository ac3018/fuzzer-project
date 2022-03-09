"""
Fuzzer Project
SWEN 331
Alan Chen(ac3018)

This file is responsible for parsing urls from guessed and discovered pages
"""


def parse(urls):
    param_dict = dict()
    for url in urls:
        base, url_params = parse_url(url)
        param_dict[base] = url_params
    return param_dict


def parse_url(url):
    url_params = dict()
    sub_divide = url.split('?')

    if len(sub_divide) > 1:
        if "#" in sub_divide[1]:
            params = sub_divide[1].split("#")
            url_parameters = params[0].split("&")
        else:
            url_parameters = sub_divide[1].split("&")

        for key_val in url_parameters:
            if len(key_val.split("=")) == 2:
                key, val = key_val.split("=")
                url_params[key] = val
                print("URL: " + url + "; Parameter: " + key + "; Value: " + val)

    return sub_divide[0], url_params
