#!/usr/bin/env python
# coding: utf-8

#1)     extend list
# In[1]:
#extend la noi chuoi
thislist = ["apple","banana","cherry"]
tropical = ["mango","pineapple","papaya"]
thislist.extend(tropical)
print('noi chuoi: ')
print(thislist)
# In[2]:
thislist = ["apple","banana","cherry"]
thistuple = ["kiwi","orange"]
thislist.extend(thistuple)
print('noi chuoi: ')
print(thislist)
print()

#2)     remove specified item
#remove la xoa
# In[3]:
thislist =["apple","banana","cherry"]
thislist.remove("banana")
print('xoa banana')
print(thislist)
print()

#3)     remove theo chỉ số 
thislist =["apple","banana","cherry"]
thislist.pop(0)
print('xoa phantu 0 bang pop')
print(thislist)
#nếu không có chỉ số(đối số) thì xóa phần tử cuối cùng của danh sách
# thislist =["apple","banana","cherry"]
thislist =["apple","banana","cherry"]
thislist.pop()
print(thislist) 
print()

#4)     remove dùng del
thislist =["apple","banana","cherry"]
del thislist[0]
print('xoa bang phan tu 0 del ')
print(thislist) 
#xóa list
print('xóa list')
del thislist
print()

#5)     xoa tất cả phần tử dùng clear
thislist =["apple","banana","cherry"]
thislist.clear()
print('xóa tất cả phần tử')
print(thislist)
print()

#6)     loop list
thislist =["apple","banana","cherry"]
print('in list từng phần tử')
for i in range(len(thislist)):
    print(thislist[i])

#dung while 
thislist =["apple","banana","cherry"]
i=0
print('in list bằng while')
while i<len (thislist):
    print(thislist[i])
    i=i+1
print()

#vd:
print('xuất các loại trái cây có chữ a')
fruits = ["apple","banana","cherry"]
newlist =[]
for x in fruits:
    if "a" in x:
        newlist.append(x)
print(newlist)
#cung mục đích như trên 
fruits = ["apple","banana","cherry"]
newlist= [x for x in fruits if "a" in x]
print(newlist)
print()

#7)     các cách ghi khác nhau cùng một chức năng 
newlist=[x for x in fruits]
newlist=[x for x in range(10)]
newlist=[x for x in range(10) if x <5]
newlist=[x.upper() for x in fruits]
newlist=['hello' for x in fruits]
newlist=[x if x!= "banana" else "orange" for x in fruits]
print(newlist)
print()

#8)     sortlist
#dung sắp xếp chữ cái a->z
fruits = ["apple","banana","cherry"]
thislist.sort()
print(thislist)
#sắp xếp từ z->a
fruits = ["apple","banana","cherry"]
thislist.sort(reverse=True)
print(thislist)
print()

#9)     copy list
print('copy: ')
fruits = ["apple","banana","cherry"]
mylist = fruits.copy()
print(mylist)
print()

#10) join two lists
list1 =["a","b", "c"]
list2 =[1,2,3]
list3=list1+list2
print('nối 2 chuỗi')
print(list3)
print('thêm phần tử 2 vào chuỗi 1')
for x in list2:
    list1.append(x) #them vao duoi
print(list1)
print()