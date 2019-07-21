
# Eric Huber 20190720
# https://github.com/echuber2/random_examples

# Fake tail-call optimization / continuation-passing style with Python.
# Refactoring to return lambdas lets you pretend you're doing recursion.
# This is kind of similar to "continuation-passing style" transformations
# so I'll just tag the transformed versions with CPS for clarity (although
# real CPS is different from this too.)

# Motivation: Simply doing tail recursion in Python often exceeds the
# stack limit for recursion depth and crashes, like this version:

def sumlist_aux(l, acc):
  if l == []:
    return acc
  next_item = l.pop()
  return sumlist_aux(l, acc+next_item)

def sumlist(l):
  l_copy = list(l)
  return sumlist_aux(l_copy, 0)

# numbers 0...9999 inclusive:
long_list = list(range(10000))
expected_sum = sum(long_list)

# This would crash:
# print(sumlist(long_list))

# This version will run successfully by passing a lambda containing the
# next step to perform:

def sumlist_aux_cps(l, acc):
  if l == []:
    return (False, acc)
  next_item = l.pop()
  return (True, lambda: sumlist_aux_cps(l, acc+next_item))

def sumlist_cps(l):
  l_copy = list(l)
  return (True, lambda: sumlist_aux_cps(l_copy, 0))

def run_cps(f, x):
  (cps_running, next_thing) = f(x)
  while cps_running:
    (cps_running, next_thing) = next_thing()
  return next_thing

# Testing code...

import time

# naive looping sum
def loop_sum(l):
  acc = 0
  for x in l:
    acc = acc + x
  return acc

if run_cps(sumlist_cps, long_list) != expected_sum:
  raise(Exception("Fake CPS sum is incorrect"))

if loop_sum(long_list) != expected_sum:
  raise(Exception("loop_sum result is incorrect"))

print("Running ten times for benchmark: ")

times = []
for i in range(20):
  start_time = time.time()
  result = run_cps(sumlist_cps, long_list)
  stop_time = time.time()
  times.append(stop_time-start_time)
avg_cps_time = sum(times) / len(times)

times = []
for i in range(20):
  start_time = time.time()
  result = loop_sum(long_list)
  stop_time = time.time()
  times.append(stop_time-start_time)
avg_loop_sum_time = sum(times) / len(times)

times = []
for i in range(20):
  start_time = time.time()
  result = sum(long_list)
  stop_time = time.time()
  times.append(stop_time-start_time)
avg_builtin_time = sum(times) / len(times)

print("Avg time for fake CPS version: ", avg_cps_time)
print("Avg time for naive looping version: ", avg_loop_sum_time)
print("Avg time for built-in sum function: ", avg_builtin_time)

