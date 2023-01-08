from mydescpackage.arithmetic import add, subtract, divide, multiply, product

def test_add():
    a = 4
    b = 8

    ans = 12

    assert add(a, b) == ans

def test_divide():
    a = 4
    b = 8

    ans = 0.5

    assert divide(a, b) == ans

def test_subtract():
    a = 4
    b = 8

    ans = -4

    assert subtract(a, b) == ans

def test_multiply():
    a = 4
    b = 8

    ans = 32

    assert multiply(a, b) == ans

def test_product():
    a = 4
    b = 8
    c = 10

    ans = 320

    assert product([a, b, c]) == ans
