from random import randint, random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

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
    if not 0 <= social_distancing_factor <= 1:
        raise ValueError("Social distancing factor must be between 0 and 1.")
    if not 0 <= vaccination_factor <= 1:
        raise ValueError("Vaccination factor must be between 0 and 1.")
    if not 0 <= travel_rate <= 1:
        raise ValueError("Travel rate must be between 0 and 1.")

    town = [Place(i) for i in range(places)]
    people = [Person('healthy', travel_rate) for _ in range(n_healthy)] + \
            [Person('sick', travel_rate) for _ in range(n_sick)]

    vaccinated_count = int((n_healthy + n_sick) * vaccination_factor)
    for i in range(vaccinated_count):
        people[i].vaccination = True

    healthy_history = [n_healthy]
    sick_history = [n_sick]
    recovered_history = [0]
    dead_history = [0]
    days = [day for day in range(iterations)]

    for day in days:
        healthy = 0
        sick = 0
        recovered = 0
        dead = 0

        for person in people:
            person.cmn_place = town[randint(0, len(town) - 1)]

        for person in people:
            if person.status == 'healthy':
                healthy += 1
            elif person.status == 'sick':
                sick += 1
                person.cmn_place.num_sick += 1
            elif person.status == 'recovered':
                recovered += 1
            else:
                dead += 1

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

    return days, healthy_history, sick_history, recovered_history, dead_history


# Set the initial parameters
places = 75
n_healthy = 25000
n_sick = 25
iterations = 100
initial_social_distancing = 0
initial_vaccination = 0
initial_travel_rate = 0

# Create the figure and subplots
fig, axs = plt.subplots(3, sharex=True, sharey=False)
fig.suptitle('VIRUS SIMULATION')

# Set the initial data
days, healthy_history, sick_history, recovered_history, dead_history = simulate(
    places, n_healthy, n_sick, iterations, initial_social_distancing, initial_vaccination, initial_travel_rate
)

# Plot the initial data
axs[0].plot(days, healthy_history[:-1])
axs[0].set_title('HEALTHY')
axs[1].plot(days, sick_history[:-1], 'tab:orange')
axs[1].set_title('SICK')
axs[2].plot(days, recovered_history[:-1], 'tab:green')
axs[2].set_title('RECOVERED')
axs[3].plot(days, dead_history[:-1], 'tab:red')
axs[3].set_title('DEAD')

# Creating  the sliders for factors
slider_ax_social_distancing = plt.axes([0.2, 0.070, 0.65, 0.01])
slider_ax_vaccination = plt.axes([0.2, 0.035, 0.65, 0.01])
slider_ax_travel_rate = plt.axes([0.2, 0.0, 0.65, 0.01])

slider_social_distancing = Slider(slider_ax_social_distancing, 'Social Distancing', 0, 1, valinit=initial_social_distancing)
slider_vaccination = Slider(slider_ax_vaccination, 'Vaccination', 0, 1, valinit=initial_vaccination)
slider_travel_rate = Slider(slider_ax_travel_rate, 'Travel Rate', 0, 1, valinit=initial_travel_rate)

def update_plot(val):
    social_distancing = slider_social_distancing.val
    vaccination = slider_vaccination.val
    travel_rate = slider_travel_rate.val

    days, healthy_history, sick_history, recovered_history, dead_history = simulate(
        places, n_healthy, n_sick, iterations, social_distancing, vaccination, travel_rate
    )

    # Update the plot
    axs[0].cla()
    axs[0].plot(days, healthy_history[:-1])
    axs[0].set_title('HEALTHY')

    axs[1].cla()
    axs[1].plot(days, sick_history[:-1], 'tab:orange')
    axs[1].set_title('SICK')

    axs[2].cla()
    axs[2].plot(days, recovered_history[:-1], 'tab:green')
    axs[2].set_title('RECOVERED')

    #axs[3].cla()
    #axs[3].plot(days, dead_history[:-1], 'tab:red')
    #axs[3].set_title('DEAD')

    # Redraw the canvas
    fig.canvas.draw()

# Connect the update_plot function to the slider events
slider_social_distancing.on_changed(update_plot)
slider_vaccination.on_changed(update_plot)
slider_travel_rate.on_changed(update_plot)

plt.show()


        


