import math
import os

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
        self.starting_position = (0, -40, 0)
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
            vel = 80
            self.comet.template.position.y += vel*dt
            #self.comet.template.velocity.y = vel



#############################################################################
#
# Copyright (c) 2008 by Casey Duncan and contributors
# All Rights Reserved.
#
# This software is subject to the provisions of the MIT License
# A copy of the license should accompany this distribution.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#
#############################################################################
"""Flying comet using textured billboard quads"""

__version__ = '$Id$'

import os
import math
from pyglet import image
from pyglet.gl import *

from lepton import Particle, ParticleGroup, default_system
from lepton.renderer import BillboardRenderer
from lepton.texturizer import SpriteTexturizer
from lepton.emitter import StaticEmitter
from lepton.controller import Gravity, Lifetime, Movement, Fader, ColorBlender

# comet = StaticEmitter(
#     rate=600,
#     template=Particle(
#         size=(2, 2, 0),
#         color=(1, 1, 0),
#     ),
#     deviation=Particle(
#         velocity=(0.7, 0.7, 0.7),
#         up=(0, 0, math.pi),
#         rotation=(0, 0, math.pi),
#         color=(0.5, 0.5, 0.5))
# )
#
# images = [image.load(os.path.join(os.path.dirname(__file__), 'resources/flare%s.png' % (i + 1)))
#           for i in range(4)]
# group = ParticleGroup(controllers=[comet],
#                       renderer=BillboardRenderer(SpriteTexturizer.from_images(images)))
#
# arc_radius = 150
# angle = math.pi * 0.7
# speed = 1.0
#
#
# def move_comet(td):
#     global angle, arc_radius, speed
#     comet.template.position = (
#         -math.sin(angle) * arc_radius * 0.3,
#         math.sin(angle * 0.7) * arc_radius * 0.03,
#         -math.cos(angle) * arc_radius - arc_radius * 1.05)
#     comet.template.velocity = (
#         comet.template.position.x * 0.05 - comet.template.last_position.x,
#         comet.template.position.y * 0.05 - comet.template.last_position.y,
#         comet.template.position.z * 0.05 - comet.template.last_position.z)
#     angle -= td * speed


def run_tracer(dt):
    # pyglet.clock.schedule_interval(move_comet, (1.0 / 30.0))
    # move_comet(0)
    comet = Tracer()
