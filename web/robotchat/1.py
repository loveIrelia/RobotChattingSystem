count = 0
s='匿名'
d ={}
for i in range(0,5):
    temo = '匿名{name}'.format(name=count)
    d[temo]=1
    count+=1
    print(temo)
print(d)
