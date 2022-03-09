"""
Fuzzer Project
SWEN 331
Alan Chen(ac3018)
"""
import mechanicalsoup


def test(param_dict, form_dict, args):
    vectors = open(args.vectors).readlines()
    browser = mechanicalsoup.Browser()
    f = open(args.sensitive, 'r')
    sensitive_words = f.read().split()

    print("\n*** Testing Vectors Against Forms ***\n")
    test_forms(form_dict, vectors, browser, args.slow, sensitive_words)

    print("\n*** Testing Vectors Against URL Parameters ***\n")
    test_url_param(param_dict, vectors, browser, args.slow, sensitive_words)


def get_status_code(code):
    if code == 200:
        return "200 --> Successful (OK)"
    if code == 303:
        return "303 --> Redirection (See Other)"
    if code == 400:
        return "400 --> Client Error (Bad Request)"
    if code == 401:
        return "401 --> Client Error (Unauthorized)"
    if code == 403:
        return "403 --> Client Error (Forbidden)"
    if code == 404:
        return "404 --> Client Error (Not Found)"
    if code >= 500:
        return code.__str__() + " --> Server Error"
    else:
        return code.__str__() + " --> Unknown Code"


def analyze_response_time(response, timeout):
    load_time = response.elapsed.total_seconds() * 1000
    if load_time > timeout:
        print("Response took " + load_time.__str__() + " ms; Potential Denial Of Service Vulnerability")


def analyze_status_code(response):
    print("Return code: " + get_status_code(response.status_code))


def analyze_sensitive_data(response, sensitive_words):
    for sensitive_word in sensitive_words:
        if sensitive_word in response.text:
            print("Response contained the following sensitive word: " + sensitive_word)


def analyze_sanitization(response, vector):
    if '&lt' in vector and '&gt' in vector:
        if vector in response.text:
            print("The following vector wasn't sanitized correctly: " + vector)
            print("This page may be vulnerable to cross site scripting")


def test_forms(form_dict, vectors, browser, timeout, sensitive_words):

    name = ""
    form_keys = list(form_dict.keys())

    # for each url & corresponding form list
    for url in form_keys:
        print("Testing forms on: " + url + "\n")
        forms = form_dict[url]

        # for each form
        for form in forms:
            form_method = str(form['method']).lower()

            for vector in vectors:
                inputs = form.find_all('input')

                print("Testing Vector: " + vector.__str__())

                # dict of inputs -> vectors
                request_params = {}

                for inp in inputs:
                    if 'name' in inp.attrs:
                        name = inp['name']
                    elif 'type' in inp.attrs:
                        name = inp['type']

                    if name.lower().strip() == 'submit':
                        request_params[name] = "Submit"
                    else:
                        request_params[name] = vector.rstrip()
                if form_method == "post":

                    post_response = browser.post(url, data=request_params)

                    analyze_response_time(post_response, timeout)
                    analyze_status_code(post_response)
                    analyze_sensitive_data(post_response, sensitive_words)
                    analyze_sanitization(post_response, vector)
                elif form_method == "get":
                    get_response = browser.get(url, data=request_params)

                    analyze_response_time(get_response, timeout)
                    analyze_status_code(get_response)
                    analyze_sensitive_data(get_response, sensitive_words)
                    analyze_sanitization(get_response, vector)
                print("")
        print("")


def test_url_param(param_dict, vectors, browser, timeout, sensitive_words):
    key_list = list(param_dict.keys())

    # for each url & corresponding param dict
    for url in key_list:
        print("Testing url parameters on: " + url)
        curr_param_d = param_dict[url]
        parameters = curr_param_d.keys()  # ignore values
        request_param_d = {}

        for vector in vectors:
            for param in parameters:
                request_param_d[param] = vector

                response = browser.get(url, params=request_param_d)
                analyze_response_time(response, timeout)
                analyze_status_code(response)
                analyze_sensitive_data(response, sensitive_words)
                analyze_sanitization(response, vector)