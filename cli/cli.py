import sys

from firework_parsing import firework_parsing

if __name__ == '__main__':
    val = input("Enter your value: ")
    firework = firework_parsing.parse_firework(val)
    if firework is None:
        print(f'Unrecognised command: {val}', file=sys.stderr)
    from window import window
    window.run(firework)
