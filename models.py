from datetime import datetime

class RideRequest:
    def __init__(self,name,destination,slot,year,order):
        self.name=name
        self.destination=destination
        self.slot=slot
        self.year=year
        self.request_time=datetime.now()
        self.order=order

    def __str__(self):
        return f"{self.name} (Year {self.year}) going to {self.destination}, {self.slot}"


class Cab:
    def __init__(self,driver,seats,destination,slot):
        self.driver=driver
        self.seats=seats
        self.left=False
        self.destination=destination
        self.slot=slot
        self.passengers=[]

    def __str__(self):
        status="Left" if self.left else "Available"
        return f"{self.driver} | {self.destination}, {self.slot} | {len(self.passengers)}/{self.seats} seats taken | {status}"