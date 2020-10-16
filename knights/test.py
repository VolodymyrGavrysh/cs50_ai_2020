from logic import *

k = Symbol('Test_k')

m = Symbol('rt_t')

sen = And(k, Not(k))


print(sen.formula())