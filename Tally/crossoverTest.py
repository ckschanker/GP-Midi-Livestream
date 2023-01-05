import asyncio, telnetlib3

async def shell(reader, writer):
    while True:
        writer.write("print(injectGVG100command('020041'))\n")
        outp = await reader.readline()
        print(outp[outp.find("> ") + 2:-1], flush=True)

        writer.write("print(injectGVG100command('020042'))\n")
        outp = await reader.readline()
        print(outp[outp.find("> ") + 2:-1], flush=True)

        await asyncio.sleep(0.1)


    # EOF
    print()




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