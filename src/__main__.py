import requests
import file2


def main():
    print("Hello World")
    response = requests.get("https://httpbin.org/ip")  # Using requests from the bundle!
    print("Your IP is {0}".format(response.json()["origin"]))
    file2.test()  # Example of using a local file


if __name__ == "__main__":
    main()
