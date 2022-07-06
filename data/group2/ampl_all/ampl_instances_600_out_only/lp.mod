param set_len;
# Y= [1,2,3.. len]
set Y := 1..set_len;

# parameters that passed from .dat
param values{Y};
param target_sum;

# local variables
var x{Y} >= 0 <= 1;

# maximize [objective name]: sum{[index] in [index_set]}[Parameter]*[Variable]
maximize calculated_sum: sum{i in Y} values[i]*x[i];
subject to c1: sum{i in Y} values[i]*x[i] = target_sum;
