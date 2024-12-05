from collections import Counter

a, b = [], []
with open('input.txt', 'r') as f:
    for line in f.readlines():
        x, y = (int(z) for z in line.split())
        a.append(x)
        b.append(y)

a.sort()
b.sort()
n = len(a)

# part 1
print(sum(abs(a[i]-b[i]) for i in range(n)))

# part 2
c = Counter(b)
print(sum(a[i]*c[a[i]] for i in range(n)))