from fireworks import basic_firework


def parse_firework(firework_command):
    """
    Given a string, returns a firework object that can be displayed
    :param firework_command: The firework string
    :return: A firework to display
    """
    if firework_command == 'firework':
        return basic_firework.fire
    else:
        return None
