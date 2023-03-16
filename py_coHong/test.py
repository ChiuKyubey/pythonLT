values = []
for i in range(5):
    newVal = str (input("story %d: " % (i+1)))
    values += [newVal]
print("Subscript Value")
for i in range(len (values)):
    print("%9d %1s"% (i+1, *values[i]))