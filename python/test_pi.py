from my_arithmetic import compute_pi
import math

def test_add():
    ans = 3.14

    assert math.isclose(compute_pi(), ans, rel_tol=0.01)
