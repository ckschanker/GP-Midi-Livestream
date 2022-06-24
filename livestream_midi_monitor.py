import time
import sys
import socket
from simplecoremidi import MIDIDestination

tf5_ip = "192.168.0.128"
tf5_port = 49280

def send_tf5(command):
    try:
        # connect socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((tf5_ip,tf5_port))

        # Recalls a scene
        s.sendall(command.encode())

        # receive a message and closing socket
        s.recv(1500)
        s.close()
        return 0

    except socket.timeout as err:
        s.close()
        print ("Couldn't Connect to TF5")
        return 1

    except OSError as err:
        s.close()
        print ("Network Issue")
        return 1
        


def main():
    midi_destination = MIDIDestination("midi_livestream")

    while True:
        midi_input = midi_destination.recv()
        if midi_input:
            print(f"Received Input: {midi_input}")

            #TF 5 Commands
            if midi_input[0] == 144:
                if midi_input[1] == 0:
                    result = send_tf5("ssrecall_ex scene_a " + str(midi_input[2]) + "\n")
                    
                    if result == 0:
                        print(f"Sending Command to Change to Scene {midi_input[2]} A")

                elif midi_input[1] == 1:
                    result = send_tf5("ssrecall_ex scene_b " + str(midi_input[2]) + "\n")
                    
                    if result == 0:
                        print(f"Sending Command to Change to Scene {midi_input[2]} B")

        time.sleep(0.1)

    print("Program Shut Down")


if __name__ == '__main__':
    main()
