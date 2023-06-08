# pep8 format
def covid():
    # importing necessary labraries
    from random import randint, random
    import matplotlib.pyplot as plt
    # from matplotlib.animation import FuncAnimation
    from matplotlib.widgets import Slider

    class Person:
        # creating a class person and initialising attributes
        def __init__(self, status, travel_restri):
            self.status = status
            self.time_sick = 0
            self.cmn_place = []
            self.travel_restri = travel_restri
            self.vaccination = False

    class Place:
        # creating a class place and initialising attributes
        def __init__(self, cmn_place_id):
            self.cmn_place_id = id
            self.num_sick = 0

    def simulate(places, n_healthy, n_sick, time_frame,
                 social_distancing_factor,
                 vaccination_factor, travel_restri):
        # introducing various factors affecting the epidemic spread
        if not 0 <= social_distancing_factor <= 1:
            raise ValueError(
                "Social distancing factor must be between 0 and 1."
                )  # error handling
        if not 0 <= vaccination_factor <= 1:
            raise ValueError("Vaccination factor must be between 0 and 1.")
        if not 0 <= travel_restri <= 1:
            raise ValueError("Travel rate must be between 0 and 1.")

        town = [Place(i) for i in range(places)]
        # introducing list of cmn_places
        people = [Person('healthy',
                         travel_restri) for _ in range(n_healthy)] + \
            [Person('sick', travel_restri) for _ in range(n_sick)]

        vaccinated_count = int((n_healthy + n_sick) * vaccination_factor)
        # for updating the num_of_people vaccinated
        for i in range(vaccinated_count):
            people[i].vaccination = True

        healthy_history = [n_healthy]
        # initialising lists for various attributes
        sick_history = [n_sick]
        recovered_history = [0]
        dead_history = [0]
        days = [day for day in range(time_frame)]

        for day in days:
            # intialising values of various parameters
            healthy = 0
            sick = 0
            recovered = 0
            dead = 0

            for person in people:
                person.cmn_place = town[randint(0, len(town) - 1)]

            for person in people:
                '''updating the attributes
                   according to the progression of epidemic'''
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
                # updating the status according to the progression of epidemic
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
                    chance_of_infection = 0.0009 * x * (1 - y)
                    if random() < chance_of_infection:
                        person.status = 'sick'

            for cmn_place in town:
                cmn_place.num_sick = 0

            # adding to the lists created
            healthy_history.append(healthy)
            sick_history.append(sick)
            recovered_history.append(recovered)
            dead_history.append(dead)

        return days, healthy_history,\
            sick_history, recovered_history, dead_history

    # Set the initial parameters ini_slid_values
    places = 75
    n_healthy = 25000
    n_sick = 25
    time_frame = 100
    initial_social_distancing = 0
    initial_vaccination = 0
    initial_travel_restri = 0

    # Create the figure and subplots
    fig, axs = plt.subplots(4, sharex=True, sharey=False)
    fig.suptitle('VIRUS SIMULATION')

    # Set the initial data
    days, healthy_history,\
        sick_history, recovered_history,\
        dead_history = simulate(places, n_healthy,
                                n_sick, time_frame, initial_social_distancing,
                                initial_vaccination, initial_travel_restri)

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
    slider_ax_social_distancing = plt.axes([0.2, 0.080, 0.65, 0.01])
    slider_ax_vaccination = plt.axes([0.2, 0.045, 0.65, 0.01])
    slider_ax_travel_restri = plt.axes([0.2, 0.010, 0.65, 0.01])

    slider_social_distancing = Slider(slider_ax_social_distancing,
                                      'Social Distancing', 0, 1,
                                      valinit=initial_social_distancing)
    slider_vaccination = Slider(slider_ax_vaccination,
                                'Vaccination', 0, 1,
                                valinit=initial_vaccination)
    slider_travel_restri = Slider(slider_ax_travel_restri,
                                  'Travel Restriction', 0, 1,
                                  valinit=initial_travel_restri)

    def update_plot(val):
        social_distancing = slider_social_distancing.val
        vaccination = slider_vaccination.val
        travel_restri = slider_travel_restri.val

        days, healthy_history,\
            sick_history, recovered_history,\
            dead_history = simulate(places,
                                    n_healthy, n_sick, time_frame,
                                    social_distancing, vaccination,
                                    travel_restri)

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

        axs[3].cla()
        axs[3].plot(days, dead_history[:-1], 'tab:red')
        axs[3].set_title('DEAD')

        # Redraw the canvas
        fig.canvas.draw()

    # Connect the update_plot function to the slider events
    slider_social_distancing.on_changed(update_plot)
    slider_vaccination.on_changed(update_plot)
    slider_travel_restri.on_changed(update_plot)

    plt.show()
