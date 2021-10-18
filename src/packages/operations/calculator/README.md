# How to Use Solver

## Operator Priority

Mathematical operations were conducted based on priority level set as shown in the table below:
| Operator    | Descriptions    | Priority    |
| ----------- | --------------- | ----------- |
| +           | Addition        | 0           |
| -           | Subtraction     | 0           |
| *           | Multiplication  | 1           |
| /           | Division        | 1           |
| ^           | Exponent        | 2           |

A string that constitutes of multiple operators e.g. `2*3 + 3/4^2 -1` will go through the following steps:

`2*3 + 3/4^2 -1` -> `2*3 + 3/16 -1` -> `6 + 0.1875 -1` -> `6 + 0.1875 -1`

##### Answer: 5.1875

Additionally, bracket terms will yield higher priority and is ranked based on how nested the terms are, e.g.

`2^2+(2*(1+2))` -> `2^2+(2*3)` -> `2^2+6` -> `4+6`

##### Answer = 10

## Types of Solver

1. [Calculator](#calculator)
2. [Linear](#linear)

# Calculator

1. Begin with ...

# Linear
