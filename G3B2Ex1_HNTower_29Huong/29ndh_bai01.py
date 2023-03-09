def SNTo(n):
    if n<2 : return 0
    else :
      if n==2 : return 1 
      else:
        for i in range(2,int (n**(1/2)+1)) :
            if n%i==0: 
                return 0
        return 1
n=2
i=1
while i<=100:
    if SNTo(n)==1:
        m=str(n)
        print(m)
        i=i+1
    n=n+1
    

           
