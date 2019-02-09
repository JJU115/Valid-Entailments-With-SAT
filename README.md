# Valid-Entailments-With-SAT
Course project in programming and logic. Translation of Boolean formulas to CNF, validity and entailment checking.

Upon executing ./vcheck3 at the terminal you will be prompted to enter a comma separated list of boolean formulas. The last formula entered will be treated asthe conclusion and everything prior as premises. The program will determine whether the premises entail the conclusion and if it doesn't will report an assignment where all premises are true and the conclusion is false.

For example, after executing vcheck3 you will see:

Enter comma separated boolean expression(s) >>>A1 v A2, A3 -> A4, A2 & A1, (A3 & A2) -> A1


Here, A1 v A2, A3 -> A4, A2 & A1 are premises and (A3 & A2) -> A1 is the conclusion.
