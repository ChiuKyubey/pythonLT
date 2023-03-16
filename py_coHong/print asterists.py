values = []
for i in range(3):
    newVal = int (input("enter integer %d: " % (i+1)))
    values += [newVal]
print("%s %10s %10s"% ("element", "value", "asterisks"))
for i in range(len (values)):
    print("%7d %10d %s"% (i, values[i],"*" *values[i]))