import numpy as np
import pygame

class Planet:
    def __init__(self, position, mass, size, colour):
        self.x, self.y = position
        self.mass = mass
        self.size = size
        self.colour = colour
        self.force = np.array([0.0, 0.0])
        self.velocity = np.array([0.0, 0.0])
    
    def show(self, screen):
        x, y = int(self.x), int(self.y)
        pygame.draw.circle(screen, self.colour, (x, y), self.size)
    
    def get_pos(self):
        return np.array([self.x, self.y])
    
    def move(self):
        position = self.get_pos()
        acceleration = self.force/self.mass
        self.velocity += acceleration
        position += self.velocity
        self.x, self.y = position[0], position[1]
        # print("Velocity: ", self.velocity, " | Size: ", self.size)

class Environment:
    def __init__(self, screen,  width, height, colour=(0, 0, 0)):
        self.screen = screen
        self.width = width
        self.height = height
        self.colour = colour
        self.planets = []
        self.GravityConstant = 50
    
    def addPlanets(self, n, **kargs):
        for i in range(n):
            size = kargs.get('size', np.random.randint(5, 50))
            # size = kargs.get('size', 25)
            mass = size
            x = kargs.get('x', np.random.uniform(size, self.width-size))
            y = kargs.get('y', np.random.uniform(size, self.height-size))
            colour = (np.random.uniform(50, 255), np.random.uniform(50, 255), np.random.uniform(50, 255))

            planet = Planet(position=(x, y), mass=mass, size=size, colour = colour)
            self.planets.append(planet)
    
    def showPlanets(self):
        for planet in self.planets:
            planet.show(self.screen)
    
    def resultant_forces(self):
        for planet_i in self.planets:
            Force = np.array([0.0, 0.0])
            for planet_j in self.planets:
                rij = planet_j.get_pos() - planet_i.get_pos()
                rij_mag = np.linalg.norm(rij)
                if planet_i != planet_j:
                    if self.collision_check(planet_i, planet_j):
                        self.elastic_collision(planet_i, planet_j)
                    else:
                        Force += self.GravityConstant*planet_i.mass*planet_j.mass/rij_mag**3*rij
                    
                    planet_i.force = Force
                    
    def elastic_collision(self, p1, p2):
        rij = p1.get_pos()-p2.get_pos()
        mass_factor1 = 2*p1.mass/(p1.mass + p2.mass)
        vec_factor1 = (p1.velocity-p2.velocity).dot(rij)
        denom1 = np.linalg.norm(rij)**2
        p1.velocity = p1.velocity - mass_factor1*vec_factor1/denom1*(rij)
        mass_factor2 = 2*p2.mass/(p1.mass + p2.mass)
        vec_factor2 = (p2.velocity-p1.velocity).dot(-rij)
        denom2 = np.linalg.norm(-rij)**2
        p2.velocity = p2.velocity - mass_factor2*vec_factor2/denom2*(-rij)
    
    def collision_check(self, p1, p2):
        rij = p1.get_pos()-p2.get_pos()
        rij_mag = np.linalg.norm(rij)
        c2c = rij_mag - (p1.size+p2.size)
        return True if c2c<= 0.0 else False
    
    def update(self):
        for planet in self.planets:
            planet.move()

'''
Collision: (vector form)
v1 = u1 - 2m2/(m1+m2)*(v1-v2).(x1-x2)/||x1-x2||^2*(x1-x2)

v2 = u2 - 2m1/(m1+m2)*(v2-v1).(x2-x1)/||x2-x1||^2*(x2-x1)
'''