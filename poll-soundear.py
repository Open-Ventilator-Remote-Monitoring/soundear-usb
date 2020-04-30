import hid
import time
import struct

def decode_bytes(byte_1, byte_2, byte_3, byte_4):
    bytes_reversed_and_concatenated = byte_4*(16**6) + byte_3*(16**4) + byte_2*(16**2) + byte_1

    bytes_hex = hex(bytes_reversed_and_concatenated)[2:]

    bytes_decimal = str(round(struct.unpack('!f', bytes.fromhex(bytes_hex))[0], 1))

    return bytes_decimal


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

    print("Manufacturer: %s" % h.get_manufacturer_string())
    #print("Product: %s" % h.get_product_string())
    print("Serial No: %s" % h.get_serial_number_string())
    print()

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

            timestamp = str(d[23]) + ":" + str(d[24]) + ":" + str(d[25]) + " "  + str(d[21]) + "-" + str(d[22]) + "-20" + str(d[20])

            dBAslow = decode_bytes(d[12], d[13], d[14], d[15])
            Laeq1s = decode_bytes(d[8], d[9], d[10], d[11])
            dBAfast = decode_bytes(d[4], d[5], d[6], d[7])
            LCpeak = decode_bytes(d[16], d[17], d[18], d[19])
            dBCfast = decode_bytes(d[28], d[29], d[30], d[31])
            dBCslow = decode_bytes(d[32], d[33], d[34], d[35])

            print("db(A)slow= " + dBAslow + ", db(A)fast= " + dBAfast + ", Laeq,1s= " + Laeq1s + ", LCpeak= " + LCpeak + ", dB(C)fast= " + dBCfast + ", dB(C)slow= " + dBCslow  + ", Timestamp= " + timestamp, end='\r', flush=True)

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

