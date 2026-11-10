import json
from models import RideRequest,Cab

destinations = ["Delhi","Jaipur"]
slots=["Morning","Afternoon","Evening","Night"]

waiting=[]
cabs=[]


def ask_name():
    while True:
        name=input("Name: ").strip()
        while not name:
            print("Name cannot be empty")
            name=input("Name: ").strip()
        return name



def ask_choice(prompt,options):
    while True:
        answer=input(prompt).strip().capitalize()
        if answer in options:
            return answer
        else:
            print(f"Please pick a valid option")

def ask_year():
    while True:
        answer=input("Year(1-5): ").strip()
        try:
            year=int(answer)
            if year<1 or year>5:
                raise ValueError
            return year
        except ValueError:
            print("Please pick a valid number")


def add_request():
    print("\n New ride request ")
    name = ask_name()
    destination = ask_choice("Destination (Delhi/Jaipur): ", destinations)
    slot = ask_choice("Time slot (Morning/Afternoon/Evening/Night): ", slots)
    year = ask_year()   

    request = RideRequest(name, destination, slot, year)
    waiting.append(request)
    print(f"Added: {request}")




def load_cabs(filename):
    try:
        with open(filename) as file:
            data=json.load(file)
    except FileNotFoundError or json.JSONDecodeError:
        print(f"No cabs found")
        return []

    loaded=[]
    for item in data:
        try:
            cab=Cab(item["driver"], int(item["seats"]), item["destination"], item["slot"])
        except (KeyError, ValueError, TypeError):
            print(f"Skipping a cab")
            continue    

        loaded.append(cab)
    return loaded




def show_all():
    print(f"\n--- Waiting students ({len(waiting)}) ---")
    for request in waiting:
        print(request)

    print(f"\n--- Cabs ({len(cabs)}) ---")
    for cab in cabs:
        print(cab)


def show_header():
    open_cabs = 0
    for cab in cabs:
        if not cab.departed:
            open_cabs += 1

    print("  CAB POOL MATCHER  ")
    print(f"  Waiting: {len(waiting)}    Open cabs: {open_cabs}")


MENU = {
    "1": ("Add a ride request", add_request),
    "2": ("View waiting students and cabs", show_all),
}


def main():
    cabs.extend(load_cabs("cabs.json"))
    while True:
        show_header()
        for key in MENU:
            label = MENU[key][0]
            print(f"  [{key}] {label}")
        print("  [3] Quit")

        choice = input(" ").strip()

        if choice == "3":
            print("Quitting application")
            break
        elif choice in MENU:
            action = MENU[choice][1]
            action()
        else:
            print("Type a valid option")


if __name__ == "__main__":
    main()