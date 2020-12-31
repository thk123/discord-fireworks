import os
from random import expovariate, uniform, gauss
from lepton import Particle, ParticleGroup, default_system, domain
from lepton.controller import Lifetime, Movement, Fader, ColorBlender
from lepton.emitter import StaticEmitter, PerParticleEmitter
from lepton.renderer import PointRenderer
from lepton.texturizer import SpriteTexturizer, create_point_texture
from pyglet import image
from pyglet.gl import *

spark_tex = image.load(os.path.join(os.path.dirname(__file__), 'resources/flare2.png')).get_texture()
spark_texturizer = SpriteTexturizer(spark_tex.id)
point_texturizer = SpriteTexturizer(create_point_texture(8, 50))

class Kaboom:
    lifetime = 5

    def __init__(self):
        self.color = (uniform(0, 1), uniform(0, 1), uniform(0, 1), 1)
        while max(self.color[:3]) < 0.9:
            self.color = (uniform(0, 1), uniform(0, 1), uniform(0, 1), 1)

        self.pos = (uniform(-50, 50), uniform(-30, 30), uniform(-30, 30))

        spark_emitter = StaticEmitter(
            template=Particle(position=self.pos, color=self.color),
            deviation=Particle(
                velocity=(gauss(0, 2), gauss(1, 2), gauss(0, 2)),
                age=1.5),
            velocity=domain.Sphere((0, 0, 0), 60, 50))

        self.sparks = ParticleGroup(
            controllers=[
                Lifetime(self.lifetime * 0.75),
                Movement(damping=0.93),
                ColorBlender([(0, (1, 1, 1, 1)), (2, self.color), (self.lifetime, self.color)]),
                Fader(fade_out_start=1.0, fade_out_end=self.lifetime * 0.5),
            ],
            renderer=PointRenderer(abs(gauss(10, 3)), spark_texturizer))

        spark_emitter.emit(int(gauss(200, 30)), self.sparks)

        pyglet.clock.schedule_once(self.add_twinkles, self.lifetime * 0.2)

    def add_twinkles(self, dt=None):
        def vel_component():
            return uniform(2.0, 5.0)

        self.trail_emitter = PerParticleEmitter(self.sparks,
            rate=gauss(25, 5),
            template=Particle(color=self.color),
            deviation=Particle(velocity=(vel_component(), vel_component(), vel_component()), age=self.lifetime * 0.5),
            time_to_live=self.lifetime * 0.15)

        self.trails = ParticleGroup(
            controllers=[
                Lifetime(self.lifetime * 1.5),
                Movement(damping=uniform(0.82, 0.98)),
                ColorBlender([(0, (1,1,1,1)), (1, self.color), (self.lifetime, self.color)]),
                Fader(max_alpha=0.75, fade_out_start=0, fade_out_end=gauss(self.lifetime * 0.2, 2)),
                self.trail_emitter
            ],
            renderer=PointRenderer(10, point_texturizer))

        if (uniform(0.0, 1.0) > 0.95):
            min_radius = 90
            ring = StaticEmitter(
                template=Particle(position=self.pos, color=self.color),
                velocity=domain.Disc(
                    (0, 0, 0),
                    (gauss(0.0, 0.1), 1, gauss(0.0, 0.1)),
                    max(min_radius, gauss(min_radius * 1.2, 30)),
                    min_radius))

            ring.emit(int(gauss(300, 20)), self.sparks)

        pyglet.clock.schedule_once(self.die, self.lifetime)

    def die(self, dt=None):
        default_system.remove_group(self.sparks)
        default_system.remove_group(self.trails)

def fire(dt=None):
    Kaboom()
