import hid
import time
import struct

VENDOR_ID = 3095
PRODUCT_ID = 2305

# enumerate USB devices
'''
for d in hid.enumerate():
    keys = list(d.keys())
    keys.sort()
    for key in keys:
        print("%s : %s" % (key, d[key]))
    print()
'''
# try opening a device, then perform write and read

try:
    #print("Opening the device")

    h = hid.device()
    h.open(VENDOR_ID, PRODUCT_ID) # Soundear
    '''
    print("Manufacturer: %s" % h.get_manufacturer_string())
    #print("Product: %s" % h.get_product_string())
    print("Serial No: %s" % h.get_serial_number_string())
    '''
    # enable non-blocking mode
    h.set_nonblocking(1)

    # write some data to the device
    #print("Write the data")
    #h.write([0, 63, 35, 35] + [0] * 61)

    # wait
    time.sleep(0.05)

    # read back the answer
    #print("Read the data")
    while True:
        d = h.read(64)
        if d:
            #print(d)

            dBA_slow_byte_1 = d[12] # sample value = 22
            dBA_slow_byte_2 = d[13] # sample value = 101
            dBA_slow_byte_3 = d[14] # sample value = 64
            dBA_slow_byte_4 = d[15] # sample value = 66

            #print("dB(A)slow byte 1= " + str(dBA_slow_byte_1))
            #print("dB(A)slow byte 2= " + str(dBA_slow_byte_2))
            #print("dB(A)slow byte 3= " + str(dBA_slow_byte_3))
            #print("dB(A)slow byte 4= " + str(dBA_slow_byte_4))

            dBA_slow_byte_1_hex = hex(dBA_slow_byte_1) 
            dBA_slow_byte_2_hex = hex(dBA_slow_byte_2) 
            dBA_slow_byte_3_hex = hex(dBA_slow_byte_3)
            dBA_slow_byte_4_hex = hex(dBA_slow_byte_4)

            #print("dB(A)slow byte 1 hex= " + str(dBA_slow_byte_1_hex)) # sample value = 16
            #print("dB(A)slow byte 2 hex= " + str(dBA_slow_byte_2_hex)) # sample value = 65
            #print("dB(A)slow byte 3 hex= " + str(dBA_slow_byte_3_hex)) # sample value = 40
            #print("dB(A)slow byte 4 hex= " + str(dBA_slow_byte_4_hex)) # sample value = 42

            dBAslow = dBA_slow_byte_4*(16**6) + dBA_slow_byte_3*(16**4) + dBA_slow_byte_2*(16**2) + dBA_slow_byte_1

            dBAslow_hex = hex(dBAslow)[2:]

            #print("dB(A)slow hex= " + str(dBAslow_hex)) # sample value = 42406516

            dBAslow_decimal = str(round(struct.unpack('!f', bytes.fromhex(dBAslow_hex))[0], 1))
            timestamp = str(d[23]) + ":" + str(d[24]) + ":" + str(d[25]) + " "  + str(d[21]) + "-" + str(d[22]) + "-20" + str(d[20])

            print("db(A)slow= " + dBAslow_decimal + ", Timestamp= " + timestamp, end='\r', flush=True)

            time.sleep(1)

        else:
            break

    #print("Closing the device")
except KeyboardInterrupt:
    h.close()

except IOError as ex:
    print(ex)
    print("You probably don't have the hard coded device. Update the hid.device line")
    print("in this script with one from the enumeration list output above and try again.")


#print("Done")


#device = hid.device()
#device.open(VENDOR_ID, PRODUCT_ID)
#print('Connected to Soundear:' + str(PRODUCT_ID))

#device.close()
