# Imports for Interfacing w/ Switcher & Tally
import pyfirmata, time, socket, select, string, sys, re



# Globals
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)

# board = None

#Tally Updates
# def updateTally():
#     # Camera 1
#     board.digital[2].write( 1 if current_program == "0300c105" else 0 ) # Program
#     board.digital[3].write( 1 if current_preview == "0300c205" else 0 ) # Preview

#     # Camera 2
#     board.digital[4].write( 1 if current_program == "0300c108" else 0 ) # Program
#     board.digital[5].write( 1 if current_preview == "0300c208" else 0 ) # Preview

#     # Camera 3
#     board.digital[6].write( 1 if current_program == "0300c10e" else 0 ) # Program
#     board.digital[7].write( 1 if current_preview == "0300c20e" else 0 ) # Preview

#     # Camera 4
#     board.digital[8].write( 1 if current_program == "0300c10b" else 0 ) # Program
#     board.digital[9].write( 1 if current_preview == "0300c20b" else 0 ) # Preview

#     # Camera 5
#     board.digital[10].write( 1 if current_program == "0300c10c" else 0 ) # Program
#     board.digital[11].write( 1 if current_preview == "0300c20c" else 0 ) # Preview

#     # Camera 6
#     board.digital[12].write( 1 if current_program == "0300c10d" else 0 ) # Program
#     board.digital[13].write( 1 if current_preview == "0300c20d" else 0 ) # Preview



#Swither Updates
def getSwitcher(current_program, current_preview):
	#Get Program
	s.sendall(b"print(injectGVG100command('020041'))\n")
	time.sleep(0.01)
	data = s.recv(256).decode("utf-8")

	for x in data.split():
		if x.find("0300c1") != -1:
			current_program = x
			break

	# Get Preview
	s.sendall(b"print(injectGVG100command('020042'))\n")
	time.sleep(0.01)
	data = s.recv(256).decode("utf-8")
	for x in data.split():
		if x.find("0300c2") != -1:
			current_preview = x
			break
	return current_program, current_preview

def main():
	print("Starting Tally System - v3.0")
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
	# try :
	# 	board = pyfirmata.Arduino('/dev/cu.usbserial-1420')
	# 	print ('Connected to Tally')
	# except :
	# 	print ('Tally Inaccessible')
	# 	sys.exit()

	
	try:
		while True:
			# Get Updated Program and Preview
			current_program, current_preview = getSwitcher(current_program, current_preview)
			print(f"PGM: {current_program}, PVM: {current_preview}")
			
			# Check if Values Have Changed
			# if(current_program != previous_program or current_preview != previous_preview):  
			# 	print(f"PGM: {current_program}, PVM: {current_preview}")
			# 	previous_program = current_program
			# 	previous_preview = current_preview
			# 	#updateTally()
			# 	time.sleep(0.1)

	except KeyboardInterrupt:
		print ("Received User Interrupt") 

	finally:
		print ("Shutting Down Program") 

if __name__ == '__main__':
	main()