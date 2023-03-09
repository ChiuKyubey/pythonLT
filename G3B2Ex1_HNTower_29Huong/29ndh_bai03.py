#giai phuong trinh bac 1 bac 2
a= float(input("nhap a: "))
b= float(input("nhap b: "))
c= float(input("nhap c: "))
def bac1 (a,b,c):
    if b==0 :
        if c==0: print("vo so nghiem") 
        else : print("vo nghiem")
    else :
        x=-c/b
        print(x)
def bac2 (a,b,c):
    denta=b**2-4*a*c
    if denta==0:
        x1=-b/(2*a)
        print("nghiem kep: " ,x1)
    elif denta>0 : 
        x1= (-(denta**(1/2))-b)/(2*a) 
        x2= (-(denta**(1/2))+b)/(2*a)
        print("x1= ",x1)
        print("x2= ",x2)
    else : print ("vo nghiem")
if a==0: bac1(a,b,c)
else : bac2(a,b,c)
