

def gcd(iterable):
    def _gcd(x, y):
        """Euclidian algorithm"""
        while y:
            x, y = y, x % y
        return x

    gcd_value = _gcd(iterable.pop(), iterable.pop())
    for item in iterable:
        gcd_value = _gcd(gcd_value, item)
    return gcd_value
