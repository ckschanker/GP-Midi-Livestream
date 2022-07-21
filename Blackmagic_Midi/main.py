import time
import sys
import socket
from simplecoremidi import MIDIDestination

blackmagic_ip = "192.168.110.097"
blackmagic_port = 9993

def send_blackmagic(command):
    try:
    # connect socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((blackmagic_ip,blackmagic_port))

        # Recalls a scene
        command += '\r\n'
        s.sendall(command.encode())

        # receive a message and closing socket
        s.recv(1500)
        s.close()
        return 0

    except socket.timeout as err:
        s.close()
        print ("Couldn't Connect to Blackmagic")
        return 1

    except OSError as err:
        s.close()
        print ("Network Issue")
        return 1
        


def main():
    print("Starting Blackmagic Midi")
    midi_destination = MIDIDestination("midi_blackmaigc")

    while True:
        midi_input = midi_destination.recv()
        if midi_input:
            print(f"Received Input: {midi_input}")

            #TF 5 Commands
            if midi_input[0] == 144:
                if midi_input[1] == 0:
                    result = send_blackmagic("record")
                    
                    if result == 0:
                        print(f"Sending Command to Start Recodring")

                elif midi_input[1] == 1:
                    result = send_blackmagic("stop")
                    
                    if result == 0:
                        print(f"Sending Command to Stop Recodring")

        time.sleep(0.1)

    print("Program Shut Down")


if __name__ == '__main__':
    main()
