def add(a,b):
    """ Add a to b and return the result. """
    return a + b

def subtract(a, b):
    """ Subtract b from a and return the result. """
    return a - b

def multiply(a, b):
    """ Multiply a and b and return the result. """
    return a * b

def divide(a, b):
    """ Divide a by b and return the result. """
    return a / b

def compute_pi():
    """ Compute Pi using Leibniz’s formula. """

    # Initialize denominator
    k = 1
    
    # Initialize sum
    s = 0
    
    for i in range(1000):
    
        # even index elements are positive
        if i % 2 == 0:
            s += 4/k
        else:
    
            # odd index elements are negative
            s -= 4/k
    
        # denominator is odd
        k += 2
    
    return s
