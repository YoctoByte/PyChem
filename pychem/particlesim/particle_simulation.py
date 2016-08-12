from decimal import Decimal


e = Decimal('1.6021766e-19')            # elementary charge (Coulomb)
u = Decimal('1.660539040e-27')          # atomic mass unit (kilograms)


class Particle:
    def __init__(self):
        self.mass = None
        self.gravitation = True
        self.weak_interaction = False
        self.strong_interaction = False
        self.electromagnetism = False

        self.position = (0, 0, 0)
        self.velocity = (0, 0, 0)


class Quark(Particle):
    def __init__(self):
        Particle.__init__(self)
        self.weak_interaction = True
        self.strong_interaction = True
        self.electromagnetism = True


class UpQuark(Quark):
    def __init__(self):
        Quark.__init__(self)
        self.charge = Decimal(2)/Decimal(3)*e


class DownQuark(Quark):
    def __init__(self):
        Quark.__init__(self)
        self.charge = Decimal(-1)/Decimal(3)*e


class Boson(Particle):
    def __init__(self):
        Particle.__init__(self)


class Photon(Boson):
    def __init__(self):
        Boson.__init__(self)


class Gluon(Boson):
    def __init__(self):
        Boson.__init__(self)


class ComposedParticle:
    def __init__(self):
        self.particles = set()


class Electron(Particle):
    def __init__(self):
        Particle.__init__(self)


class Proton(ComposedParticle):
    def __init__(self):
        ComposedParticle.__init__(self)
        self.particles = {UpQuark, UpQuark, DownQuark}
        self.mass = Decimal('1.007276466879') * u


class Neutron(ComposedParticle):
    def __init__(self):
        ComposedParticle.__init__(self)
        self.particles = {UpQuark, DownQuark, DownQuark}
        self.mass = Decimal('1.00866491588') * u
