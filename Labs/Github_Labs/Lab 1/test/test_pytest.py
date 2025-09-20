import pytest
from src.calculator import fun1, fun2, fun3, fun4, check_type

def test_fun1():
    assert fun1(2, 3) == 5
    assert fun1(-1, 1) == 0
    assert fun1(0, 0) == 0
    assert fun1(2.5, 3.5) == 6.0
    assert fun1(-2.5, 4) == 1.5

def test_fun2():
    assert fun2(2, 3) == -1
    assert fun2(-1, 1) == -2
    assert fun2(0, 0) == 0
    assert fun2(2.5, 3.5) == -1.0
    assert fun2(-2.5, 4) == -6.5

def test_fun3():
    assert fun3(2, 3) == 6
    assert fun3(-1, 1) == -1
    assert fun3(0, 0) == 0
    assert fun3(2.5, 3.5) == 8.75
    assert fun3(-2.5, 4) == -10.0

def test_fun4():
    assert fun4(2, 3) == 10
    assert fun4(-1, 1) == -3
    assert fun4(0, 0) == 0
    assert fun4(2.5, 3.5) == 13.75
    assert fun4(-2.5, 4) == -15.0

def test_check_type():
    with pytest.raises(TypeError):
        check_type("a", 1)
    with pytest.raises(TypeError):
        check_type(1, "b")
    with pytest.raises(TypeError):
        check_type("a", "b")
    # Valid types should not raise an error
    try:
        check_type(1, 2)
        check_type(1.5, 2.5)
        check_type(-1, -2)
    except TypeError:
        pytest.fail("check_type raised TypeError unexpectedly!")