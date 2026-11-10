from models import RideRequest

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



def show_all():
    print("\n Waiting students ")
    for request in waiting:
        print(request)

    print(" Cabs ")
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