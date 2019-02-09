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

# Task 4: Brute Force Comparison
For small, simple formulas the brute force method will often have a shorter run
time. This is especially true when there are few variables as the brute force does
not need to create as many test cases. For example:

```
python brute_force.py 
(A1 v ~A1) & (~A2 v A2)
Brute Force returned: VALID in 0.000651121139526s
CNF method returned: VALID in 0.00645089149475s
```

```
python brute_force.py 
(A1 & A2) -> A3
Brute Force returned: NOT VALID in 0.000617027282715s
CNF method returned: NOT VALID in 0.00601100921631s
```

However, as the number of variables gets large and the complexity of the
formulas increases the CNF conversion method starts to outperform the brute
force method. This happens because as the number of variables increases the
number of possible test cases that the brute force method must check increases
exponentially (for n variables there are 2^n possible truth assignments) but
the CNF conversion method uses minisat which is able to narrow down the
possibilities by ruling out parts of the search space. When the number of
variables is large the only way that the brute force method can beat the CNF
conversion method is if the formula is invalid and the brute force method
happens to guess a truth assignment proving that the formula is invalid early
on. For example:

```
python brute_force.py
(A1 & (~A10 -> (A11 -> A13)) -> (~A2 -> (A3 -> ((A4 & A5) v (A1 -> ~A2) v (A6 -> (~A7 & (A8 v ~A9)) v (A13 & A10))))))
Brute Force returned: VALID in 0.20072722435s
CNF method returned VALID in 0.0077748298645s
```

```
python brute_force.py
A1 -> (A2 -> (~A3 -> ((~A4 v ~A1) -> ((A5 & A6 & A7) -> A8) v ((A1 v ~A2) & (A9 -> ~A10)))))
Brute Force returned: NOT VALID in 0.0131900310516s
CNF method returned: NOT VALID in 0.0091769695282s
```
