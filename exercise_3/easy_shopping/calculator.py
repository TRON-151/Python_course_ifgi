# this lib contains function for calculations

# addition function
def add(a,b):
    return a+b

# subtraction function
def sub(a,b):
    return a-b

# multiplication function
def multiply(a,b):
    return a*b

#division function
def divide(a,b):

    # if the division is Zero we through an error
    if b == 0:
        print("ERROR: Divisor should not be zero")
    # else do the division
    else:
        return a/b