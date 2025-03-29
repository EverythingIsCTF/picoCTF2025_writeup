# EVEN RSA CAN BE BROKEN??

## Challenge Information
- **Category:** Crypto
- **Description:** This service provides you an encrypted flag. Can you decrypt it with just N & e? Connect to the program with netcat: ```$ nc verbal-sleep.picoctf.net 51434``` The program's source code can be downloaded here.
- **Hints:** 
    - How much do we trust randomness?
    - Notice anything interesting about N?
    - Try comparing N across multiple requests

## Analysis

Let's determine the parameters:

```cmd
$ nc verbal-sleep.picoctf.net 51434
N: 15956406145787045697045836875872205963351137069379098306075049231425780726092381593192489624682718392952485959590857931900862464349656345859605041845071886
e: 65537
cyphertext: 15424440168528358995286123614851011350015209432001800630444797091190078867982876803870765184208807547755974974623583704791108443351513009891970935033143305
```

The security of RSA depends on the difficulty of factoring  
$$ N = p \cdot q $$  
into its two prime factors.

Observing that N is even, we can infer that one of the primes is 2—a perfect match for the challenge title!

$$
\begin{aligned}
p &= 2\\[5pt]
q &= N/2\\[5pt]
\phi_N &= (p-1)(q-1)\\[5pt]
       &= q - 1
\end{aligned}
$$

Given that \( e = 65537 \), we calculate the decryption key as:
$$
d = \text{inverse\_mod}(e, \phi_N)
$$  
Then, the plaintext is recovered by computing:
$$
\text{plaintext} = \text{pow}(\text{ciphertext}, d, N)
$$

```python
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
```

Thus, we obtain the flag:

`picoCTF{tw0_1$_pr!m381772be5}`