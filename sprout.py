import random

class SproutCipher:
    def __init__(self, key, iv):
        self.nlfsr = [int(x) for x in list(iv[:40])]
        self.lfsr = [int(x) for x in list(iv[40:]) + [1]*9 + [0]]
        self.key = [int(x) for x in list(key)]
        self.counter = 0

    def nonlinear_filter(self, x):
        return (x[0] + x[1] + x[2]) % 2

    def counter_function(self):
        self.counter = (self.counter + 1) % 512
        return (self.counter >> 2) % 40

    def round_key(self, index):
        return self.key[index]

    def key_initialization(self):
        for i in range(320):
            nlfsr_out = self.nlfsr[0]
            lfsr_out = self.lfsr[0]
            
            index = self.counter_function()
            round_key_bit = self.round_key(index)
            
            feedback_bit = self.nonlinear_filter([nlfsr_out, lfsr_out, round_key_bit])
            
            self.nlfsr = [feedback_bit] + self.nlfsr[:-1]
            self.lfsr = [feedback_bit] + self.lfsr[:-1]

    def keystream_generation(self):
        keystream = []
        for i in range(320):
            nlfsr_out = self.nlfsr[0]
            lfsr_out = self.lfsr[0]
            
            index = self.counter_function()
            round_key_bit = self.round_key(index)
            
            feedback_bit = self.nonlinear_filter([nlfsr_out, lfsr_out, round_key_bit])
            
            keystream_bit = (nlfsr_out + lfsr_out + round_key_bit) % 2
            keystream.append(keystream_bit)
            
            self.nlfsr = [feedback_bit] + self.nlfsr[:-1]
            self.lfsr = [feedback_bit] + self.lfsr[:-1]
        
        return keystream

def encrypt(plaintext, key, iv):
    plaintext = ''.join(['{0:08b}'.format(ord(c)) for c in plaintext])
    cipher = SproutCipher(key, iv)
    cipher.key_initialization()
    keystream = ''
    while len(keystream) < len(plaintext):
        keystream += ''.join(map(str,cipher.keystream_generation()))
    ciphertext = []
    for i in range(len(plaintext)):
        ciphertext.append(int(plaintext[i]) ^ int(keystream[i]))
    return ''.join([str(c) for c in ciphertext])

def decrypt(ciphertext, key, iv):
    cipher = SproutCipher(key, iv)
    cipher.key_initialization()
    keystream = ''
    while len(keystream) < len(ciphertext):
        keystream += ''.join(map(str,cipher.keystream_generation()))
    ciphertext = [int(c) for c in ciphertext]
    plaintext = []
    for i in range(len(ciphertext)):
        plaintext.append(ciphertext[i] ^ int(keystream[i]))
    plaintext = ''.join([str(c) for c in plaintext])
    decrypted_text = ''.join([chr(int(plaintext[i:i+8], 2)) for i in range(0, len(plaintext), 8)])
    return decrypted_text

# Example usage
key = ''.join([str(random.randint(0, 1)) for _ in range(40)])
iv = ''.join([str(random.randint(0, 1)) for _ in range(70)])
plaintext = "Capra crapa piatra, piatra crapa-n patru."
print("Plaintext:", plaintext)

ciphertext = encrypt(plaintext, key, iv)
print("Ciphertext:",ciphertext)

decrypted_text = decrypt(ciphertext, key, iv)
print("Decrypted Text:", decrypted_text)