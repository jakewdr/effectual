import requests
import file2


def main():
    print("Hello World")
    response = requests.get("https://httpbin.org/ip")
    print("Your IP is {0}".format(response.json()["origin"]))
    file2.test()


if __name__ == "__main__":
    main()
