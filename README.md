# Valid-Entailments-With-SAT
Course project in programming and logic. Translation of Boolean formulas to CNF, validity and entailment checking.

# To Run vcheck1, vcheck2, vcheck3
You may need to ensure that they are all executable: `chmod +x vcheck1 vcheck2
vcheck3`.

Then run the commands as `./vcheck1 A1 v A2` for example.

Some boolean formula tokens will be interpreted as bash commands unless
surrounded by double quotes.

For example `./vcheck1 (~A1 v ~A2) & ~A3` should be written as `./vcheck1 "(~A1
v ~A2) & ~A3"` to ensure that this doesn't happen.
