"""
Fuzzer Project
SWEN 331
Alan Chen(ac3018)
"""

import argparse
import sys
import discover
import test


def main():
    # Parsing command line arguments
    # Will add more commands Part 2
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("--custom-auth", type=str,
                               help="Signal that the fuzzer should use hard-coded authentication for a specific "
                                    "application (e.g. dvwa).")
    parent_parser.add_argument("url", help="the url of the website")

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="Commands", description="Commands the app can run", dest="command")

    discover_parser = subparsers.add_parser("discover", parents=[parent_parser])
    discover_parser.add_argument("--common-words", type=str,
                        help="Newline-delimited file of common words to be used in page guessing. Required.", required=True)
    discover_parser.add_argument("--extensions", type=str,
                        help='Newline-delimited file of path extensions, e.g. ".php".'
                             + 'Optional. Defaults to ".php" and the empty string if not specified')

    test_parser = subparsers.add_parser("test", parents=[parent_parser])
    test_parser.add_argument("--common-words", type=str, help="Newline-delimited file of common words to be used in page guessing. Required.", required=True)
    test_parser.add_argument("--extensions", type=str, help='Newline-delimited file of path extensions, e.g. ".php".'
                             + 'Optional. Defaults to ".php" and the empty string if not specified')
    test_parser.add_argument("--vectors", type=str, help="Newline-delimited file of common exploits to vulnerabilities. Required.", required=True)
    test_parser.add_argument("--sanitized-chars", type=str, help="Newline-delimited file of characters that should be sanitized from inputs. Defaults to just < and >")
    test_parser.add_argument("--sensitive", type=str, help="Newline-delimited file data that should never be leaked. It's assumed that this data is in the application's database (e.g. test data), but is not reported in any response. Required.", required=True)
    test_parser.add_argument("--slow", type=int, default=500, help='Number of milliseconds considered when a response is considered "slow". Optional. Default is 500 milliseconds')

    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        if args.command == "discover":
            discover.discover(args)
        elif args.command == "test":
            param_dict, form_dict, browser = discover.discover(args)
            test.test(param_dict, form_dict, args)


if __name__ == '__main__':
    main()
