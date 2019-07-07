
# Eric Huber 20190706
# https://github.com/echuber2/random_examples

# Another attempt at a sequencing function that could be used in a lambda.
# The "pipe" function gets or sets the pipe_ global variable. This only
# works if arguments to seq() are evaluated from left to right, which isn't
# guaranteed until Python 3.8. Version 3.8 may also introduce assignment
# expressions that could replace the global dictionary for other variables.
# Refer to: https://www.python.org/dev/peps/pep-0572/

# init
pipe_ = None
cond_ = None

# let('x', 3) sets the global x to 3
def let(var_name_string, val):
  globals()[var_name_string] = val

# let('x', 'y', 3) sets the global x[y] to 3
def letkey(var_name_string, key_name_string, val):
  globals()[var_name_string][key_name_string] = val

# Synonym for letkey, meant for list indices. Works the same way through duck-typing.
letind = letkey

# If car is an object with attribute color (car.color), then you can do this:
# letattr('car', 'color', 'blue')
def letattr(var_name_string, prop_name_string, val):
  setattr(globals()[var_name_string], prop_name_string, val)

# Get or set the pipe variable. Don't pass more than one argument.
def pipe(*args):
  global pipe_
  for arg in args:
    pipe_ = arg
  return pipe_

# Pass arguments that are expressions you'd like to evaluate in order.
# This should work, but not guaranteed until Python 3.8
def seq(*args):
  return pipe()

# Get or set the condition boolean. Don't pass more than one argument.
def cond(*args):
  global cond_
  for arg in args:
    cond_ = bool(arg)
  return cond_

# Evaluate either the true or the false branch, depending on cond_.
# Note that t and f MUST be lambda-lifted expressions or functions.
# This is necessary to avoid evaluating both branches.
def branch(true_lambda,false_lambda):
  global cond_
  return true_lambda() if cond_ else false_lambda()

# While loop: As long as cond_lambda evaluates true, body_lambda will be
# called again. Both arguments must be lambda-lifted.
def whi(cond_lambda, body_lambda):
  result = None
  while cond_lambda():
    result = body_lambda()
  return result

# EXAMPLES

# Note: One fun side effect of writing this way, is your whitespace on the
# left doesn't seem to matter much. Tabless Python?
seq(pipe(10), whi(
      lambda: pipe() > 0,
      lambda: seq(
        print('Running body because >0:', pipe()),
        pipe(pipe()-1)
        )
    ), print("Final:", pipe()))

seq(print('Math lesson:'), cond(2+2==4), branch(
      lambda: print('Yeah, 2+2==4'),
      lambda: print('No, 2+2==5') 
    ), print("Now you know!"))

# Here I define variables x, y, and z in the middle of the call. If you
# have a linter or IDE, it will complain, but this still works!
# (Also, all of this is in a lambda, which was originally the point.)
foo = lambda: seq(print('Setting x to 7'), let('x', 7), print('Setting y to 9'),
  let('y',9), print('Setting z to the sum'), let('z',x+y),
  print('Value of z:', z))

foo()

