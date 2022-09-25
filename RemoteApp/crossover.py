import time
import telnetlib
import sys


class Crossover:
    def __init__(self):
        self.connected = False

        self.current_program = ""
        self.current_preview = ""

        self.desired_input = ""
        self.desired_operation = "None"

        self.pgm_prefix = '0300c1'
        self.pvw_prefix = '0300c2'

        self.crossover_ip = '192.168.110.32'
        self.crossover_port = '2100'

    def read_bus(self, telnet_connection, read_code):
        telnet_connection.write(b"print(injectGVG100command('" + read_code.encode('ascii') + b"'))\n")
        full_program_bus = str(telnet_connection.read_until(b"gvg100> "))

        if "0300c" in full_program_bus:
            cleaned_bus = full_program_bus[full_program_bus.find("0300c"):full_program_bus.find("0300c")+8]
            return cleaned_bus
        else:
            print("\tFailed to get bus: shutting down")
            exit()

    def send_command(self, telnet_connection, command):
        telnet_connection.write(b"print(injectGVG100command('" + command.encode('ascii') + b"'))\n")
        validation = telnet_connection.read_until(b"gvg100> ")

        if validation[0:4] == b'0180':
            print("\tSuccessful switch")
        elif validation[0:4] == b'0140':
            print("\tFailed to switch")
        else:
            print("\tUnknown Result")

    def remote_switch(self, desired_input, desired_operation):  # Number, 'cut' or 'autotrans'
        self.desired_input = desired_input
        self.desired_operation = desired_operation

        try:
            with telnetlib.Telnet(self.crossover_ip, self.crossover_port, 1) as telnet_connection:
                self.connected = True
                telnet_connection.read_until(b"gvg100> ")

                self.current_program = self.read_bus(telnet_connection, "020041")
                self.current_preview = self.read_bus(telnet_connection, "020042")

                print(f"\tPV: {self.current_preview}, PGM: {self.current_program}, DS: {self.desired_input}")

                switch_delay = 0.05
                switch_code = ""
                if self.desired_operation == "cut":
                    switch_code = '0300fb4a'
                elif self.desired_operation == "autotrans":
                    switch_code = '0300fb0b'
                    switch_delay = 1.05

                if self.current_program == desired_input:
                    print("\tNo switch Needed")
                    return

                elif self.current_preview == desired_input:
                    print("\tPerform Operation")
                    
                    self.send_command(telnet_connection, switch_code)

                elif self.current_program != desired_input:
                    print("\tNeed to set preview")
                    self.send_command(telnet_connection, self.pvw_prefix + desired_input)
                    self.send_command(telnet_connection, switch_code)

                time.sleep(switch_delay)
                telnet_connection.close()
        except telnetlib.socket.timeout:
            self.connected = False
            print("\tAttempted a Switch but Switcher Not Connected")


        except:
            print(f"\n --------------------------------------------------------------")
            print(f"Programmed & Corey is Sad :( \n Error: {sys.exc_info()[0]}")
            print(f"\n --------------------------------------------------------------")
            exit()
