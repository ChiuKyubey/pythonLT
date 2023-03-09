def NDH(n, toaMot, toaHai, toaBa):
    if n == 1:
        print("chuyen tu", toaMot, "sang", toaBa)
    else:
        NDH(n-1, toaMot, toaBa, toaHai)
        print("chuyen tu", toaMot, "sang", toaBa)
        NDH(n-1, toaHai, toaMot, toaBa)
NDH(4,"1","2","3")