
# Examples of simple lambda-lifted conditional and sequencing combinators
# in Python. (This is mainly to show how you can do things in Python lambdas
# that the syntax otherwise doesn't seem to allow.)

# https://github.com/echuber2/random_examples
# Eric Huber 20190705

# ----------------------------------------------------------

# Lambda-lifted if function:
# cond must evaluate to a bool
# true_lambda and false_lambda must be lambdas that take no arguments
def iff(cond, true_lambda, false_lambda):
    if cond:
        return true_lambda()
    else:
        return false_lambda()

# Primitive sequencing function:
# s1 is evaluated before s2 assuming Python evaluates parameters
# from left to right. These should not be lambdas. (If they are,
# invoke them in-place when passing.) The result of the second
# statement is returned.
def seq_simple(s1, s2_result):
    return s2_result

# More elaborate sequencing function:
# You can provide any number of expressions as parameters from left to right
# and they'll get evaluated in sequence. The return value of the last one
# is returned overall.
# (The expressions should not be lambda-lifted.)
def seq(*args):
    x = None
    for arg in args:
        x = arg
    return x

# Some functions for testing:

# print message and return a value
# (written in regular style)
# def gift10(msg):
#     print(msg)
#     return 10

# Same thing using seq:
gift10 = lambda msg: seq(print(msg),10)

gift20 = lambda msg: seq(print(msg),20)

# Examples with output:

print("\nseq example 1:")
seq(print("A"),print("B"),print("C"))
# Output:
# A
# B
# C

print("\nseq example 2:")
seq_result = seq(gift10("Hi. Throwing away 10."), gift20("Bye. Returning 20."))
print("seq_result has value: " + str(seq_result))
# Output:
# Hi. Throwing away 10.
# Bye. Returning 20.
# seq_result has value: 20

print("\niff example:")
# lambda lifting prevents both branches from being evaluated
iff(5>2, lambda: print("True branch! This will be shown!"), lambda: print("False branch! This never gets evaluated!"))
# Output:
# True branch! This will be shown!

# a more complex example:
ten_or_twenty = lambda b: iff(b, \
    lambda: seq(print("True branch!"),gift10("Returning 10.")), \
    lambda: seq(print("False branch!"),gift20("Returning 20.")))

print("\ncomplex example: (passing True)")
get_10 = ten_or_twenty(True)
print("get_10 has value: " + str(get_10))
# Output:
# True branch!
# Returning 10.
# get_10 has value: 10

print("\ncomplex example: (passing False)")
get_20 = ten_or_twenty(False)
print("get_20 has value: " + str(get_20))
# False branch!
# Returning 20.
# get_20 has value: 20

