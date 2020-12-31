from fireworks import basic_firework, text_firework, tracer


def parse_firework(firework_command):
    """
    Given a string, returns a firework object that can be displayed
    :param firework_command: The firework string
    :return: A firework to display
    """

    bits = firework_command.split()

    basic_func = None

    if firework_command == 'continuous_firework':
        return basic_firework.fire
    elif bits[0] == 'firework':
        basic_func = basic_firework.fire_one
    elif bits[0] == 'text':
        basic_func = lambda dt: text_firework.fire(" ".join(bits[1:]))
    elif bits[0] == 'rocket':
        basic_func = tracer.rocket
    else:
        basic_func = None

    if basic_func:
        n = 1
        try:
            n = int(bits[-1]) if len(bits)>1 else 1
        except:
            pass
        return lambda dt: repeat(basic_func, n, dt)

def repeat(fn, N, dt):
    for i in range(min(N, 100)):
        fn(dt)