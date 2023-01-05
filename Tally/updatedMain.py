import asyncio, telnetlib3, pyfirmata

crossover_ip = '192.168.110.32'
crossover_port = '2100'

board = pyfirmata.Arduino('/dev/cu.usbserial-1420')


async def shell(reader, writer):
    current_program = ""
    current_preview = ""

    previous_program = ""
    previous_preview = ""


    while True:
        writer.write("print(injectGVG100command('020041'))\n")
        pgm = await reader.readline()
        current_program = pgm[pgm.find("> ") + 2:-1]

        writer.write("print(injectGVG100command('020042'))\n")
        pvw = await reader.readline()
        current_preview = pvw[pvw.find("> ") + 2:-1]

        if(current_program != previous_program or current_preview != previous_preview):  
            previous_program = current_program
            previous_preview = current_preview
            await updateTally(current_program, current_preview)


async def updateTally(current_program, current_preview):
    # Camera 1
    board.digital[2].write( 1 if current_program == "0300c105" else 0 ) # Program
    board.digital[3].write( 1 if current_preview == "0300c205" else 0 ) # Preview

    # Camera 2
    board.digital[4].write( 1 if current_program == "0300c108" else 0 ) # Program
    board.digital[5].write( 1 if current_preview == "0300c208" else 0 ) # Preview

    # Camera 3
    board.digital[6].write( 1 if current_program == "0300c10e" else 0 ) # Program
    board.digital[7].write( 1 if current_preview == "0300c20e" else 0 ) # Preview

    # Camera 4
    board.digital[8].write( 1 if current_program == "0300c10b" else 0 ) # Program
    board.digital[9].write( 1 if current_preview == "0300c20b" else 0 ) # Preview

    # Camera 5
    board.digital[10].write( 1 if current_program == "0300c10c" else 0 ) # Program
    board.digital[11].write( 1 if current_preview == "0300c20c" else 0 ) # Preview

    # Camera 6
    board.digital[12].write( 1 if current_program == "0300c10d" else 0 ) # Program
    board.digital[13].write( 1 if current_preview == "0300c20d" else 0 ) # Preview

async def tallyTask():
    print("Starting Tally Updates")
    if(current_program != previous_program or current_preview != previous_preview):  
        print("Update")
        previous_program = current_program
        previous_preview = current_preview
        await updateTally()
        await asyncio.sleep(0.1)

if __name__ == '__main__':
    print ("Starting Telnet Client")
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        coro = telnetlib3.open_connection('192.168.110.32', 2100, shell=shell)
        
        reader, writer = loop.run_until_complete(coro)
        loop.run_until_complete(writer.protocol.waiter_closed)

    except KeyboardInterrupt:
        pass

    finally:
        print ("Shutting Down Program")        