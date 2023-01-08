def compute_pi(n_iter=1000):
    """ Compute Pi using Leibniz’s formula. """

    # Initialize denominator
    k = 1
    
    # Initialize sum
    s = 0
    
    for i in range(n_iter):
    
        # even index elements are positive
        if i % 2 == 0:
            s += 4/k
        else:
    
            # odd index elements are negative
            s -= 4/k
    
        # denominator is odd
        k += 2
    
    return s

def display_pi(n_iter=1000):

    print(compute_pi(n_iter=n_iter))
