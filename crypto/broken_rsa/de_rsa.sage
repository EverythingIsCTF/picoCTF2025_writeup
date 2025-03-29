# Sage code

# Given values
n  = 15956406145787045697045836875872205963351137069379098306075049231425780726092381593192489624682718392952485959590857931900862464349656345859605041845071886
ct = 15424440168528358995286123614851011350015209432001800630444797091190078867982876803870765184208807547755974974623583704791108443351513009891970935033143305
e  = 65537

# Since n = p * q, and p = 2, then q = n/2
p = 2
q = n // p

# Euler’s totient φ(n) = (p - 1)(q - 1), but p = 2 => (2-1)(q-1) = q - 1
phi_n = q - 1

# Find d = e^(-1) mod φ(n)
d = inverse_mod(e, phi_n)

# Decrypt by computing ct^d mod n
pt = pow(ct, d, n)

# Convert the numeric plaintext into hex
pt_hex = hex(pt)[2:]         # remove leading "0x"
if len(pt_hex) % 2 == 1:
    pt_hex = '0' + pt_hex    # ensure even length for proper byte conversion

# Convert hex to bytes, and decode as UTF-8
pt_bytes  = bytes.fromhex(pt_hex)
try:
    pt_text = pt_bytes.decode('utf-8')
except UnicodeDecodeError:
    pt_text = pt_bytes

print(pt_text)