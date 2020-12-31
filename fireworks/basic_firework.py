import os
from random import expovariate, uniform, gauss
from lepton import Particle, ParticleGroup, default_system, domain
from lepton.controller import Lifetime, Movement, Fader, ColorBlender
from lepton.emitter import StaticEmitter, PerParticleEmitter
from lepton.renderer import PointRenderer
from lepton.texturizer import SpriteTexturizer, create_point_texture
from pyglet import image
from pyglet.gl import *

spark_tex = image.load(os.path.join(os.path.dirname(__file__), 'resources/flare3.png')).get_texture()
spark_texturizer = SpriteTexturizer(spark_tex.id)
trail_texturizer = SpriteTexturizer(create_point_texture(8, 50))


class Kaboom:
    lifetime = 5

    def __init__(self, pos=None):
        color = (uniform(0, 1), uniform(0, 1), uniform(0, 1), 1)
        while max(color[:3]) < 0.9:
            color = (uniform(0, 1), uniform(0, 1), uniform(0, 1), 1)
        pos = pos if pos else (uniform(-50, 50), uniform(-30, 30), uniform(-30, 30))
        spark_emitter = StaticEmitter(
            template=Particle(
                position=pos,
                color=color),
            deviation=Particle(
                velocity=(gauss(0, 5), gauss(0, 5), gauss(0, 5)),
                age=1.5),
            velocity=domain.Sphere((0, gauss(40, 20), 0), 60, 60))

        self.sparks = ParticleGroup(
            controllers=[
                Lifetime(self.lifetime * 0.75),
                Movement(damping=0.93),
                ColorBlender([(0, (1, 1, 1, 1)), (2, color), (self.lifetime, color)]),
                Fader(fade_out_start=1.0, fade_out_end=self.lifetime * 0.5),
            ],
            renderer=PointRenderer(abs(gauss(10, 3)), spark_texturizer))

        spark_emitter.emit(int(gauss(60, 40)) + 50, self.sparks)

        spread = abs(gauss(0.4, 1.0))
        self.trail_emitter = PerParticleEmitter(self.sparks, rate=uniform(5, 30),
                                                template=Particle(
                                                    color=color),
                                                deviation=Particle(
                                                    velocity=(spread, spread, spread),
                                                    age=self.lifetime * 0.75))

        self.trails = ParticleGroup(
            controllers=[
                Lifetime(self.lifetime * 1.5),
                Movement(damping=0.83),
                ColorBlender([(0, (1, 1, 1, 1)), (1, color), (self.lifetime, color)]),
                Fader(max_alpha=0.75, fade_out_start=0, fade_out_end=gauss(self.lifetime, self.lifetime * 0.3)),
                self.trail_emitter
            ],
            renderer=PointRenderer(10, trail_texturizer))

        pyglet.clock.schedule_once(self.die, self.lifetime * 2)

    def reduce_trail(self, dt=None):
        if self.trail_emitter.rate > 0:
            self.trail_emitter.rate -= 1

    def die(self, dt=None):
        default_system.remove_group(self.sparks)
        default_system.remove_group(self.trails)




MEAN_FIRE_INTERVAL = 3.0


def fire(dt=None):
    Kaboom()
    Kaboom()
    Kaboom()

    pyglet.clock.schedule_once(fire, expovariate(1.0 / (MEAN_FIRE_INTERVAL - 1)) + 1)

def fire_one(dt=None):
    Kaboom()

def fire_N(num_times, dt):
    for i in range(num_times):
        Kaboom()