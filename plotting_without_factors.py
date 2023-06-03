from random import randint, random
from matplotlib import pyplot as plt


class Person:
    def __init__(self, status, travel_rate):
        self.status = status
        self.time_sick = 0
        self.cmn_place = []
        self.travel_rate = travel_rate
        self.vaccination = False


class Place:
    def __init__(self, cmn_place_id):
        self.cmn_place_id = id
        self.num_sick = 0
def simulate(places, n_healthy, n_sick, iterations,social_distancing_factor , vaccination_factor):
    town = [Place(i) for i in range(places)]
    people = [Person('healthy', 0) for i in range(n_healthy)] + \
             [Person('sick', 0) for i in range(n_sick)]

    vaccinated_count = int((n_healthy + n_sick) * vaccination_factor)
    for i in range(vaccinated_count):
        people[i].vaccination = True

    healthy_history = [n_healthy]
    sick_history = [n_sick]
    recovered_history = [0]
    dead_history = [0]
    days = [day for day in range(iterations)]




