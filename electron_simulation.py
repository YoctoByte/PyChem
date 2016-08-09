from decimal import Decimal
from random import choice, random
from math import sqrt, asin, acos, atan, sin, cos, tan, pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import time


G = Decimal('6.67408e-11')              # gravitational constant (m3*kg-1*s-2)
Ke = Decimal('8.9875517873681764e9')    # Coulomb's constant (N*m2*C-2)
u = Decimal('1.660539040e-27')          # atomic mass unit (kilograms)
e = Decimal('1.6021766e-19')            # elementary charge (Coulomb)
eV = Decimal('1.6021766e-19')           # electronvolt (Joule)
delta_t = Decimal('100e-22')              # seconds

particles = set()

class Electron:
    def __init__(self):
        self.mass = Decimal('5.48579909070e-4') * u  # mass in kg
        self.radius = Decimal('0.8751e-15')
        self.position = (Decimal(choice('0123456789') + 'e-13'),
                         Decimal(choice('0123456789') + 'e-13'),
                         Decimal(choice('0123456789') + 'e-13'))  # (x, y, z) in meters
        self.charge = -e
        self.energy_goal = 13 * eV
        self.velocity = Decimal(sqrt(2*self.energy_goal/self.mass))
        self.direction = (Decimal(2 * pi * random()), 2 * pi * random())  # in (xy_angle, z_angle)


class Atom:
    def __init__(self):
        self.mass = Decimal('1.00782504') * u  # mass in kg
        self.position = (Decimal('0'), Decimal('0'), Decimal('0'))  # (x, y, z) in meters
        self.charge = e
        self.velocity = Decimal('0')
        self.direction = (Decimal('0'), Decimal('0'))  # in (xy_angle, z_angle)


def simulation():
    def coulombs_law(c1, c2, r):
        F = Ke*c1*c2/(r*r)
        return F

    def gravitaional_force(m1, m2, r):
        F = G*m1*m2/(r*r)
        return F

    def get_angle(a=None, o=None, s=None):
        angle = None
        if a is not None and o is not None:
            if a == 0:
                if o == 0:
                    angle = Decimal('0')
                elif o > 0:
                    angle = Decimal(0.5 * pi)
                elif o < 0:
                    angle = Decimal((-0.5) * pi)
            elif o == 0:
                if a > 0:
                    angle = Decimal('0')
                elif a < 0:
                    angle = Decimal(pi)
            else:
                angle = Decimal(atan(o/a))
                if a < 0:
                    angle += Decimal(pi)
        if angle is not None:
            if angle < 0:
                angle += Decimal(pi)
            return angle
        else:
            raise ValueError

    atom = Atom()
    electron = Electron()

    data = dict()
    data['positions'] = list()
    data['distances'] = list()
    data['velocities'] = list()
    initial_conditions = dict()
    initial_conditions['delta time'] = float(delta_t)
    initial_conditions['electron velocity'] = float(electron.velocity)
    x, y, z = electron.position
    initial_conditions['electron position'] = (float(x), float(y), float(z))
    xy, z = electron.direction
    initial_conditions['electron direction'] = (float(xy), float(z))
    data['initial conditions'] = initial_conditions
    for _ in range(500):
        # print('--------')
        xe, ye, ze = electron.position
        xa, ya, za = atom.position
        dx, dy, dz = abs(xe-xa), abs(ye-ya), abs(ze-za)
        r = Decimal(sqrt(dx*dx + dy*dy + dz*dz))
        dx, dy, dz = xe-xa, ye-ya, ze-za
        xy_angle = get_angle(a=dx, o=dy)
        xy_r = Decimal(sqrt(dx*dx + dy*dy))
        z_angle = get_angle(a=xy_r, o=dz)

        Fg = gravitaional_force(electron.mass, atom.mass, r)
        Fe = coulombs_law(electron.charge, atom.charge, r)
        Ftot = Fe + Fg
        a_electron = Ftot/electron.mass
        a_atom = Ftot/atom.mass

        delta_v_electron = a_electron * delta_t
        velocity = electron.velocity
        xy_dir, z_dir = electron.direction
        x_vel = Decimal(velocity * Decimal(cos(xy_dir)) * Decimal(sin(z_dir)))
        y_vel = Decimal(velocity * Decimal(sin(xy_dir)) * Decimal(sin(z_dir)))
        z_vel = Decimal(velocity * Decimal(sin(z_dir)))
        delta_x_vel = Decimal(-delta_v_electron * Decimal(cos(xy_angle)) * Decimal(sin(z_angle)))
        delta_y_vel = Decimal(-delta_v_electron * Decimal(sin(xy_angle)) * Decimal(sin(z_angle)))
        delta_z_vel = Decimal(-delta_v_electron * Decimal(sin(z_angle)))
        new_x_vel = Decimal(x_vel - delta_x_vel)
        new_y_vel = Decimal(y_vel - delta_y_vel)
        new_z_vel = Decimal(z_vel - delta_z_vel)
        new_xe = Decimal(xe + new_x_vel * delta_t)
        new_ye = Decimal(ye + new_y_vel * delta_t)
        new_ze = Decimal(ze + new_z_vel * delta_t)
        electron.position = (new_xe, new_ye, new_ze)
        electron.velocity = Decimal(sqrt(new_x_vel*new_x_vel + new_y_vel*new_y_vel + new_z_vel*new_z_vel))
        new_xy_dir = get_angle(a=new_x_vel, o=new_y_vel)
        new_xy_vel = Decimal(sqrt(new_x_vel*new_x_vel + new_y_vel*new_y_vel))
        new_z_dir = get_angle(a=new_xy_vel, o=new_z_vel)
        electron.direction = (new_xy_dir, new_z_dir)
        # print('vel: ' + str(electron.velocity))
        # print('pos: ' + str(electron.position))
        # print('dis: ' + str(r))
        data['positions'].append((float(new_xe*Decimal('1e12')),
                                  float(new_ye*Decimal('1e12')),
                                  float(new_ze*Decimal('1e12'))))
        data['velocities'].append(float(electron.velocity))
        data['distances'].append(float(r))

        # delta_v_atom = a_atom * delta_t
    return data


def plot_3d(data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs = list()
    ys = list()
    zs = list()
    for x, y, z in data['positions']:
        xs.append(float(x))
        ys.append(float(y))
        zs.append(float(z))
    ax.scatter(xs, ys, zs)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()


data = simulation()
with open('files/esim_data/' + str(time.time()) + '.json', 'w') as jsonfile:
    json.dump(data, jsonfile, separators=(',', ':'), indent=4)
plot_3d(data)


def plot_2d(xs, ys):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xs, ys)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    plt.show()

# for a in range(589):
#     angle = a/587 * 2 * pi
#     x = cos(angle)
#     y = sin(angle)
#     new_angle = get_angle(a=x, o=y)
#     print(angle, new_angle)
