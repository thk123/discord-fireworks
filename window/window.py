import pyglet
from lepton import default_system
from lepton._controller import Gravity, Lifetime, Movement, Fader
from pyglet.gl import *

win = pyglet.window.Window(resizable=True, visible=False)
win.clear()


def on_resize(width, height):
    """Setup 3D projection for window"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, 1.0 * width / height, 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


win.on_resize = on_resize

yrot = 0.0

glEnable(GL_BLEND)
glShadeModel(GL_SMOOTH)
glBlendFunc(GL_SRC_ALPHA, GL_ONE)
glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);
glDisable(GL_DEPTH_TEST)

default_system.add_global_controller(
    Gravity((0, -15, 0))
)
default_system.add_global_controller(
	Lifetime(3.0),
	Movement(min_velocity=5),
	Fader(max_alpha=0.7, fade_out_start=1, fade_out_end=3.0),
)

def run(firework):
    win.set_visible(True)
    pyglet.clock.schedule_interval(default_system.update, (1.0 / 30.0))
    if firework:
        firework()
    pyglet.app.run()


@win.event
def on_draw():
    global yrot
    win.clear()
    glLoadIdentity()
    glTranslatef(0, 0, -100)
    glRotatef(yrot, 0.0, 1.0, 0.0)
    default_system.draw()
    '''
	glBindTexture(GL_TEXTURE_2D, 1)
	glEnable(GL_TEXTURE_2D)
	glEnable(GL_POINT_SPRITE)
	glPointSize(100);
	glBegin(GL_POINTS)
	glVertex2f(0,0)
	glEnd()
	glBindTexture(GL_TEXTURE_2D, 2)
	glEnable(GL_TEXTURE_2D)
	glEnable(GL_POINT_SPRITE)
	glPointSize(100);
	glBegin(GL_POINTS)
	glVertex2f(50,0)
	glEnd()
	glBindTexture(GL_TEXTURE_2D, 0)
	'''
