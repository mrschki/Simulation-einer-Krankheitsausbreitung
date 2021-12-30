
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import random
import math
import matplotlib as mpl


def epidemic_simulation(number_of_points, radius_size, infection_probability, healing_time):
    class Point:
        def __init__(self, x, y, box_x, box_y, in_box):
            self.x = x
            self.y = y
            self.velocity = [0.5 * random.randint(-1, 1), 0.5 * random.randint(-1, 1)]
            self.box_x = box_x
            self.box_y = box_y
            self.update_direction = random.randint(0, 150)
            self.is_infected = False
            self.infected_this_round = None
            self.is_healed = False
            self.healed_this_round = None
            self.in_box = in_box
            self.reproduction = 0

        def __repr__(self):
            return f'Coordinates are: {self.x}, {self.y}'

        def move(self):
            self.x = self.x + self.velocity[0]
            self.y = self.y + self.velocity[1]
            self.x = self.x + self.velocity[0]
            self.y = self.y + self.velocity[1]
            # self.y = self.y + random.randint(-10, 10)
            # self.x = self.x + random.randint(-10, 10)
            if self.x < self.box_x[0] or self.x > self.box_x[1]:
                self.velocity[0] = -self.velocity[0]
            elif self.y < self.box_y[0] or self.y > self.box_y[1]:
                self.velocity[1] = -self.velocity[1]

        def to_list(self):
            return [self.x, self.y]

    def points_to_array(points):
        num_points = len(points)
        xs = np.zeros(num_points)
        ys = np.zeros(num_points)

        for i in range(num_points):
            c = points[i]
            xs[i] = c.x
            ys[i] = c.y
        return xs, ys

    all_points = []

    box1_x = [0, 500]
    box1_y = [0, 500]
    box2_x = [600, 1100]
    box2_y = [0, 500]
    box3_x = [0, 500]
    box3_y = [600, 1100]
    box4_x = [600, 1100]
    box4_y = [600, 1100]

    for _ in range(number_of_points):
        all_points.append(Point(random.randint(box1_x[0], box1_x[1]), random.randint(box1_y[0],
                                box1_y[1]), box1_x, box1_y, in_box=0))
    for _ in range(number_of_points):
        all_points.append(Point(random.randint(box2_x[0], box2_x[1]), random.randint(box2_y[0], box2_y[1]),
                                box2_x, box2_y, in_box=1))
    for _ in range(number_of_points):
        all_points.append(Point(random.randint(box3_x[0], box3_x[1]), random.randint(box3_y[0], box3_y[1]),
                                box3_x, box3_y, in_box=2))
    for _ in range(number_of_points):
        all_points.append(Point(random.randint(box4_x[0], box4_x[1]), random.randint(box4_y[0], box4_y[1]),
                                box4_x, box4_y, in_box=3))
    all_points[0].is_infected = True
    all_points[0].infected_this_round = 0

    colour = np.zeros(number_of_points)
    infectious = []
    recovered = []
    susceptible = []

    def update(i):
        list_of_infected = []
        list_of_recovered = []
        for p in all_points:
            p.move()
            if i % 150 == p.update_direction:
                p.velocity = [0.5 * random.randint(-1, 1), 0.5 * random.randint(-1, 1)]
        xs, ys = points_to_array(all_points)
        scat.set_offsets(np.stack((xs, ys), axis=-1))

        radius(radius_size, colour, i)
        scat.set_array(colour)
        healing(colour, i, i)
        for p in all_points:
            if p.infected_this_round is not None:
                list_of_infected.append(p)
            if p.healed_this_round is not None:
                list_of_recovered.append(p)
        #move_to_center_location() # Mit Zentrum
        change_box() #mit Reisen unter verschiedenen Kolonien
        infectious.append(len(list_of_infected) - len(list_of_recovered))
        recovered.append(len(list_of_recovered))
        susceptible.append(len(all_points) - len(list_of_infected))

    def healing(c, i, rounds):
        for j in range(len(all_points)):
            p = all_points[j]
            if p.is_infected:
                if i == healing_time + p.infected_this_round:
                    p.is_infected = False
                    p.healed_this_round = rounds
                    c[j] = 0.5
                    if p.healed_this_round == rounds:
                        p.is_healed = True

    def radius(r, c, rounds):
        num_points = len(all_points)
        for i in range(num_points):
            for j in range(num_points):
                if i == j:
                    continue
                p = all_points[i]
                q = all_points[j]
                distance_check = math.dist(p.to_list(), q.to_list())
                if (not p.is_infected and not q.is_infected)\
                        or (p.is_infected and q.is_infected)\
                        or (not p.is_infected and p.infected_this_round is not None)\
                        or (not q.is_infected and q.infected_this_round is not None):
                    continue
                if distance_check <= r:
                    if random.random() <= infection_probability:
                        c[i] = 1
                        c[j] = 1
                        if p.infected_this_round is None:
                            p.infected_this_round = rounds
                            q.reproduction =q.reproduction + 1
                        if q.infected_this_round is None:
                            q.infected_this_round = rounds
                            p.reproduction = p.reproduction + 1
                if p.is_infected:
                    c[i] = 1
                if q.is_infected:
                    c[j] = 1
        for p in all_points:
            if p.infected_this_round == rounds:
                p.is_infected = True

    center_probability = 0.0005
    change_probability = 0.0005
    box_probability = 0.25

    def change_box():
        for p in all_points:
            if random.random() <= change_probability:
                if p.in_box == 0:
                    if random.random() <= box_probability:
                        p.in_box = 1
                        p.x = centerpoint2_x
                        p.y = centerpoint2_y
                        p.box_x = box2_x
                        p.box_y = box2_y
                    elif random.random() <= box_probability:
                        p.in_box = 2
                        p.x = centerpoint3_x
                        p.y = centerpoint3_y
                        p.box_x = box3_x
                        p.box_y = box3_y
                    elif random.random() <= box_probability:
                        p.in_box = 3
                        p.x = centerpoint4_x
                        p.y = centerpoint4_y
                        p.box_x = box4_x
                        p.box_y = box4_y
                elif p.in_box == 1:
                    if random.random() <= box_probability:
                        p.in_box = 0
                        p.x = centerpoint1_x
                        p.y = centerpoint1_y
                        p.box_x = box1_x
                        p.box_y = box1_y
                    elif random.random() <= box_probability:
                        p.in_box = 2
                        p.x = centerpoint3_x
                        p.y = centerpoint3_y
                        p.box_x = box3_x
                        p.box_y = box3_y
                    elif random.random() <= box_probability:
                        p.in_box = 3
                        p.x = centerpoint4_x
                        p.y = centerpoint4_y
                        p.box_x = box4_x
                        p.box_y = box4_y
                elif p.in_box == 2:
                    if random.random() <= box_probability:
                        p.in_box = 0
                        p.x = centerpoint1_x
                        p.y = centerpoint1_y
                        p.box_x = box1_x
                        p.box_y = box1_y
                    elif random.random() <= box_probability:
                        p.in_box = 1
                        p.x = centerpoint2_x
                        p.y = centerpoint2_y
                        p.box_x = box2_x
                        p.box_y = box2_y
                    elif random.random() <= box_probability:
                        p.in_box = 3
                        p.x = centerpoint4_x
                        p.y = centerpoint4_y
                        p.box_x = box4_x
                        p.box_y = box4_y
                elif p.in_box == 3:
                    if random.random() <= box_probability:
                        p.in_box = 0
                        p.x = centerpoint1_x
                        p.y = centerpoint1_y
                        p.box_x = box1_x
                        p.box_y = box1_y
                    elif random.random() <= box_probability:
                        p.in_box = 1
                        p.x = centerpoint2_x
                        p.y = centerpoint2_y
                        p.box_x = box2_x
                        p.box_y = box2_y
                    elif random.random() <= box_probability:
                        p.in_box = 2
                        p.x = centerpoint3_x
                        p.y = centerpoint3_y
                        p.box_x = box3_x
                        p.box_y = box3_y

    def move_to_center_location():
        for p in all_points:
            if random.random() <= center_probability:
                p.x = centerpoint1_x
                p.y = centerpoint1_y

    fig, ax = plt.subplots()
    centerpoint1_x = box1_x[1] / 2
    centerpoint1_y = box1_y[1] / 2
    centerpoint2_x = centerpoint1_x + box2_x[0]
    centerpoint2_y = box2_y[1] / 2
    centerpoint3_x = centerpoint1_x
    centerpoint3_y = centerpoint1_y + box3_y[0]
    centerpoint4_x = centerpoint2_x
    centerpoint4_y = centerpoint3_y


    ax.set(xlim=(box1_x[0], box2_x[1]), ylim=(box1_y[0], box3_y[1]))
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    xs, ys = points_to_array(all_points)
    scat = ax.scatter(xs, ys,
                      c=np.zeros(xs.shape[0]),
                      cmap=mpl.colors.ListedColormap(['blue', 'grey', 'red']),
                      vmin=0, vmax=1)

    ax.plot(centerpoint1_x, centerpoint1_y, 'Dk')
    ax.plot(centerpoint2_x, centerpoint2_y, "Dk")
    ax.plot(centerpoint3_x, centerpoint3_y, "Dk")
    ax.plot(centerpoint4_x, centerpoint4_y, "Dk")

    reproduction_number = []



    #Hier kann ein Video eines Durchlaufs gespeichert werden.

    #Writer = animation.writers['ffmpeg']
    #writer = Writer(fps=60, metadata=dict(artist='Me'), bitrate=1800)
    #ani.save('CentralLocation.mp4', writer=writer)
    #plt.show()

    t = [i for i in range(3000)]
    i = 0
    simulation_running = False
    #simulation_running = True
    while simulation_running:
        update(i)
        i = i + 1
        t.append(i)
        if min(infectious) == 0:
            simulation_running = False

    ax.vlines(box1_x[1], ymin=box1_y[0], ymax=box3_y[1], colors="black")
    ax.vlines(box2_x[0], ymin=box2_y[0], ymax=box3_y[1], colors="black")
    ax.hlines(box1_y[1], xmax=box2_x[1], xmin=box1_x[0], colors="black")
    ax.hlines(box3_y[0], xmax=box2_x[1], xmin=box1_x[0], colors="black")

    ani = animation.FuncAnimation(fig, update, interval=20, frames=range(len(t) - 1), repeat=False)
    plt.show()
    for p in all_points:
        if p.infected_this_round is not None:
            reproduction_number.append(p.reproduction)

    plt.plot(t, susceptible, label="Susceptible")
    plt.plot(t, infectious, label="Infectious")
    plt.plot(t, recovered, label="Recovered")
    plt.legend()
    plt.savefig("SIR-Graph")
    plt.show()

    base_repoduction = reproduction_number[0]

    peak = infectious[infectious.index(max(infectious))]#, infectious.index(max(infectious))]
    disease_extinct = max(t)
    with open('Peak.txt', 'w') as f:
        f.write(f"{peak}, ")

    with open('infectious.txt', 'w') as f:
        for p in infectious:
            f.write(f"{p}, ")
    with open("Kranheit_ausgestorben.txt", "w") as f:
        f.write(f"{disease_extinct}, ")

    with open('Reproduktionszahl.txt', 'w') as f:
        f.write(f"{base_repoduction}, ")
    return peak, infectious, disease_extinct, base_repoduction, susceptible


epidemic_simulation(number_of_points=35, infection_probability=0.6, radius_size=13, healing_time=600)



"""
Hier wird dis Simulation oft Durchgeführt um quantitative Daten zu sammeln.

x_axis = []
all_peaks = []
all_extinct = []
all_reproduction = []
all_susceptible = []
point = 30
radius = 13
infection = 0.0
healing = 600
for h in range(50):
    average_susceptible = []
    average_peak = []
    average_extinct = []
    average_reproduction = []
    print(h)
    for i in range(10):
        peak, infectious, disease_extinct, base_reproduction, susceptible = epidemic_simulation(number_of_points=point, radius_size=radius, infection_probability=infection, healing_time=healing)
        #print(average_peak)
        #print(peak)
        average_susceptible.append(susceptible)
        average_peak.append(peak)
        average_extinct.append(disease_extinct)
        average_reproduction.append(base_reproduction)
    average_extinct = sum(average_extinct) / len(average_extinct)
    all_extinct.append(average_extinct)
    average_peak = sum(average_peak) / len(average_peak)
    all_peaks.append(average_peak)
    average_reproduction = sum(average_reproduction) / len(average_reproduction)
    all_reproduction.append(average_reproduction)
    average_susceptible = sum(susceptible) / len(susceptible)
    all_susceptible.append(average_susceptible)
    #radius = radius + 1
    #x_axis.append(radius)
    infection = infection + 1./50
    x_axis.append(infection)
    #healing = healing + 50
    #x_axis.append(healing)
print(all_peaks)
print(all_reproduction)
print(all_extinct)
print(all_susceptible)
with open("Numerische Werte", "w") as f:
    f.write(str(all_peaks))
    f.write(str(all_reproduction))
    f.write(str(all_extinct))
    f.write(str(all_susceptible))
plt.plot(x_axis, all_peaks, label="Peaks")
plt.legend()
plt.savefig("peaks")
plt.plot(x_axis, all_extinct, label="Extinct")
plt.legend()
plt.savefig("extinct")
plt.plot(x_axis, all_reproduction, label="Reproduction")
plt.legend()
plt.savefig("reproduction")
"""