import requests
import file2
import sys
import os


def main() -> None:
    print("Hello World")
    bundleCheck()
    url: str = "https://httpbin.org/ip"
    response = requests.get(url)  # Using requests from the bundle!
    print("Your IP is {0}".format(response.json()["origin"]))
    file2.test()  # Example of using a local file


def bundleCheck() -> None:
    scriptPath: str = str(
        os.path.realpath(__file__).replace(os.sep, "/")
    )  # Gets the path of the current running python script and makes sure forward-slashes are used

    if "bundle.py" in scriptPath:
        print("Running in bundle!")
    else:
        print("Running in developer mode!")


def versionCheck() -> None:
    if sys.version_info[0] != 3 and sys.version_info[1] != 11:
        raise EnvironmentError("This bundle was made for python version 3.11!")


if __name__ == "__main__":
    main()
