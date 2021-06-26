#!/usr/bin/env python3

''' A script with some common operations used to solve XOR challenges in CTFs. '''

import sys

def print_help():
    ''' Outputs how to use the script. '''
    print('Usage: %s <encrypted/plain text file> <plain text/encrypted file>, or' % sys.argv[0])
    print('       %s <encrypted/plain text file> <--key|-k> <key>' % sys.argv[0])
    print('       %s <encrypted/plain text file> <--brute|-b>' % sys.argv[0])
    sys.exit(1)

def extract_key(res):
    ''' Extracts the key from the string obtained from XORing two files. '''
    # c_key: candidate key
    c_key = res

    # pck_a: partial ck array
    pck_a = []

    i = -1

    while i == -1 and len(c_key) > 0:
        i = (c_key+c_key).find(c_key, 1, -1)

        if i == -1:
            pck_a.append(c_key[-1])
        c_key = c_key[:-1]

    pck = ''.join(pck_a)[::-1]

    if len(c_key) > 0 and c_key.find(pck) != -1:
        return c_key[:i]

    return res

def xor_two_files():
    ''' XORs two files. '''
    input_files = [sys.argv[1], sys.argv[2]]
    key_a = []  # _a: array

    try:
        f_if = open(input_files[0], 'rb')   # f_if: first input file
    except FileNotFoundError:
        sys.exit('No such file or directory: \'%s\'' % input_files[0])

    try:
        g_if = open(input_files[1], 'rb')
    except FileNotFoundError:
        sys.exit('No such file or directory: \'%s\'' % input_files[1])

    while True:
        f_ch = f_if.read(1)
        g_ch = g_if.read(1)

        if not f_ch or not g_ch:
            break

        f_ch_asc = ord(f_ch)
        g_ch_asc = ord(g_ch)

        key_a.append(chr(f_ch_asc^g_ch_asc))

    result = ''.join(key_a)
    key = extract_key(result)
    print(key)

    f_if.close()
    g_if.close()

def xor_file_with_key():
    ''' XORs a file with a key. '''
    input_file = sys.argv[1]
    key = sys.argv[3]
    text = []
    i = 0

    try:
        f_if = open(input_file, 'rb')
    except FileNotFoundError:
        sys.exit('No such file or directory: \'%s\'' % input_file)

    while True:
        f_ch = f_if.read(1)
        j = i%len(key)

        if not f_ch:
            break

        key_ch_asc = ord(key[j])
        f_ch_asc = ord(f_ch)

        # print(f_ch, f_ch_asc, key[j], key_ch_asc, chr(f_ch_asc^key_ch_asc), f_ch_asc^key_ch_asc)

        text.append(chr(f_ch_asc^key_ch_asc))
        i += 1

    print(''.join(text), end='')

    f_if.close()

def xor_brute_force():
    ''' XORs a file with all possible strings made out of 2 bytes. '''
    input_file = sys.argv[1]

    try:
        f_if = open(input_file, 'rb')
    except FileNotFoundError:
        sys.exit('No such file or directory: \'%s\'' % input_file)

    f_content = f_if.read()
    f_if.close()

    g_if = open(input_file+'.bf_res', 'wb')

    for i in range(65536):
        text = []

        if i > 255:
            j = 0

            msb = i//256
            lsb = i%256

            for ch_asc in f_content:
                if j%2 == 0:
                    text.append(chr(ch_asc^msb))
                else:
                    text.append(chr(ch_asc^lsb))
                j += 1
        else:
            for ch_asc in f_content:
                text.append(chr(ch_asc^i))

        out = hex(i)+': '+''.join(text)+'\n'
        g_if.write(out.encode('utf-8'))

    g_if.close()

if __name__ == '__main__':
    if len(sys.argv) not in [3, 4]:
        print_help()

    elif len(sys.argv) == 3:
        if sys.argv[2] not in ['--brute', '-b']:
            xor_two_files()
        else:
            xor_brute_force()

    elif len(sys.argv) == 4:
        if sys.argv[2] not in ['--key', '-k']:
            print('Invalid syntax')
            print_help()

        xor_file_with_key()
