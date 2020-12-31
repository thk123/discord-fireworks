import sys

import threading
from firework_parsing import firework_parsing
import pyglet

if __name__ == '__main__':
    from window import window
    draw_thread = threading.Thread(target = lambda: window.run(None))
    draw_thread.start()

    while True:
        val = input("Enter next command: ")
        if val == "quit":
            pyglet.app.exit()
        else:
            try:
                firework = firework_parsing.parse_firework(val)
                if firework is None:
                    print(f'Unrecognised command: {val}', file=sys.stderr)
                    continue
                pyglet.clock.schedule_once(firework, 0)
            except:
                print(f'Parsing error: {val}', file=sys.stderr)
                continue
