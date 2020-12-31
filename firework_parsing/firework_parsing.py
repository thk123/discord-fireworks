from fireworks import basic_firework, text_firework, tracer


def parse_firework(firework_command):
    """
    Given a string, returns a firework object that can be displayed
    :param firework_command: The firework string
    :return: A firework to display
    """

    bits = firework_command.strip().split()

    basic_func = None

    n = None
    func_name = None
    try:
        n = int(bits[0])
        func_name = bits[1]
        bits = bits[2:]
    except:
        n = 1
        func_name = bits[0]
        bits = bits[1:]
    func_name = func_name.lower()

    if firework_command == 'continuous_firework':
        return basic_firework.fire
    elif func_name == 'firework':
        basic_func = basic_firework.fire_one
    elif func_name == 'text':
        basic_func = lambda dt: text_firework.fire(" ".join(bits))

    elif func_name == 'rocket':
        basic_func = tracer.rocket
    else:
        basic_func = None

    if basic_func:
        return lambda dt: repeat(basic_func, n, dt)

def repeat(fn, N, dt):
    for i in range(min(N, 100)):
        fn(dt)