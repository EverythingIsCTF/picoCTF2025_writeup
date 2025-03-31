# Solving the `perplexed` Binary Password Challenge

This document explains how to reverse-engineer the `perplexed` binary to find the correct 27-character password that makes the `check` function return 0, resulting in the "Correct!! :D" message. The solution involves analyzing the binary's logic, understanding its bit comparison mechanism, and constructing the password programmatically.

---

## Introduction

The goal is to determine the exact input string that satisfies the password check in the `perplexed` binary. The binary takes a user-provided string, passes it to the `check` function, and outputs "Correct!! :D" if the function returns 0, or "Nope :(" otherwise. Through analysis (e.g., using `objdump`), we can uncover the logic and derive the password.

---

## Step-by-Step Analysis

### 1. Initial Length Check
The `check` function begins by verifying the length of the input string:
- It calls `strlen` on the input.
- If the length is not exactly 27 characters, it returns 1 (failure).
- **Key Insight**: The password must be precisely 27 characters long.

### 2. Reference Data Setup
The function sets up a hardcoded 23-byte reference sequence on the stack:
- These bytes are loaded explicitly in the assembly code.
- Example bytes (from analysis): `[0xe1, 0xa7, 0x1e, ..., 0xf4]` (full list shown in code below).
- This sequence totals 184 bits (23 bytes × 8 bits per byte), which will be compared to bits from the input.

### 3. Bit Comparison Logic
The function uses nested loops to compare bits:
- **Outer Loop**: Iterates over the 23 reference bytes (controlled by a counter).
- **Inner Loop**: Iterates over the 8 bits of each byte (from MSB to LSB).
- For each reference bit (184 total), it:
  - Computes a position in the input string using two variables (`v1` for bit position, `v2` for byte index).
  - Extracts the corresponding bit from the input.
  - Compares it to the reference bit.
- If any bit mismatches, it returns 1. If all 184 bits match, it returns 0.

### 4. Password Construction
The bit mapping follows a specific pattern:
- `v1` increments from 1 to 7, then resets to 0, while `v2` increments when `v1` resets.
- This creates a sequence of (byte, bit) positions in the input string (e.g., `(0, 6), (0, 5), ..., (1, 7)`).
- We can reverse this process to build the password by setting input bits to match the reference bits.

### 5. Verification
The constructed password must:
- Be 27 characters long.
- Have its bits at the mapped positions match the 184 reference bits.
- Include a newline (`\n`) as the final character, as expected by the binary's input handling.

---

## Solution Code

To automate password construction, we use this Python script:

```python
# Hardcoded 23-byte reference sequence from the binary
reference = [0xe1, 0xa7, 0x1e, 0xf8, 0x75, 0x23, 0x7b, 0x61, 0xb9, 0x9d, 0xfc,
             0x5a, 0x5b, 0xdf, 0x69, 0xd2, 0xfe, 0x1b, 0xed, 0xf4, 0xed, 0x67, 0xf4]

# Extract 184 bits from reference (MSB to LSB)
ref_bits = [((byte >> (7 - j)) & 1) for byte in reference for j in range(8)]

# Simulate the bit mapping sequence
v1, v2 = 0, 0
sequence = []
for i in range(23):
    for v5 in range(8):
        if v1 == 0:
            v1 = 1
        bit_pos = 7 - v1
        sequence.append((v2, bit_pos))
        v1 += 1
        if v1 == 8:
            v1, v2 = 0, v2 + 1

# Initialize 27-byte password array
str_bytes = [0] * 27
for k in range(184):
    v2, bit_pos = sequence[k]
    str_bytes[v2] |= (ref_bits[k] << bit_pos)

# Convert bytes to characters, append newline
password = ''.join(chr(b) for b in str_bytes[:-1]) + '\n'
print(password)