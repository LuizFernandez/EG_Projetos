***



```
operation: op_arit
		 | op_logical

op_arit: termo_arit
	   | op_arit OPA termo_arit

termo_arit: factor_arit
		  | termo_arit OPM factor_arit

factor_arit : value
			| factor_arit POW factor_arit
		    | LPAR op_arit RPAR

OPA : ADD | SUB
OPM : MUL | DIV | MOD
OPP : POW

op_logical: expr_logical
		  | op_arit OPR op_arit

OPR : EQ
    | NE
    | LT
    | LE
    | GT
    | GE

op_logical: termo_log
	      | op_logical OR termo_log

termo_log: fator_log
		 | termo_log AND fator_log

fator_log: op_logical
		 | BOOL
		 | value "in" ID
		 | LPAR op_logical RPAR

```

