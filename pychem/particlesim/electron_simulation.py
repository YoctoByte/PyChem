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
delta_t = Decimal('100e-22')            # seconds


particles = set()


class Particle:
    def __init__(self,
                 position=(Decimal('0'), Decimal('0'), Decimal('0')),
                 mass=u,
                 charge=Decimal('0'),
                 velocity=(Decimal('0'), Decimal('0'), Decimal('0'))):
        particles.add(self)
        self.position = position
        self.mass = mass
        # self.radius = Decimal('0.8751e-15')
        self.charge = charge
        # self.energy_goal = 13 * eV
        self.velocity = velocity


def simulation():
    def coulombs_law(c1, c2, r):
        if r != 0:
            F = Decimal(Ke*c1*c2/(r*r))
        else:
            F = None
        return F

    def gravitional_force(m1, m2, r):
        if r != 0:
            F = Decimal(G*m1*m2/(r*r))
        else:
            F = None
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

    data = dict()
    for particle in particles:
        data[particle] = dict()
        data[particle]['positions'] = list()
        data[particle]['velocities'] = list()

    for _ in range(300):
        for particle in particles:
            current_x, current_y, current_z = particle.position
            current_v_x, current_v_y, current_v_z = particle.velocity

            # calculate the next position of the particle:
            for other_particle in particles:
                if other_particle != particle:
                    other_x, other_y, other_z = other_particle.position
                    dx, dy, dz = other_x-current_x, other_y-current_y, other_z-current_z
                    distance = Decimal(sqrt(dx*dx + dy*dy + dz*dz))

                    fg = gravitional_force(particle.mass, other_particle.mass, distance)
                    fe = -coulombs_law(particle.charge, other_particle.charge, distance)
                    f_tot = fg + fe
                    f_x = dx / distance * f_tot
                    f_y = dy / distance * f_tot
                    f_z = dz / distance * f_tot
                    a_x, a_y, a_z = f_x/particle.mass, f_y/particle.mass, f_z/particle.mass
                    delta_v_x, delta_v_y, delta_v_z = a_x*delta_t, a_y*delta_t, a_z*delta_t

                    current_v_x += delta_v_x
                    current_v_y += delta_v_y
                    current_v_z += delta_v_z

            next_x = Decimal(current_x + current_v_x * delta_t)
            next_y = Decimal(current_y + current_v_y * delta_t)
            next_z = Decimal(current_z + current_v_z * delta_t)
            particle.next_position = (next_x, next_y, next_z)
            particle.next_velocity = (current_v_x, current_v_y, current_v_z)

        # applying all the calculated positions to the particle
        for particle in particles:
            particle.position = particle.next_position
            particle.velocity = particle.next_velocity

            current_x, current_y, current_z = particle.position
            data[particle]['positions'].append((float(current_x*Decimal('1e12')),
                                                float(current_y*Decimal('1e12')),
                                                float(current_z*Decimal('1e12'))))
    return data


def plot_3d(data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for key in data:
        xs = list()
        ys = list()
        zs = list()
        for x, y, z in data[key]['positions']:
            xs.append(float(x))
            ys.append(float(y))
            zs.append(float(z))
        ax.scatter(xs, ys, zs)
    plt.show()


# create hydrogen atom:
def create_atom(mass, charge, position=(Decimal('0'), Decimal('0'), Decimal('0'))):
    Particle(position=position,
             mass=mass,
             charge=charge,
             velocity=(Decimal('0'), Decimal('0'), Decimal('0')))


# create electron:
def create_electron():
    x = choice('+-') + choice('0123456789') + 'e-12'
    y = choice('+-') + choice('0123456789') + 'e-12'
    z = choice('+-') + choice('0123456789') + 'e-12'
    vx = choice('+-') + choice('0123456789') + 'e6'
    vy = choice('+-') + choice('0123456789') + 'e6'
    vz = choice('+-') + choice('0123456789') + 'e6'
    print('electron:')
    print('  pos: ' + x + ', ' + y + ', ' + z)
    print('  vel: ' + vx + ', ' + vy + ', ' + vz)
    Particle(position=(Decimal(x), Decimal(y), Decimal(z)),
             mass=Decimal('5.4857991e-4') * u,
             charge=-e,
             velocity=(Decimal(vx), Decimal(vy), Decimal(vz)))


create_atom(Decimal('1.00782504')*u, e)
create_atom(Decimal('1.00782504')*u, e, position=(Decimal('0'), Decimal('50e-12'), Decimal('0')))
create_electron()
create_electron()

data = simulation()
json_data = list()
for key in data:
    json_data.append(data[key])
with open('files/esim_data/version2.0/' + str(time.time()) + '.json', 'w') as jsonfile:
    json.dump(json_data, jsonfile, separators=(',', ':'), indent=4)
plot_3d(data)
