#!/usr/bin/python


def decorate(func):

    def wrapper():
        print("Before calling the function")
        func()
        print("After calling the function")

    return wrapper


@decorate
def test():
    print("Inside the function")


test()
