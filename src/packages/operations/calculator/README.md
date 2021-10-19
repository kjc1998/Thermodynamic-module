# Mathematical Solvers

## How to Use

Download the two .py files and import math_linear.py to use the solvers

_(Installable packages - WIP)_

## Key Points

Mathematical operations were conducted based on priority level set as shown in the table below: <br/>
| Operator | Descriptions | Priority |
| ----------- | --------------- | ----------- |
| + | Addition | 0 |
| - | Subtraction | 0 |
| \* | Multiplication | 1 |
| / | Division | 1 |
| ^ / \*\* | Exponent | 2 |

<br/>

Special Constants & Functions : <br/>
| Symbol | Descriptions | Type |
| ----------- | --------------- | --- |
| exp | Exponential | Constant |
| pi | π | Constant |
| sin | Sine | Function |
| cos | Cosine | Function |
| tan | Tangent | Function |
| asin | Arcsine | Function |
| acos | Arccosine | Function |
| atan | Arctangent | Function |
| sqrt | Square Root | Function |
| log10 | Log Base 10 | Function |
| ln | Natural Logarithm | Function |

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
> - `-2^2` will yield **-4**, where as `(-2)^2` gives **4**
> - `2^2^3` does not give any priority to any two values, i.e. **(`4^3` or `2^8`)** <br/>Keep it as a rule of thumb to always define exponent terms using brackets

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

2. To show steps done to reach that stage, one simply use `linear_get_log` method

```python
# print out steps
test.linear_get_log()
```

---

# Linear

## Intructions :

1. Initialised `LinearSolver` instance with a given set of **_n-1_** unknowns:

```python
test = LinearSolver("1 + (2/3)*a + (b-c^2) = 3", b=1, c=2)
```

> ### _Rules for Variables_ :
>
> - Variables mustn't be named using any of the special constant/ operators listed in the table above
> - Variable names can consist of digits (but ideally avoid doing so)
> - Output variables will always be in lower case settings (keep it to lower case definition to avoid confusion)

2. Running the above line will automatically call the solver. Results will be output in dictionary format as such:

```python
print(test.results)
# {'b': 1, 'c': 2, 'a': 7.5}
print(test.answer) # 7.5 (automatically detects 'a' is the unknown variable)
```

3. Similar to calculator, printing out step-by-step calculation can be done via `linear_get_log()` method.

```python
# print out steps
test.linear_get_log()
```

> ### _Note_ :
>
> To get the string output instead, use:
>
> ```python
> print(test.log) # string output similar to what's shown for linear_get_log()
> ```
