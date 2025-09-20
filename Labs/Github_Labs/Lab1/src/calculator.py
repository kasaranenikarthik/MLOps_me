'''
This module is a simple calculator with four functions.
Each function takes two arguments and performs a basic arithmetic operation.
'''

def check_type(x, y):
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError("Both arguments must be int or float")
 
def fun1(x, y):
    '''Returns the sum of x and y'''
    check_type(x, y)
    return x + y

def fun2(x, y):
    '''Returns the difference of x and y'''
    check_type(x, y)
    return x - y

def fun3(x, y):
    '''Returns the product of x and y'''
    check_type(x, y)
    return x * y

def fun4(x, y):
    '''Returns the quotient of x and y'''
    check_type(x, y)
    return fun1(x, y) + fun2(x, y) + fun3(x, y)
