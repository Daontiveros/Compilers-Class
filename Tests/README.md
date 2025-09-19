# Homework (Working with CFGs)

## Setup

Copy the "Tests" folder inside the bril folder

## Test Cases

First case is a simple bril program with a loop

```sh
@main {
  v: int = const 4; 
  jmp .somewhere;   
  v: int = const 2; 
.somewhere:         
  print v; 
  x: int = const 2;          
.here:              
  print v;   
  jmp .somewhere;   
}
```

Second bril program is not reducible
```sh
@main {
  v: int = const 4; 
  br cond .loop1 .loop2
  print v;
.loop1:
  print v;
.loop2:
  print v;
.merge:
  jmp .loop1;
}
```

## How to run it

Go inside the "Tests" folder

Run the command:
```sh
bril2json < loop.bril | python3 ex4.py
```

Output should be:
```sh
CFG:  {0: [1], 1: [3], 2: [3], 3: [4], 4: [5], 5: [6], 6: [7], 7: [8], 8: [3]}
{0: 0, 1: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7}
[0, 1, 3, 4, 5, 6, 7, 8]
[(8, 3)]
Is reducible? True
```
Run the command:
```sh
bril2json < second.bril | python3 ex4.py
```

Output should be:
```sh
CFG:  {0: [1], 1: [2, 4], 2: [3], 3: [4], 4: [5], 5: [6], 6: [7], 7: [2]}
{0: 0, 1: 1, 2: 2, 4: 2, 3: 3, 5: 3, 6: 4, 7: 5}
[0, 1, 2, 3, 4, 5, 6, 7]
[(7, 2)]
Is reducible? False
```
## What does the output show?
1. The CFG
2. Shortest Path Length node: distance from entry
   (Please note that each instruction is a node, including .somewhere, .loop1 (from bril code))
   (@main is not an instruction)
3. Reverse postorder
4. Back edges
5. If it is reducible
