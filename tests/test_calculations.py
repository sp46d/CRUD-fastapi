import pytest
from app.calculations import add, multiply, subtract


@pytest.mark.parametrize(["num1", 'num2', 'res'], [
    (1, 2, 3),
    (2, 3, 5)
])
def test_add(num1, num2, res):
    assert add(num1, num2) == res

def test_subtract():
    assert subtract(5, 3) == 2
