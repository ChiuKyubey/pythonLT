b = {1:"mot", 2:"hai", 3:"ba", 4:"bon", 5:"nam", 6:"sau", 7:"bay", 8:"tam", 9:"chin", 0:"khong"}
def InRaSo(str):
    c = ""
    for i in str:

        c += b[int(i)] + " "
    return c
print(InRaSo("138"))