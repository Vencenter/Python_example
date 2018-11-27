
#一处列表相同元素

a = [11, 22, 33, 33, 55, 66,33]

m=[]
for i in a:
    print i
    if i == 33:
        m.append(i)

for i in range(len(m)):
    a.remove(m[i])

print a


gen = (i for i in range(5))
print 3 in gen
        

foo1(1, 2)
foo2(1, 2)
print(foo1.__annotations__)
print(foo2.__annotations__)
