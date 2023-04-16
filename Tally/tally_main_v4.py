# Imports for Interfacing w/ Switcher & Tally
import pyfirmata, time, socket, select, string, sys, re

# Program is code 1
# Preview is code 2

# Globals
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)

#Tally Updates
def updateTally(board, current_program, current_preview):
    # Camera 1
    board.digital[2].write( 1 if current_program == "05" else 0 ) # Program
    board.digital[3].write( 1 if current_preview == "05" else 0 ) # Preview

    # Camera 2
    board.digital[4].write( 1 if current_program == "08" else 0 ) # Program
    board.digital[5].write( 1 if current_preview == "08" else 0 ) # Preview

    # Camera 3
    board.digital[6].write( 1 if current_program == "0e" else 0 ) # Program
    board.digital[7].write( 1 if current_preview == "0e" else 0 ) # Preview

    # Camera 4
    board.digital[8].write( 1 if current_program == "0b" else 0 ) # Program
    board.digital[9].write( 1 if current_preview == "0b" else 0 ) # Preview

    # Camera 5
    board.digital[10].write( 1 if current_program == "0c" else 0 ) # Program
    board.digital[11].write( 1 if current_preview == "0c" else 0 ) # Preview

    # Camera 6
    board.digital[12].write( 1 if current_program == "0d" else 0 ) # Program
    board.digital[13].write( 1 if current_preview == "0d" else 0 ) # Preview



#Swither Updates
def getSwitcher(current_program, current_preview):
	# Send code for Program and Preview
	s.sendall(b"print(injectGVG100command('020041'))\n") # Command for Program
	s.sendall(b"print(injectGVG100command('020042'))\n") # Command for Preview

	time.sleep(0.05)

	data = s.recv(512).decode("utf-8")

	for x in data.split():
		if x.find("0300c1") != -1:
			current_program = x[6:]

		if x.find("0300c2") != -1:
			current_preview = x[6:]

	return current_program, current_preview

def main():
	print("Starting Tally System - v3.1")
	current_program = " "
	current_preview = " "

	previous_program = " "
	previous_preview = " "

	# Connect To Switcher
	host = '192.168.110.32'
	port = 2100

	try :
		s.connect((host, port))
		print ('Connected to Switcher')
	except :
		print ('Switcher Inaccessible')
		sys.exit()

	# Connect To Tally Box
	try :
		board = pyfirmata.Arduino('/dev/cu.usbserial-1420')
		print ('Connected to Tally')
	except :
		print ('Tally Inaccessible')
		sys.exit()

	
	try:
		while True:
			# Get Updated Program and Preview
			current_program, current_preview = getSwitcher(current_program, current_preview)
			print(f"PGM: {current_program}, PVM: {current_preview}")
			
			# Check if Values Have Changed
			if(current_program != previous_program or current_preview != previous_preview):  
				print(f"PGM: {current_program}, PVM: {current_preview}")
				previous_program = current_program
				previous_preview = current_preview
				updateTally()
				time.sleep(0.05)

	except KeyboardInterrupt:
		print ("Received User Interrupt") 

	finally:
		print ("Shutting Down Program") 

if __name__ == '__main__':
	main()