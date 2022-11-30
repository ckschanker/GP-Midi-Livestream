#!/usr/bin/env python3

import pyfirmata
import time
import telnetlib
import sys

class Tally:
    def __init__(self):
        self.connected = False

        self.current_program = ""
        self.current_preview = ""

        self.previous_program = "null"
        self.previous_preview = "null"

        self.pgm_prefix = '0300c1'
        self.pvw_prefix = '0300c2'

        self.crossover_ip = '192.168.110.32'
        self.crossover_port = '2100'
        
        self.board = pyfirmata.Arduino('/dev/cu.usbserial-1420')
        print("Communication Successfully started")

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

    def led(self):
        # Camera 1
        if(self.current_program == self.pgm_prefix+"05"):
            print("Cam 1 On")
            self.board.digital[2].write(0)
            self.board.digital[3].write(1)
        elif(self.current_preview == self.pvw_prefix+"05"):
            print("Cam 1 Preview")
            self.board.digital[2].write(1)
            self.board.digital[3].write(0)
        else:
            self.board.digital[2].write(0)
            self.board.digital[3].write(0)

        # Camera 2
        if(self.current_program == self.pgm_prefix+"08"):
            print("Cam 2 On")
            self.board.digital[4].write(0)
            self.board.digital[5].write(1)
        elif(self.current_preview == self.pvw_prefix+"08"):
            print("Cam 2 Preview")
            self.board.digital[4].write(1)
            self.board.digital[5].write(0)
        else:
            self.board.digital[4].write(0)
            self.board.digital[5].write(0)

        # Camera 3
        if(self.current_program == self.pgm_prefix+"0e"):
            print("Cam 3 On")
            self.board.digital[6].write(0)
            self.board.digital[7].write(1)
        elif(self.current_preview == self.pvw_prefix+"0e"):
            print("Cam 3 Preview")
            self.board.digital[6].write(1)
            self.board.digital[7].write(0)
        else:
            self.board.digital[6].write(0)
            self.board.digital[7].write(0)

        # Camera 4
        if(self.current_program == self.pgm_prefix+"0b"):
            print("Cam 4 On")
            self.board.digital[8].write(0)
            self.board.digital[9].write(1)
        elif(self.current_preview == self.pvw_prefix+"0b"):
            print("Cam 4 Preview")
            self.board.digital[8].write(1)
            self.board.digital[9].write(0)
        else:
            self.board.digital[8].write(0)
            self.board.digital[9].write(0)

        # Camera 5
        if(self.current_program == self.pgm_prefix+"0c"):
            print("Cam 5 On")
            self.board.digital[10].write(0)
            self.board.digital[11].write(1)
        elif(self.current_preview == self.pvw_prefix+"0c"):
            print("Cam 5 Preview")
            self.board.digital[10].write(1)
            self.board.digital[11].write(0)
        else:
            self.board.digital[10].write(0)
            self.board.digital[11].write(0)

        # Camera 6
        if(self.current_program == self.pgm_prefix+"0d"):
            print("Cam 6 On")
            self.board.digital[12].write(0)
            self.board.digital[13].write(1)
        elif(self.current_preview == self.pvw_prefix+"0d"):
            print("Cam 6 Preview")
            self.board.digital[12].write(1)
            self.board.digital[13].write(0)
        else:
            self.board.digital[12].write(0)
            self.board.digital[13].write(0)




    def update(self):  # Number, 'cut' or 'autotrans'
        try:
            with telnetlib.Telnet(self.crossover_ip, self.crossover_port, 1) as telnet_connection:
                self.connected = True
                telnet_connection.read_until(b"gvg100> ")

                self.current_program = self.read_bus(telnet_connection, "020041")
                self.current_preview = self.read_bus(telnet_connection, "020042")

                if(self.current_program != self.previous_program or self.current_preview != self.previous_preview):
                    print(f"Input Change to {self.current_program} & {self.current_preview}")
                    self.previous_program = self.current_program
                    self.previous_preview = self.current_preview
                    self.led()
                
                telnet_connection.close()
        except telnetlib.socket.timeout:
            self.connected = False
            print("\tAttempted a Switch but Switcher Not Connected")


        # except:
        #     print(f"\n --------------------------------------------------------------")
        #     print(f"Programmed & Corey is Sad :( \n Error: {sys.exc_info()[0]}")
        #     print(f"\n --------------------------------------------------------------")
        #     exit()

if __name__ == '__main__':
    tally = Tally()

    while True:
        tally.update()
