
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import random
import math
import matplotlib as mpl


class Point:
    def __init__(self, x, y, box_x, box_y):
        self.x = x
        self.y = y
        self.velocity = [random.randint(-2, 2), random.randint(-2, 2)]
        self.box_x = box_x
        self.box_y = box_y
        self.update_direction = random.randint(0, 150)
        self.is_infected = False
        self.infected_this_round = None
        self.is_healed = False

    def __repr__(self):
        return f'Coordinates are: {self.x}, {self.y}'

    def move(self):
        self.y = self.y + self.velocity[1]
        self.x = self.x + self.velocity[0]
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
number_of_points = 100
box_x = [0, 1500]
box_y = [0, 1500]
for _ in range(number_of_points):
    all_points.append(Point(random.randint(1, 1500), random.randint(1, 1500), box_x, box_y))
all_points[0].is_infected = True
all_points[0].infected_this_round = 0

radius_size = 20
colour = np.zeros(number_of_points)
susceptible = []
infectious = []
recovered = []


def update(i):
    for p in all_points:
        p.move()
        if i % 150 == p.update_direction:
            p.velocity = [random.randint(-2, 2), random.randint(-2, 2)]
        if p.is_infected:
            infectious.append(p)
        elif not p.is_infected:
            susceptible.append(p)
        elif p.is_healed:
            recovered.append(p)
    xs, ys = points_to_array(all_points)
    scat.set_offsets(np.stack((xs, ys), axis=-1))

    radius(radius_size, colour, i)
    scat.set_array(colour)
    healing(colour, i)
    #move_to_center_location()


def healing(c, i):
    for j in range(len(all_points)):
        p = all_points[j]
        if p.is_infected:
            if i == 600 + p.infected_this_round:
                p.is_infected = False
                p.is_healed = True
                c[j] = 0.5


infection_probability = 0.4


def radius(r, c, round):
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
                        p.infected_this_round = round
                    if q.infected_this_round is None:
                        q.infected_this_round = round
            if p.is_infected:
                c[i] = 1
            if q.is_infected:
                c[j] = 1
    for p in all_points:
        if p.infected_this_round == round:
            p.is_infected = True

        

center_probability = 0.0005
t = np.linspace(0, 160)


def move_to_center_location():
    for p in all_points:
        if random.random() <= center_probability:
            p.x = box_x[1] / 2
            p.y = box_y[1] / 2


fig, (ax1, ax2) = plt.subplots(2)
#fig, ax = plt.subplots()
centerpoint_x = box_x[1] / 2
centerpoint_y = box_y[1] / 2

ax1.set(xlim=(box_x[0], box_x[1]), ylim=(box_y[0], box_y[1]))
ax1.axes.xaxis.set_visible(False)
ax1.axes.yaxis.set_visible(False)
xs, ys = points_to_array(all_points)
scat = ax1.scatter(xs, ys,
                    c=np.zeros(xs.shape[0]),
                    cmap=mpl.colors.ListedColormap(['blue', 'grey', 'red']),
                    vmin=0, vmax=1)
#ax1.plot(centerpoint_x, centerpoint_y, 'Dk')

#ax2.plot(t, susceptible)
#ax2.plot(t, infectious)
#ax2.plot(t, recovered)

ani = animation.FuncAnimation(fig, update, interval=10)#, frames=range(6000), repeat=False)
Writer = animation.writers['ffmpeg']
writer = Writer(fps=60, metadata=dict(artist='Me'), bitrate=1800)
ani.save('CentralLocation.mp4', writer=writer)
plt.show()

