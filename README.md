# Valid-Entailments-With-SAT
Course project in programming and logic. Translation of Boolean formulas to CNF, validity and entailment checking.
Task 4.
Brute v Minisat
Running the bruteforce generally has a shorter run time for small, simple formulas. 
This is especially true when there are few variables as brute force does not need to create as many test cases.
However, when there starts to be many variabes the run times are similar.
The more variables, the more possible test cases. 2^n cases since there are two possibilities for each variable, (true & false).
With larger more complex formulas, Minisat would be able to narrow down possibilites by ruling out parts of the search sapce. 
Where as bruteforce must go through every test case to proove it right and relies on matching a case that prooves it wrong happening
sooner to shorten the time it takes.

