import numpy as np
#数组和标量的运算（应用广播机制）
arr = np.array([[1,2,3],[4,5,6]])
b = 2 -arr
print("original:\n",arr)
print("new:\n",b)

#数组和数组的运算
arr1 = np.array([[11,12,13],[14,15,16]])
arr2 = np.array([[1,2,3],[4,5,6]])
#数组的相加，使对应位置的元素相加
arr3 =  arr1 + arr2
print(arr3)
#使用函数运算
#在Numpy中，用numpy.add函数来完成两个数组之间的加法运算，如果两个数组的形状相同，那么就会对应位置相加
#函数原型numpy.add(x1,x2,/,out=None,*,where=True,casting="same_kind",order="K",dtype=None,subok=True)
arr4 = np.add(arr1,arr2)
print(arr4)

condition = np.array([[True,True,True],[False,False,False]],dtype=np.bool_)
arr5 = np.add(arr1,arr2,where=condition)
print("运算结果:\n",arr5)
#用numpy.substract来进行减法运算
#用numpy.multiply来进行乘法运算
#用numpy.divide来进行除法运算


#Ndarray数组的广播机制：提供了一种规则，让不同形状的两个计算数组广播到相同形状，然后再去进行元素级的算数运算，使得形状不完全匹配的数组也能互相运算
#通过这个机制，numpy能在保持效率的同时，扩展数组的操作范围，从而无需显示地扩展数组维度或进行循环遍历以实现元素级的计算，极大增强了数组处理能力
#具体规则
#1.若2个数组维度不同，则形状较小的数组在前面补1维
#2.若2个数组的形状在某个维度上不匹配，且其中一个维度长度为1，则会沿该维度复制扩展来匹配另一个数组的形状
#3.如果在任一维度上不匹配且没有维度等于1，就引发异常
#eg.(1,2,3)和(3,4)是无法通过广播机制来广播到相同形状

#squeeze方法：从数组形状中删除所有单维度的条目，即把形状中为1的维度去掉，函数原型为
#numpy.squeeze(a,axis=None)
#a：输入数组，它可以是任何形状的数组，但至少有一个维度大小为1
#axis：可选参数，一个整数或者整数元组，若指定该参数，则只压缩指定的轴，若该轴在数组a中不是单维度的，则不会进行压缩。若未指定，则所有单维度轴都给压缩

arr6=np.array([[[1],[2],[3]]])
print(arr6)
print("原始数组形状：",arr6.shape)
squeezed_arr = np.squeeze(arr6,axis=2)
print(squeezed_arr)
print("压缩后的数组形状",squeezed_arr.shape)
#expand_dims方法：增加维度
arr7 = np.array([1,2,3])
expanded_arr = np.expand_dims(arr7,axis=0)
print("增加维度后的数组形状：",expanded_arr.shape)

#连接数组
#concatenate：将多个数组沿指定的轴连接起来，形成一个更大的数组
#函数原型：numpy.concatenate((a1,a2,...,arr_n),axis-0,out=None)
#(a1,a2,...,arr_n)：是一个包含数组的元组，这些数组需要被连接，所有数组在除了连接轴之外的其他维度上必须有相同的形状
#axis：整数，指定沿着哪个轴进行连接，若不指定，默认为0，表示第一个轴
#out：可选参数，提供则将直接存储在这个数组中，该数组必须具有与输入数组相同的形状和数据类型。
#工作原理：
#1.输入验证：concatenate接收一个元组或列表作为输入，其中包含一系列数组，这些数组可以是任意维度，但他们在除了连接的轴之外的所有维度必须有相同形状
#2.轴参数：concatenate有一个必需参数axis，它指定了沿哪个轴进行连接，轴编号从0开始，对1维数组，只有一个轴（轴0），二维数组，轴0是行，轴1是列
#3.形状兼容性检查：所有输入数组在axis参数指定的轴上维度大小可以不同，但在其他轴维度大小要相同。
#4.内存分配：在连接之前，concatenate会计算输出数组大小，分配足够内存空间来存储结果
#5.数据复制：concatenate会将输入数组数据复制到新分配内存空间中，具体来说，它将沿着指定的轴顺序复制每个数组数据，从而形成新的数组
#6.结果数组：输出结果是一个新数组，在axis指定的轴上维度大小是输入数组在该轴上维度大小的总和，而其他轴上则与输入数组相同
a = np.array([[1,2],[3,4]])
b = np.array([[5,6]])
print(f"数组a的形状未{a.shape},数组a为\n",a)
print(f"数组b的形状未{a.shape},数组b为\n",a)
c = np.concatenate((a,b),axis=0)
d = np.concatenate((a,b.T),axis=1)
print(c)
print(d)


#stack函数：用于沿着新的轴连接一系列数组，与numpy.concatenate不同，该函数总是创建一个新的轴，而concatenate是在现有轴上进行数组连接
#函数原型：numpy.stack(arrays,axis=0,out=None)
#arrays ：一系列数组，它们将被堆叠在一起，所有数组要有相同形状
#axis：整数，表示新轴的位置，默认为0
#out：可选参数，若提供，则直接存储到该数组中，该数组必须具有与输出数组相同形状和数据类型
#工作原理
#1.输入验证：stack接收一个数组序列（如列表或元组）作为输入，所有输入数组必须要有相同的形状
#2.轴参数：stack有一个必须的参数axis，指定了新轴的位置
#3.形状兼容性检查：所有输入数组在除了要创建的新轴外的所有维度上必须具有相同形状
#4.内存分配：stack会计算输出数组的形状，并在内存中为这个新数组分配空间，新数组形状将比输入数组的形状多一个维度，新增的维度大小等于输入数组的数量
#5.数据复制：stack将输入数组的数据复制到新分配内存空间中，每个输入数组在新轴上占据一个位置
#6.结果数组：输出结果是一个新数组，形状在axis参数指定的位置上增加了一个维度
a1 = np.array([1,2,3])
b1 = np.array([4,5,6])
c1 = np.array([7,8,9])
e = np.stack((a1,b1,c1),axis=0)
print(f"数组e的形状为{e.shape},数组e为\n",e)



#分割方法
#split：该函数用于沿着指定的轴将数组分割成多个子数组，可指定要分割的数组、分割的位置或子数组的数量。
#函数原型：numpy.split(arr,indices_or_sections,axis=0)
#arr：要分割的数组
#indices_or_sections：一个整数，表示要将数组平均分割成多少个子数组，也可以是一个整数数组，表示分割位置
#axis：沿着哪个轴分割，默认为0。
#工作原理
#1.输入验证：split接受一个数组arr作为输入，以及
0
