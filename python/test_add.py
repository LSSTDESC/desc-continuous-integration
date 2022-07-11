from my_arithmetic import add

def test_add():
    a = 4
    b = 8

    ans = 12

    assert add(a, b) == ans
