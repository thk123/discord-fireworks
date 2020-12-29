import os
from random import expovariate, uniform, gauss
from lepton import Particle, ParticleGroup, default_system, domain
from lepton.controller import Lifetime, Movement, Fader, ColorBlender
from lepton.emitter import StaticEmitter, PerParticleEmitter
from lepton.renderer import PointRenderer
from lepton.texturizer import SpriteTexturizer, create_point_texture
from pyglet import image
from pyglet.gl import *
import PIL
import PIL.ImageDraw
import math

spark_tex = image.load(os.path.join(os.path.dirname(__file__), 'resources/flare3.png')).get_texture()
spark_texturizer = SpriteTexturizer(spark_tex.id)
trail_texturizer = SpriteTexturizer(create_point_texture(8, 50))

class TextFirework:
    lifetime = 5

    def __init__(self, text):

        image = PIL.Image.new('RGB', (1, 1))
        draw = PIL.ImageDraw.Draw(image)
        text_width, text_height = draw.textsize(text)

        image = PIL.Image.new('RGB', (text_width, text_height), (0, 0, 0))
        draw = PIL.ImageDraw.Draw(image)
        draw.text((0, 0), text, fill = (255, 255, 255))

        pixels = [(x, text_height - y) for x in range(0, text_width) for y in range(0, text_height) if image.getpixel((x, y)) != (0, 0, 0)]

        color = (uniform(0, 1), uniform(0, 1), uniform(0, 1), 1)
        while max(color[:3]) < 0.9:
            color = (uniform(0, 1), uniform(0, 1), uniform(0, 1), 1)

        self.sparks = ParticleGroup(
            controllers=[
                Lifetime(self.lifetime * 0.75),
                Movement(damping=0.93),
                ColorBlender([(0, (1, 1, 1, 1)), (2, color), (self.lifetime, color)]),
                Fader(fade_out_start=1.0, fade_out_end=self.lifetime * 0.5),
            ],
            renderer=PointRenderer(abs(gauss(10, 3)), spark_texturizer))

        (origin_x, origin_y, origin_z) = (uniform(-20, 20), uniform(-20, 20), uniform(-20, 20))

        for (x, y) in pixels:
            (x, y, z) = (origin_x + x * 2, origin_y + y * 2, origin_z)
            self.sparks.new(Particle(position = (x, y, z), color = color))
        self.sparks.update(0)

        pyglet.clock.schedule_once(self.die, self.lifetime * 2)

    def die(self, dt=None):
        default_system.remove_group(self.sparks)

MEAN_FIRE_INTERVAL = 3.0

def fire(text):
    TextFirework(text)
