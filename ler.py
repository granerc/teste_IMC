import struct

arq = 'dados.bin'
form = '30s 11s 4s f f i'
tam = struct.calcsize(form)

if __name__ == '__main__':
    with open(arq, 'rb') as f:
        while True:
            record_data = f.read(tam)
            if not record_data:
                break
            record = struct.unpack(form, record_data)
            string1 = record[0].decode().strip('\x00')
            string2 = record[1].decode().strip('\x00')
            string3 = record[2].decode().strip('\x00')
            float1 = record[3]
            float2 = record[4]
            integer = record[5]
            print(f"String1: {string1}")
            print(f"String2: {string2}")
            print(f"String3: {string3}")
            print(f"Float1: {float1}")
            print(f"Float2: {float2}")
            print(f"Target: {integer}")
            print()