from fireworks import basic_firework, text_firework, tracer, sphere_firework

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

    basic_func = {'firework': basic_firework.fire_one,
                  'text':     lambda dt: text_firework.fire(" ".join(bits)),
                  'rocket':   tracer.rocket,
                  'sphere':   sphere_firework.fire,
            }.get(func_name)

    if basic_func:
        return lambda dt: repeat(basic_func, n, dt)

def repeat(fn, N, dt):
    for i in range(min(N, 100)):
        fn(dt)
