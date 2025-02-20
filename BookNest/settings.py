def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def primepartition(m):
    if m <= 0:
        return False
    for p in range(2, m):
        if is_prime(p) and is_prime(m - p):
            return True
    return False

def matched(s):
    count = 0
    for char in s:
        if char == "(":
            count += 1
        elif char == ")":
            count -= 1
        if count < 0:
            return False
    return count == 0

def rotatelist(l, k):
    if k <= 0:
        return l
    k = k % len(l)  # Reduce unnecessary full rotations
    return l[k:] + l[:k]