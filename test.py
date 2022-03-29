"""
Annie Cheng, zc375
March 23, 2022
"""

from model import Model

# Test case given in the assignment
print('--------------------Test 0--------------------')
lines = """2
H T
3
H T S
1,-1 -1,1 0,-100
-1,1 1,-1 0,-100
"""
print(lines)
test0 = Model(lines).main()

# Additional test cases given
for i in range(1,9):
    print('--------------------Test %s--------------------' % i)
    a = open('Ex%s.txt' % i, 'r')
    lines = a.read()
    print(lines)
    test1 = Model(lines).main()

# More test cases created by myself
print('--------------------Test X--------------------')
lines = """2
H T
3
H S T
1,-1 0,-100 -1,1
-1,1 0,-100 1,-1
"""
print(lines)
test0 = Model(lines).main()

print('--------------------Test X--------------------')
lines = """3
H T S
3
H T S
1,-1 -1,1 0,-100
-1,1 1,-1 0,-100
-100,-100 -100,-100 -100,-100
"""
print(lines)
test0 = Model(lines).main()

print('--------------------Test X--------------------')
lines = """3
R P S
3
R P S
0,0 -1,1 1,-1
1,-1 0,0 -1,1
-1,1 1,-1 0,0
"""
print(lines)
test0 = Model(lines).main()
