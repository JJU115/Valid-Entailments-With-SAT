# Valid-Entailments-With-SAT
Course project in programming and logic. Translation of Boolean formulas to CNF, validity and entailment checking.

# To Run vcheck1, vcheck2, vcheck3
Ensure that they are all executable: `chmod +x vcheck1 vcheck2 vcheck3`. Then
run using `./vcheck1`.

vcheck1, vcheck2, and vcheck3 read boolean formulas from stdin, not as command
line arguments.

For example use:
```
./vcheck1
A1 v ~A1
```
Rather than:
```
./vcheck1 A1 v ~A1
```
