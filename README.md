# XORUtils
A script with some common operations used to solve XOR challenges in CTFs.

# How to use XORUtils
## Encrypting/decrypting a file with a key
`python3 xorutils.py <encrypted/plain text file> <--key|-k> <key>`
### Example #1 - regular keys
`python3 xorutils.py plain.txt --key 123456`
### Example #2 - keys with spaces
`python3 xorutils.py plain.txt --key "spaced key"`

## Extracting a XOR key, given an encrypted file and a plain text file
`python3 xorutils.py <encrypted/plain text file> <plain text/encrypted file>`
### Example
`python3 xorutils.py crypt.enc plain.txt`

## Brute-forcing an encrypted file with all possible keys made out of 1 and 2 bytes
This generates a file called <encrypted/plain text file>.bf_res containing the results:

`python3 xorutils.py <encrypted/plain text file> <--brute|-b>`
### Example
This generates a file called crypt.enc.bf_res containing the results:

`python3 xorutils.py crypt.enc --brute`
