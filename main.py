import requests


def main():
    response = requests.get("http://api.sr.se/api/v2/traffic/messages?format=json")
    data = response.json()

    i = 0
    print(type(data))
    length = len(data["messages"])
    while i < length:
        print(data["messages"][i]["title"])
        i = i + 1


if __name__ == "__main__":
    main()
