import math
import os
from random import uniform, normalvariate

import pyglet
from lepton import Particle
from lepton.emitter import StaticEmitter
from lepton.group import ParticleGroup
from lepton.particle_struct import Vec3
from lepton.renderer import BillboardRenderer
from lepton.texturizer import SpriteTexturizer
from pyglet import image

from fireworks.basic_firework import Kaboom

arc_radius = 150
angle = math.pi * 0.7
speed = 1.0


class Tracer:
    def __init__(self):
        self.time_to_explode = 1.0
        self.starting_position = (uniform(-44, 44), -40, normalvariate(0, 25))
        self.starting_velocity = Vec3(uniform(-25, 25), normalvariate(100, 10), uniform(-10, 10))
        self.comet = StaticEmitter(
            rate=600,
            time_to_live=self.time_to_explode,
            template=Particle(
                size=(2, 2, 2),
                color=(1, 1, 0),
                position=self.starting_position
            ),
            deviation=Particle(
                velocity=(0.7, 0.7, 0.7),
                up=(0, 0, math.pi),
                rotation=(0, 0, math.pi),
                color=(0.5, 0.5, 0.5)),
        )

        images = [image.load(os.path.join(os.path.dirname(__file__), 'resources/flare%s.png' % (i + 1)))
                  for i in range(4)]
        group = ParticleGroup(controllers=[self.comet],
                              renderer=BillboardRenderer(SpriteTexturizer.from_images(images)))
        pyglet.clock.schedule_interval(self.tick, (1.0 / 30.0))

    def tick(self, dt):
        self.time_to_explode -= dt
        if self.time_to_explode <= 0.0:
            Kaboom(Vec3(self.comet.template.position.x, self.comet.template.position.y, self.comet.template.position.z))
            pyglet.clock.unschedule(self.tick)
        else:
            self.starting_velocity.y -= 2
            self.comet.template.position.x += self.starting_velocity.x * dt
            self.comet.template.position.y += self.starting_velocity.y * dt
            self.comet.template.position.z += self.starting_velocity.z * dt


def run_tracer(dt):
    comet = Tracer()
