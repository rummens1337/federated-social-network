
# This would be the function imported from another file
def f():
    return 3

# This would be the test.
def test_function_false():
    assert f() == 4

# This would be the test.
def test_function_true():
    assert f() == 3