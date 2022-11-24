import requests
import datetime
import re

# One request to save SR some computing power
response = requests.get("https://api.sr.se/api/v2/channels/?format=json&pagination=false")
channel_list = response.json()


def display_channels():
    i = 0
    length_of_schedule = len(channel_list["channels"])
    while i < length_of_schedule:  # Displays all the channels
        print("   ", f"[{i + 1}: ", channel_list["channels"][i]["name"], "]", end="")
        if i % 9 == 0:
            print("\n")
        i += 1

    print("\n")
    user_input = input("Pick a channel: ")
    print("\n")
    if user_input.isnumeric() & 0 <= int(user_input) - 1 <= 51:
        display_schedule(int(user_input) - 1)

    print(f"{user_input} is not a valid channel!\n")
    display_channels()


def display_schedule(user_input):
    print(channel_list["channels"][user_input]["tagline"])
    print("Here is the link to the Radio!")
    print(channel_list["channels"][user_input]["siteurl"])
    schedule_url = channel_list["channels"][user_input]["id"]

    # requests with get the schedule with the id
    schedule_response = requests.get(
        f"https://api.sr.se/v2/scheduledepisodes?channelid={schedule_url}&format=json&pagination=false")
    schedule = schedule_response.json()

    length_of_schedule = len(schedule["schedule"])
    print("\n")
    i = 0
    current_program = 0
    while i < length_of_schedule:  # Prints the rest of the days programs
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
    user_input = input("Click enter to return or exit to close the program: ")
    if user_input != "exit":
        print("\n")
        display_channels()


if __name__ == "__main__":
    display_channels()
