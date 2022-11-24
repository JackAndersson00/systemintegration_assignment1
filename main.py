import requests
import datetime
import re


def main():
    running = True
    while running:
        response = requests.get("https://api.sr.se/api/v2/channels/?format=json&pagination=false")
        first_page = response.json()

        i = 0
        length = len(first_page["channels"])
        while i < length:  # Displays all the channels
            print("  | ", f"{i}: ", first_page["channels"][i]["name"], end="")
            if i % 7 == 0:
                print("\n")
            i += 1

        print("\n")
        in_num = input("Pick a program or write stop to exit: ")
        print("\n")
        if in_num == "stop":
            break
            # Takes the users chosen channel and gets its description and schedule
        print(first_page["channels"][int(in_num)]["tagline"])
        print(first_page["channels"][int(in_num)]["siteurl"])
        schedule_url_dict = first_page["channels"][int(in_num)]["id"]

        # requests with get the schedule with the id
        schedule_response = requests.get(
            f"https://api.sr.se/v2/scheduledepisodes?channelid={schedule_url_dict}&format=json&pagination=false")
        schedule = schedule_response.json()

        length = len(schedule["schedule"])
        print("\n")
        i = 0
        current_program = 0
        while i < length:  # Prints the rest of the days programs
            end = schedule["schedule"][i]["endtimeutc"]
            end = re.sub(r"\D", "", end)
            end_time = datetime.datetime.fromtimestamp(int(end) / 1000)
            if end_time >= datetime.datetime.now():
                if current_program == 0:
                    print("Currently running: ", end="")
                    current_program += 1
                start = schedule["schedule"][i]["starttimeutc"]
                start = re.sub(r"\D", "", start)
                start_time = datetime.datetime.fromtimestamp(int(start) / 1000)
                print(schedule["schedule"][i]["title"], end="  |  ")
                print(start_time.strftime("%H:%M"), end="")
                print(" -", end_time.strftime("%H:%M"))
                print(schedule["schedule"][i]["description"], "\n")
            i += 1
        input("Click enter to return ")


if __name__ == "__main__":
    main()
