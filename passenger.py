#import random
from enum import Enum, auto

class PassengerState(Enum):
    walking = auto()
    waiting = auto()
    boarding = auto()
    checking_in = auto()
    settling = auto()


class Passenger:
    def __init__(self, name, age, ticket_number, boarding_group):
        self.name = name
        self.age = age
        self.ticket_number = ticket_number
        self.family_members = []
        self.boarding_group = boarding_group

    def __str__(self):
        return f"Passenger Name: {self.name}, Age: {self.age}, Ticket Number: {self.ticket_number}, Boarding Group: {self.boarding_group}"

#bob = Passenger("Bob Smith", 30, "A12345", random.randint(1, 5))
#print(bob)  # Output: Passenger Name: Bob Smith, Age: 30, Ticket Number: A12345