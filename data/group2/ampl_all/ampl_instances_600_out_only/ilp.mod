param set_len;	
set Y := 1..set_len;
param values{Y};
var x{Y} binary;
param target_sum;
	
maximize calculated_sum: sum{i in Y} x[i] * values[i];
	
	subject to constraint:
	    sum{i in Y} values[i]*x[i] = target_sum;
