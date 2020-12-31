from fireworks import basic_firework, text_firework, tracer


def parse_firework(firework_command):
    """
    Given a string, returns a firework object that can be displayed
    :param firework_command: The firework string
    :return: A firework to display
    """

    bits = firework_command.split()

    if firework_command == 'continuous_firework':
        return basic_firework.fire
    elif bits[0] == 'firework':
        num_times = int(bits[1]) if len(bits)>1 else 1
        return lambda dt: basic_firework.fire_N(num_times, dt)
    elif bits[0] == 'text':
        return lambda dt: text_firework.fire(" ".join(bits[1:]))
    elif bits[0] == 'rocket':
        return tracer.rocket
    else:
        return None
