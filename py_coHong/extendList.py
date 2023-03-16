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

#2)     remove specified item
#remove la xoa
# In[3]:
thislist =["apple","banana","cherry"]
thislist.remove("banana")
print('xoa banana')
print(thislist)

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

#4)     remove dùng del
thislist =["apple","banana","cherry"]
del thislist[0]
print('xoa bang phan tu 0 del ')
print(thislist) 
#xóa list
print('xóa list')
del thislist

#5)     xoa tất cả phần tử dùng clear
thislist =["apple","banana","cherry"]
thislist.clear()
print('xóa tất cả phần tử')
print(thislist)
