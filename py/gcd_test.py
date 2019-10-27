import pytest

from gcd import gcd

def test_gcd():
    assert gcd(1, 1) == 1
    assert gcd(2, 3) == 1
    assert gcd(2, 4) == 2
    assert gcd(12, 16) == 4
    with pytest.raises(ValueError):
        gcd(0, 0)
    with pytest.raises(ValueError):
        gcd(0, 1)
    with pytest.raises(ValueError):
        gcd(1, 0)
    with pytest.raises(ValueError):
        gcd(-1, 1)
    with pytest.raises(ValueError):
        gcd(1, -1)
    
