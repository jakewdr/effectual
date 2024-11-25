import sys

import requests

import file2


def main() -> None:
    versionCheck()
    print("Hello World")
    url: str = "https://httpbin.org/ip"
    response = requests.get(url)  # Using requests from the bundle!
    print("Your IP is {0}".format(response.json()["origin"]))
    file2.test()  # Example of using a local file


def versionCheck() -> None:
    if sys.version_info[0] != 3 and sys.version_info[1] != 11:
        raise EnvironmentError("This bundle was made for python version 3.11!")


if __name__ == "__main__":
    main()
