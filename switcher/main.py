import time

from crossover import Crossover
from midi_monitor import Midi

def main():
    switcher = Crossover()
    midi_monitor = Midi()

    print("Starting Midi Monitor V2 - Fixed Switcher Reboot Issue")

    while True:
        desired_input, desired_operation = midi_monitor.check_midi()

        if desired_input:
            switcher.remote_switch(desired_input, desired_operation)
            time.sleep(0.2)
            print()


if __name__ == '__main__':
    main()
