
# Sequence-Style Python
# Eric Huber
# https://github.com/echuber2/random_examples

# v0.0: 20190706
# v0.1: 20190707

# Another attempt at a sequencing function that could be used in a lambda.
# The "pipe" function gets or sets the _pipe_ global variable. This only
# works if arguments to seq() are evaluated from left to right, which isn't
# guaranteed until Python 3.8. Version 3.8 may also introduce assignment
# expressions that could replace the global dictionary for other variables.
# Refer to: https://www.python.org/dev/peps/pep-0572/

# init
_pipe_ = None
_cond_ = None

# let('x', 3) sets the global x to 3
def let(var_name_string, val):
  globals()[var_name_string] = val

# letkey('x', 'foo', 3) sets the global x['foo'] to 3
def letkey(var_name_string, key, val):
  globals()[var_name_string][key] = val

# letind('mylist', 1, 7) sets mylist[1] to 7.
# The second parameter should be a list index integer. This is actually
# defined as a synonym for letkey, and it still works as intended because
# of duck typing.
letind = letkey

# If car is an object with attribute color (car.color), then you can do this:
# letattr('car', 'color', 'blue')
def letattr(var_name_string, prop_name_string, val):
  setattr(globals()[var_name_string], prop_name_string, val)

# Get or set the pipe variable. (Don't pass more than one argument.)
# Examples;
#  pipe(1) sets the pipe variable to 1.
#  pipe() gets the pipe variable.
def pipe(*args):
  global _pipe_
  for arg in args:
    _pipe_ = arg
  return _pipe_

# Pass arguments that are expressions you'd like to evaluate in order.
# This should work, but not guaranteed until Python 3.8
def seq(*args):
  return _pipe_

# Get or set the condition boolean. Don't pass more than one argument.
def cond(*args):
  global _cond_
  for arg in args:
    _cond_ = bool(arg)
  return _cond_

# Evaluate either the true or the false branch, depending on _cond_.
# Note that t and f MUST be lambda-lifted expressions or functions.
# This is necessary to avoid evaluating both branches.
def branch(true_lambda, false_lambda):
  return true_lambda() if _cond_ else false_lambda()

# While loop: As long as cond_lambda evaluates true, body_lambda will be
# called again. Both arguments must be lambda-lifted.
def whi(cond_lambda, body_lambda):
  result = None
  while cond_lambda():
    result = body_lambda()
  return result

# EXAMPLES

# Below, I define some variables in the middle of a seq call.
# If you have a linter or IDE, and they show you an error message
# about undefined variables, you can pre-declare any variables
# just to make the messages go away. However, it should work in
# execution regardless.
x = None # optional
y = None # optional
z = None # optional
i = None # optional

# Note: One fun side effect of writing this way is that the whitespace on
# the left doesn't matter as long as you're still listing arguments to seq().
# This allows a more flexible indentation style than usual.
seq(
  pipe(5),
  print('Example with a while loop: Counting down from', pipe(), '...'),
  whi(
      lambda: pipe() > 0,
      lambda: seq(
        print('[In body] Still >0:', pipe(), 'Decrementing...'),
        pipe(pipe()-1)
      )
    ), print("Final:", pipe(), '\n'))

seq(print('Example with a conditional branch:\nMath lesson:'), cond(2+2==4), branch(
      lambda: print('Yeah, 2+2==4'),
      lambda: print('No, 2+2==5')
    ), print("Now you know!", '\n'))

# All of this can be put in a lambda, which was originally the point of
# trying to do it. This way you can put pretty arbitrary things in lambdas,
# even with branching and assignments.
foo = lambda: seq(print('Example with sequenced assignments:'),
  print('Setting x to 7'), let('x', 7), print('Setting y to 9'),
  let('y',9), print('Setting z to the sum'), let('z',x+y),
  print('Value of z:', z, '\n'))
# seq always returns _pipe_, so if we didn't use pipe or don't care,
# just assign it to underscore to throw it away. Here, we only care
# about the side-effects (assigning a variable, printing a message).
_ = foo()

# Some unit tests that also show example usage:

let_test = lambda: seq(
  let('x','Success!'),
  print('Testing let:', x, '\n')
)
_ = let_test()

letkey_test = lambda: seq(
  let('x', {}),
  letkey('x','y','Success!'),
  print('Testing letkey:', x['y'], '\n')
)
_ = letkey_test()

letind_test = lambda: seq(
  let('x', [0,0,0]),
  # Instead of making an iteration variable 'i' here and adding junk
  # to the global namespace, you could also just use the pipe variable.
  let('i', 0),
  whi(lambda: i < len(x), lambda: seq(
      letind('x', i, 7),
      let('i', i+1)
    )
  ),
  pipe('Testing letind:'),
  cond(x == [7,7,7]),
  branch(
    lambda: print(pipe(), 'Success!\n'),
    lambda: print(pipe(), 'Failure!\n')
  )
)
_ = letind_test()

# You can define a class in the seq format using the built-in Python
# functions, but it's a pain.
class Car:
  def __init__(self):
    self.color = 'blue'

letattr_test = lambda: seq(
  let('x', Car()),
  letattr('x', 'color', 'green'),
  pipe('Testing letattr:'),
  cond(x.color == 'green'),
  branch(
    lambda: print(pipe(), 'Success!\n'),
    lambda: print(pipe(), 'Failure!\n')
  )
)
_ = letattr_test()
