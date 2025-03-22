# Echo Valley - Format String Exploitation

## Challenge Overview

"Echo Valley" is a binary exploitation challenge from picoCTF 2025 where we're given a program that "echoes back whatever you say to it." As the name suggests, the program contains a format string vulnerability that we can exploit to gain arbitrary read and write capabilities.

## Vulnerability Analysis

Based on the exploit script, the program likely has a simple structure:
1. It reads input from the user
2. It echoes back the input using a vulnerable printf-like function without proper formatting
3. It has a hidden `print_flag()` function that we need to call

The vulnerability is a classic format string vulnerability where user input is passed directly to a printf() function:
```c
printf(user_input); // Vulnerable code (instead of printf("%s", user_input))
```

This vulnerability allows us to:
1. Read values from the stack using format specifiers like `%p`
2. Write to arbitrary memory locations using `%n` format specifier

## Exploitation Strategy

Our strategy is:
1. Leak the stack canary, saved RBP, and return address using format string reads
2. Calculate the binary's base address in memory (ASLR bypass)
3. Calculate the address of the `print_flag()` function
4. Use format string write (`%n`) to overwrite the return address with the address of `print_flag()`

## Detailed Explanation of exploit.py

### Initial Setup

The script begins with setup code for either local or remote connection to the target:
```python
# Check for remote or local execution
if args.remote:
    p = remote('shape-facility.picoctf.net', args.port)
else:
    p = process('./valley')
```

### Step 1: Information Leak

The exploit uses format string reads to leak three critical pieces of information:
```python
p.send(b"%19$p\n%20$p\n%21$p\n")
```

These parameter indices (`19$`, `20$`, `21$`) were likely found through testing. They correspond to:
- `19$` - Stack canary (a value used to detect stack overflows)
- `20$` - Saved base pointer (RBP)
- `21$` - Return address (points to code in the binary)

### Step 2: Calculating Addresses

The script uses the leaked return address to calculate:
1. The binary base address (by subtracting the known offset of main's return)
2. The address of the `print_flag()` function (by adding its offset to the base)

```python
base_addr = ret_addr - MAIN_RET_OFFSET
print_flag_addr = base_addr + PRINT_FLAG_OFFSET
```

### Step 3: Format String Write Preparation

The exploit prepares to use a format string write to overwrite the return address:
```python
ret_addr_ptr = saved_rbp - 0x8  # Address where return address is stored
last_4_hex = print_flag_addr & 0xFFFF  # Get the lower 2 bytes
```

### Step 4: Payload Construction

The payload uses two parts:
1. First payload places the address we want to write to (return address location) at the beginning of our input:
   ```python
   payload = p64(ret_addr_ptr) * 3
   ```
   This makes the address accessible through a low-indexed parameter (like `%8$`)

2. Second payload performs the actual write:
   ```python
   next_payload = f"%{decimal_value}c%8$hn"
   ```
   - `%{decimal_value}c` writes exactly that many characters
   - `%8$hn` writes the count of characters printed so far to the address at parameter 8 (our ret_addr_ptr)
   - `hn` means it only writes 2 bytes (partial overwrite technique)

### Final Steps

The exploit sends both payloads and switches to interactive mode to capture the flag.

## Key Exploitation Techniques Used

1. **Format String Leaks**: Using `%p` to read values from the stack
2. **ASLR Bypass**: Calculating the binary base address from a leaked pointer
3. **Format String Write**: Using `%n` variants to perform arbitrary memory writes
4. **Return Address Overwrite**: Redirecting execution to the print_flag() function

This is a classic format string exploitation challenge where we use the vulnerability to both leak information and write to memory, ultimately redirecting program execution to the function that prints the flag.
