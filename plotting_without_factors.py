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
def simulate(places, n_healthy, n_sick, iterations,
             social_distancing_factor, vaccination_factor, travel_rate):
    

    town = [Place(i) for i in range(places)] #creating a list of cmn_places
    people = [Person('healthy', travel_rate) for _ in range(n_healthy)] + \
             [Person('sick', travel_rate) for _ in range(n_sick)]

    vaccinated_count = int((n_healthy + n_sick) * vaccination_factor)
    for i in range(vaccinated_count):
        people[i].vaccination = True #gives the number of people vaccinated

    healthy_history = [n_healthy]
    sick_history = [n_sick]
    recovered_history = [0]
    dead_history = [0]
    days = [day for day in range(iterations)] #initialising the lists to stor data

    for day in days:
        healthy = 0
        sick = 0
        recovered = 0
        dead = 0

        for person in people:
            person.cmn_place = town[randint(0, len(town) - 1)] #aasigning a random cmn_placein the town for each persons

        for person in people:
            if person.status == 'healthy':
                healthy += 1
            elif person.status == 'sick':
                sick += 1
                person.cmn_place.num_sick += 1
            elif person.status == 'recovered':
                recovered += 1
            else:
                dead += 1 #updating the list

        for person in people:
            if person.status == 'sick' and person.time_sick < 15:
                person.time_sick += 1
            elif person.status == 'sick' and person.time_sick == 15:
                if randint(0, 9) == 4:
                    person.status = 'dead'
                else:
                    person.status = 'recovered'
            if person.status == 'healthy' and not person.vaccination:
                x = person.cmn_place.num_sick
                y = social_distancing_factor
                chance_of_infection = 0.0008 * x * (1 - y)
                if random() < chance_of_infection:
                    person.status = 'sick'

        for cmn_place in town:
            cmn_place.num_sick = 0

        healthy_history.append(healthy)
        sick_history.append(sick)
        recovered_history.append(recovered)
        dead_history.append(dead)
        


