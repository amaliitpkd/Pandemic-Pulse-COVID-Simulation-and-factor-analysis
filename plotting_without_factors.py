from random import randint, random
from matplotlib import pyplot as plt


class Person:
    def __init__(self, status, travel_rate):
        self.status = status
        self.time_sick = 0
        self.cmn_place = []
        self.travel_rate = travel_rate
        self.vaccination = False


