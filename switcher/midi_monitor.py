import yaml
from simplecoremidi import MIDIDestination


class Midi:
    def __init__(self):
        try:
            self.configuration = yaml.safe_load(open("configuration.yaml"))

            self.midi_destination = MIDIDestination("midi_crossover_relay")
            self.midi_input = self.midi_destination.recv()
        except:
            print("Error: Didn't Load Midi Destination")

    def check_midi(self):
        try:
            self.midi_input = self.midi_destination.recv()
            if self.midi_input:
                for key, values in self.configuration.items():
                    if key != "HOST_IP" and key != "HOST_PORT":
                        if str(self.midi_input) == values['midi_cue_cut']:
                            print(f"Receviced: {self.midi_input}, Cutting to: {values['name']}")
                            return values["crossover_code"], "cut"
                        elif str(self.midi_input) == values['midi_cue_autotrans']:
                            print(f"Receviced: {self.midi_input}, Transitioning to: {values['name']}")
                            return values["crossover_code"], "autotrans"
                print("Error: Could Not Find Crossover Value for MIDI Value")
            return False, False

        except:
            print("Error: Could Not Find Crossover Value")
            return False, False
