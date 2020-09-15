#!/usr/bin/env python3
a, b = 0, 1
while b < 100000:
    print(b)
    a, b = b, a + b
