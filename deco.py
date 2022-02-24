#!/usr/bin/python3.10
"""
After all these years, perhaps it's not too late to get to grip with decorators!?
"""
funcs = []

def catalog(f):
    funcs.append(f)
    return f

@catalog
def square(n):
    return n*n

@catalog
def cube(n):
    return n*n*n

# note that cataloguing only happens once per decorated function.
#
print(square(3), cube(3), square(3), cube(3))
print(funcs)

# -------------------------
class Smuggler:
    """
    Smuggler is defined for situations when you want to 'sneak' more arguments into
    a callback invocation than the relevant API allows.
    """
    def __init__(self, func, *extra_args, **extra_kwargs):
        self.func = func
        self.extra_args = extra_args
        self.extra_kwargs = extra_kwargs

    def __call__(self, *args, **kwargs):
        self.func(*args , *self.extra_args, **kwargs | self.extra_kwargs)

def api_func(api_arg, callback_func):
    print(f"no real API func do do on {api_arg}")
    print(f"just call callback func {callback_func} with API's own arg")
    callback_func("api's callback arg")

def my_callback(his_arg, my_arg1, my_arg2):
    """
    In this test case, we smuggle just one extra argument into the callback.
    """
    print(f"my_callback({his_arg}, {my_arg1}, {my_arg2})")


api_func('api_arg', Smuggler(my_callback, 42, 13))
api_func('api_arg', Smuggler(my_callback, 54, 10))
