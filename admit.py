#!/usr/bin/env python
import functools

class Dummy:
    user = 'Fred'

    # must return a function that does what we want to happen when plain 'func' is called
def admit(*users):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if Dummy.user in users:
                return func(*args, **kwargs)
            else:
                print(f"user {Dummy.user} is not allowed to call {func.__name__}")

        return wrapper

    return actual_decorator

@admit('Fred', 'Gill')
def goThere():
    print(f"Hi {Dummy.user}, you're in funky town!")

goThere()
Dummy.user = 'Larry'
goThere()
Dummy.user = 'Gill'
goThere()
