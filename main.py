import json
import heapq
from models import RideRequest,Cab

destinations = ["Delhi","Jaipur"]
slots=["Morning","Afternoon","Evening","Night"]

queues={}
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
    trip=(destination,slot)
    if trip not in queues:
        queues[trip]=[]
    heapq.heappush(queues[trip],(-year,request))
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



def count_waiting():
    total=0
    for trip in queues:
        total+=len(queues[trip])
    return total




def get_open_cabs():
    open_cab=[]
    for cab in cabs:
        if not cab.left:
            open_cab.append(cab)
    return open_cab



def students_for(cab):
    queue=queues.get((cab.destination,cab.slot),[])
    ordered=[]
    for entry in sorted(queue):
        ordered.append(entry[-1])
    return ordered




def find_match():
    print("\n--- Seat preview ---")
    open_cabs = get_open_cabs()
    print(f"Open cabs: {len(open_cabs)}")

    for cab in open_cabs:
        picks = students_for(cab)[:cab.seats]
        print(f"\n{cab.driver}: {cab.destination}, {cab.slot} ({len(picks)}/{cab.seats})")
        for request in picks:
            print(f"  {request}")



def dispatch_cab():
    open_cabs=get_open_cabs()
    print(f"\nOpen cabs: {len(open_cabs)}")

    for number,cab in enumerate(open_cabs,start=1):
        print(f"  {number}. {cab}")

    choice=input("Which cab to leave?: ").strip()

    cab=None
    if choice.isdigit() and 1<=int(choice)<=len(open_cabs):
        cab=open_cabs[int(choice)-1]
    else:
        same_name=[]
        for open_cab in open_cabs:
            if open_cab.driver.lower()==choice.lower():
                same_name.append(open_cab)

        if len(same_name)==1:
            cab=same_name[0]
        elif len(same_name)>1:
            print("Error: more than one cab driver has that name")
            return

    if cab is None:
        print("Couldn't find that cab")
        return

    queue=queues.get((cab.destination,cab.slot),[])
    riders=[]
    while queue and len(riders)<cab.seats:
        entry=heapq.heappop(queue)
        riders.append(entry[-1])

    cab.passengers.extend(riders)
    cab.left=True

    print(f"\n{cab.driver} has left for {cab.destination} ({len(riders)}/{cab.seats})")
    for request in riders:
        print(f"  {request}")





def show_all():
    print(f"\n--- Waiting students ({count_waiting()}) ---")
    for trip in queues:
        for entry in sorted(queues[trip]):
            print(entry[-1])

    print(f"\n--- Cabs ({len(cabs)}) ---")
    for cab in cabs:
        print(cab)






def show_header():
    
    print("  CAB POOL MATCHER  ")
    print(f"  Waiting: {count_waiting()}    Open cabs: {len(get_open_cabs())}")


MENU = {
    "1": ("Add a ride request", add_request),
    "2": ("View waiting students and cabs", show_all),
    "3": ("Find matches", find_match),
    "4": ("Dispatch cab",dispatch_cab)
}






def main():
    cabs.extend(load_cabs("cabs.json"))
    while True:
        show_header()
        for key in MENU:
            label = MENU[key][0]
            print(f"  [{key}] {label}")
        print("  [0] Quit")

        choice = input(" ").strip()

        if choice == "0":
            print("Quitting application")
            break
        elif choice in MENU:
            action = MENU[choice][1]
            action()
        else:
            print("Type a valid option")


if __name__ == "__main__":
    main()