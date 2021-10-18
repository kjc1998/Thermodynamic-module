# Mathematical Solvers

## Operator Priority

Mathematical operations were conducted based on priority level set as shown in the table below: <br/> <br/>
| Operator | Descriptions | Priority |
| ----------- | --------------- | ----------- |
| + | Addition | 0 |
| - | Subtraction | 0 |
| \* | Multiplication | 1 |
| / | Division | 1 |
| ^ | Exponent | 2 |

<br/>

> A string that constitutes of multiple operators e.g. `2*3 + 3/4^2 -1` will go through the following steps
>
> `2*3 + 3/4^2 -1` -> `2*3 + 3/16 -1` -> `6 + 0.1875 -1` -> `6 + 0.1875 -1`
>
> **Answer = 5.1875**

> Additionally, bracket terms will yield higher priority and is ranked based on how nested the terms are
>
> `2^2+(2*(1+2))` -> `2^2+(2*3)` -> `2^2+6` -> `4+6`
>
> **Answer = 10**

> ### _Note_&nbsp;&nbsp;:
>
> `-2^2` will yield **-4**, where as `(-2)^2` gives **4**

## Types of Solver

1. [Calculator](#calculator)
2. [Linear](#linear)

---

# Calculator

## Intructions :

1. Initialised `LinearSolver` instance:

```python
test = LinearSolver("1-1-1-1-1-11+2+10/10-2^3")
# call results
print(test.answer) # -19
```

2. To show done to reach that stage, one simply use `linear_get_log` method

```python
# print out steps
test.linear_get_log()
```

# Linear
