# HOWTO put this script to compared files directory and run
# python bytesComparator.py
import os
import csv

path = os.path.dirname(os.path.abspath(__file__))
# bytes = [[offset,length,2nd_format]]
bytes = [[0x0ef2, 4, 'ascii'],
         [0xae, 2, 'none'],
         [0xB2, 2, 'dec'], [0xB4, 2, 'dec'], [0x60, 2, 'dec'],
         [0xb6, 1, 'bin'], [0xb7, 1, 'bin'],
         [0xad, 1, 'bin'],
         [0xa4, 3, 'none'],
         [0xcb, 5, 'none']]
out = 'out.csv'

output = os.path.join(path, out)
fo = open(output, "w")
with open(output, 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=';', quotechar='|',
                            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    array = []
    array.append('filename')
    for b in bytes:
        array.append('0x' + ("%02x" % b[0]))
        if b[2] != 'none':
            array.append(b[2])
    filewriter.writerow(array)
    for file in os.listdir(path):
        if file.lower().endswith('.bin'):
            current = os.path.join(path, file)
            if os.path.isfile(current):
                fi = open(current, "rb")
                array = []
                array.append(os.path.basename(current))
                for b in bytes:
                    fi.seek(b[0])
                    data = fi.read(b[1])
                    hex = data.hex()
                    num = int.from_bytes(data, 'little')
                    #array.append('0x' + ("%02x" % num).zfill(2*b[1]))
                    array.append('0x' + hex)
                    if b[2] == 'bin':
                        array.append(bin(num)[2:].zfill(8*b[1]))
                    if b[2] == 'dec':
                        array.append(str(num))
                    if b[2] == 'ascii':
                        array.append(data.decode('ascii'))
                filewriter.writerow(array)
                fi.close()
fo.close()
