from decimal import Decimal
# from random import choice, random
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
delta_t = Decimal('1000e-22')            # seconds


particles = set()


class Particle:
    def __init__(self, position=(Decimal('0'), Decimal('0'), Decimal('0')),
                 mass=u,
                 charge=Decimal('0'),
                 velocity=Decimal('0'),
                 direction=(Decimal('0'), Decimal('0'))):
        particles.add(self)
        self.position = position
        self.mass = mass
        # self.radius = Decimal('0.8751e-15')
        self.charge = charge
        # self.energy_goal = 13 * eV
        self.velocity = velocity
        self.direction = direction


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
        print('--------')
        for particle in particles:
            print('---')
            print('position: ' + str(particle.position))
            print('velocity: ' + str(particle.velocity))
            print('direction: ' + str(particle.direction))
            current_x, current_y, current_z = particle.position
            current_v = particle.velocity
            current_xy_angle, current_z_angle = particle.direction
            current_v_x = Decimal(current_v * Decimal(cos(current_xy_angle)) * Decimal(cos(current_z_angle)))
            current_v_y = Decimal(current_v * Decimal(sin(current_xy_angle)) * Decimal(cos(current_z_angle)))
            current_v_z = Decimal(current_v * Decimal(cos(current_z_angle)))
            if current_z_angle == 0.5 * pi:
                current_v_z = current_v
            if current_z_angle in [1.5 * pi, (-0.5) * pi]:
                current_v_z = -current_v

            # calculate the next position of the particle:
            for other_particle in particles:
                if other_particle != particle:
                    other_x, other_y, other_z = other_particle.position
                    dx, dy, dz = other_x-current_x, other_y-current_y, other_z-current_z
                    distance = Decimal(sqrt(dx*dx + dy*dy + dz*dz))

                    fg = gravitional_force(particle.mass, other_particle.mass, distance)
                    fe = -coulombs_law(particle.charge, other_particle.charge, distance)
                    ftot = fg + fe

                    print('fg: ' + str(fg))
                    print('fe: ' + str(fe))

                    xy_angle = get_angle(a=dx, o=dy)
                    xy_distance = Decimal(sqrt(dx*dx + dy*dy))
                    z_angle = get_angle(a=xy_distance, o=dz)
                    acceleration = ftot/particle.mass
                    delta_v = Decimal(acceleration*delta_t)
                    delta_v_x = Decimal(delta_v * Decimal(cos(xy_angle)) * Decimal(sin(z_angle)))
                    delta_v_y = Decimal(delta_v * Decimal(sin(xy_angle)) * Decimal(sin(z_angle)))
                    delta_v_z = Decimal(delta_v * Decimal(sin(z_angle)))

                    current_v_x += delta_v_x
                    current_v_y += delta_v_y
                    current_v_z += delta_v_z

            next_x = Decimal(current_x + current_v_x * delta_t)
            next_y = Decimal(current_y + current_v_y * delta_t)
            next_z = Decimal(current_z + current_v_z * delta_t)
            particle.next_position = (next_x, next_y, next_z)
            particle.next_velocity = Decimal(sqrt(current_v_x*current_v_x + current_v_y*current_v_y + current_v_z*current_v_z))
            current_v_xy = Decimal(sqrt(current_v_x*current_v_x + current_v_y*current_v_y))
            particle.next_direction = (get_angle(a=current_v_x, o=current_v_y), get_angle(a=current_v_xy, o=current_v_z))

        # applying all the calculated positions to the particle
        for particle in particles:
            particle.position = particle.next_position
            particle.velocity = particle.next_velocity
            particle.direction = particle.next_direction

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
Particle(position=(Decimal('0'), Decimal('0'), Decimal('0')),
         mass=Decimal('1.00782504') * u,
         charge=e,
         velocity=Decimal('0'),
         direction=(Decimal('0'), Decimal('0')))

# create electron:
Particle(position=(Decimal('11e-12'), Decimal('7e-12'), Decimal('3e-12')),
         mass=Decimal('5.4857991e-4') * u,
         charge=-e,
         velocity=Decimal('2e3'),
         direction=(Decimal(179/180 * pi), Decimal('0')))

data = simulation()
# with open('files/esim_data/' + str(time.time()) + '.json', 'w') as jsonfile:
#     json.dump(data, jsonfile, separators=(',', ':'), indent=4)
plot_3d(data)
