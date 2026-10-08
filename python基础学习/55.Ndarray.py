#Ndarray数组所有元素数据类型相同，数据地址连续，批量操作数组元素更快，list中列表的数据类型可能不同，要通过寻址来找到下一个元素
#Ndarray数组支持广播机制，矩阵运算不需要写for循环
#底层通过c语言实现，运行速度更高
import numpy as np
arr = np.array([1,2,3,4,5])
arr +=1  #独特的广播机制，列表必须要用for循环
print(arr)
arr1 = np.array([1,2,3,4,5])
print(arr+arr1)  #实现2个数组之间的运算


#使用arange函数创建Ndarray数组
#创建一个0到9的数组
import numpy as np
arr1 = np.arange(10)
print(arr1)

#创建一个从5到14的数组，步长未2
arr2 = np.arange(5,15,2)
print(arr2)

#创建一个从0到1的数组，包含10个值（步长为0.1）
arr3 = np.arange(0,1,0.1)
print(arr3)

#zeros函数：创建指定长度或形状的全0数组
#函数原形：numpy.zeros(shape,dtype=float,order='C')
#shape：一个整数或整数元组，用来指定输出数组的形状
#dtype：可选参数，指定数组元素的数据类型，默认为float
#order：可选参数，指定数组数据在内存中的存储顺序，'C'表示按行（c语言风格），'F'代表按列（Fortran风格）
arr4 =np.zeros(4)
arr5 = np.zeros((4,2))
print(arr4)
print(arr5)
arr6 = np.zeros((3,2,2))  #创建3个两行两列的全零数组
print(arr6)
#ones方法和zeros方法几乎一样，用来创建全1数组

#empty：创建未初始化数组
x=np.empty((2,3))
print(x)

#full函数：创建指定形状，指定元素的数组
#函数原型：numpy.full(shape,fill_value,dtype=None,order='C')
#shape：整数或整数元组，输出数组形状
#fill_value：填充数组的值
#dtype：可选，指定数组元素的数据类型，若未指定从fill_value推断，若fill_value不能被转换为指定的dtype,就会引发错误
#order：可选，指定数组数据在内存中存储顺序
x1 = np.full((2,3),7)
print(x1)

#numpy数组的索引和切片访问与列表的一样
#对二维数组arr，切片语法：arr[row_slice,column_slice]
#row_slice选择行的范围,column_slice选择列的范围，若不切列，列可省略，不切行，要用:代替
arr7=np.array([[1,2,3],[4,5,6],[7,8,9]])
print("arr:\n",arr)
row1 = arr7[1]
print(row1)
rows = arr7[1:3]
print(rows)
#选择不连续的行
rows2 = arr7[[0,2]]
print(rows2)
#选择特定的列
col1 = arr7[:,1]
print(col1)
#选择不连续的列
col2 = arr7[:,[0,2]]
print(col2)


#Ndarray数组的属性
#通过shape可返回一个表示数组维度的元组，eg一个二行三列数组shape将返回
arr8 = np.array([[1,2,3],[4,5,6]])
print(arr8.shape)
print(arr8.dtype)
#通过size来统计数组中的元素个数
print(arr8.size)
#ndim：该属性为数组的维度大小，其大小等于调用shape方法返回的元组中元素的个数
print(arr8.ndim)


#数据类型的修改
#函数原型numpy.ndarray.astype(dtype,oder='K',casting='unsafe',subok=True,copy=True)
#dtype：表示新数据类型的对象，可以是NumPy的dtype对象，也可以是Python的数据类型
#casting：控制数据类型转换的安全性
#subok：若为True，则子类将被传递，否则返回的数组转换为基类数组
#copy：布尔值，指定是否复制数据
#默认情况下，该函数会返回一个新的Ndarray数组，并且该数组与原数组没有任何关系
#casting参数说明：
#'no'：表示根本不应该进行转换数据类型。
#'equiv'：允许数值上等价的类型转换，即转换前后数据的位表示相同。这意味着转换不会导致数据丢失。
#'safe'：允许安全的类型转换，即转换过程中不会丢失信息。不允许大容器向小容器转换
#'same_kind'：允许相同数据类型类别内的转换。例如，允许整型和整型之间、浮点型和浮点型之间的转换，但是不允许整型和浮点型之间的转换。允许大容器向小容器转换
#'unsafe'：允许任何类型的转换，不考虑是否会导致数据丢失或改变。这是最不安全的选项，因为它可能会静默地丢弃数据。
arr9 = np.array([1.1,2.2,3.3])
#使用astype方法将数组转换为整数类型
new_arr = arr9.astype(np.int32)
print("Original array:",arr9)
print("old type",arr9.dtype)
print("New array:",new_arr)
print("new type",new_arr.dtype)


#形状的修改
#reshape方法：用于给数组一个新的形状而不改变其数据，返回一个新的数组，但是如果给定的形状与原始数组的数据不兼容，会抛出异常。不改变原数组
#函数原型为：numpy.ndarray.reshape(newshape,order='C')
#newshape：整数或整数元组，新的形状应该与原始数组中的元素数量相匹配
arr10 = np.array([[1,2,3],[4,5,6]])
arr11 = arr10.reshape((3,2))
print(arr11)
#resize方法：用于改变数组的大小，与reshape类似，但它直接修改调用其的原始数组，若新形状大于原始形状，就在数组末尾添加新元素，这些元素的值未定义
#若新形状小于原始形状，则会截断数组，函数原型为numpy.ndarray.resize(newshape)
arr12 = np.array([[1,2,3],[4,5,6]])
print("Before:",arr12.shape)
arr12.resize((2,2))
print("after:",arr12)
arr12.resize((2,4))
print("after",arr12)
#flatten方法：返回一个一维数组，它是原始数据的拷贝，默认按行顺序展平数组，但可以通过参数order来指定展平顺序
#函数原型：numpy.ndarray.flatten(order='C')
print(arr12.flatten())
#ravel方法返回一个连续的数组，它尝试以最低的复制操作来返回展平后的数组
#函数原型numpy.ndarray.ravel(oreder='C')
print(arr12.ravel())
#ravel和flatten的区别：
#flatten方法返回原数组的副本，返回的新数组与原数组是两个独立的对象，对新数组的修改不会影响原数组
#ravel方法返回的是原数组的视图或副本，这取决于数组的顺序，若数组连续(C-style，行优先)，则ravel返回的是视图，这意味着返回数组的修改会影响到原数组，如果数组不是连续的，则ravel返回的是副本
a = np.array([[1,2,3],[4,5,6]])
b = a.flatten()
c = a.ravel()
d = a.ravel(order='F')
a[0][0] = 100
print("a",a)
print("b",b)
print("c",c)
print("d",d)

#数组的转置
arr_2d = np.array([[1,2],[3,4],[5,6]])
#获取转置
transposed_arr = arr_2d.T
print("Original array:")
print("arr_2d")
print("Transposed array:")
print(transposed_arr)

#随机Ndarray
#随机数种子是一个用于初始化随机数生成器的值，在cs中，大多数的随机数生成器实际上是伪随机数生成器，通过算法生成看似随机的数字
#随机数种子的特点
#1. 可重现性：通过设置相同的随机数种子，每次程序运行时生成的随机数序列都是相同的。这对于调试程序、进行科学计算或模拟时保持实验结果的一致性非常有用。
#2. 算法确定性：伪随机数生成器是确定性的，这意味着给定的种子会总是产生相同的随机数序列，这与真正的随机数生成器不同，后者总会生成不同的随机数。
#3. 种子来源：随机数种子的值可以是任意的。在许多编程环境中，如果不显式设置种子，通常会使用当前时间作为种子，这样每次程序运行时都会产生不同的随机数序列。
#4. 跨平台差异：不同的操作系统或硬件平台可能会产生不同的随机数序列，即使种子相同。这是因为不同的平台可能有不同的PRNG算法。

#random.random方法
#numpy.random.random(size=None)
#size为可选参数，用来指定输出数组的形状，其可以是一个整数或元组，整数则返回一个一维数组，若为元组则返回多维数组，形状与元组指定一致
array_1d = np.random.random(5)
print(array_1d)
array_2d = np.random.random((2,3))
print(array_2d)
#random.randn方法：用于从标准正态分布中抽取样本，意味着其返回的随机数具有平均值(mean)为0和标准差为1的正态分布
#函数原型为：numpy.random.randn(d0,d1,d2,...,dn)
#d0,d1,d2这些参数指定了输出数组的维度，若只提供一个数字，将返回一个一维数组，若提供多个数字，将返回一个多维数组，其中每个维度由对应参数指定
print(np.random.randn())
print(np.random.randn(5))
print(np.random.randn(2,3))
#random.normal方法：用来从具有平均值和标准差的正态分布中抽取样本
#函数原型：numpy.random.normal(loc=0.0,scale=1.0,size=None)
#loc：正态分布的均值，对应分布的中心位置，默认为0
#scale：正态分布的标准差，对应于分布的宽度，默认为1
#size：输出数组的形状，size为一个整数返回一个一维数组，size为一个元组，则返回一个多维数组。默认为None，返回一个单个随机数
#返回一个均值为0，标准差为1的正态分布中的单个随机数
print(np.random.normal())
#返回一个均值为0，标准差为1的正态分布中的5个随机数
print(np.random.normal(size=5))
#返回一个均值为5，标准差为2的正态分布中的5个随机数
print(np.random.normal(loc=10,scale=3,size=(2,3)))
#randint用于生成随机整数，这些整数在指定范围内分布均匀
#函数原型：numpy.random.randint(low,high=None,size=None,dtype=int)
#low：生成随机数的起点，若只提供low参数而未提供high参数，那么随机整数的范围将会是0到low（不包含low本身）
#high（可选）：生成随机数的结束点
#size（可选）：定义输出数组的形状
#dtype（可选）：指定返回数组的数据类型，默认为int
#从0到10（不包含）之间随机生成一个整数
print(np.random.randint(10))
#从1到10（不包含）之间随机生成一个整数
print(np.random.randint(1,10))
#从1到10（不包含）之间生成一个3*3的整数数组
print(np.random.randint(1,10,(3,3)))
#uniform方法：从均匀分布中抽取一个浮点数
#原型：numpy.random.uniform(low=0.0,high=1.0,size=None)
#在[0,1)范围抽取一个浮点数
print(np.random.uniform())
#在[5,10)范围抽取一个浮点数
print(np.random.uniform(5,10))
#在[0,1)范围抽取一个3*3的浮点数数组
print(np.random.uniform(size=(3,3)))
#在[5,10)范围抽取一个2*3的浮点数数组
print(np.random.uniform(5,10,size=(2,3)))
#shuffle函数：用来随机打乱数组元素顺序，只适用于一维数组，在原数组上进行操作，不创建一个新数组  
arr13 = np.array([1,2,3,4,5,6])
np.random.shuffle(arr13)
print(arr13)

