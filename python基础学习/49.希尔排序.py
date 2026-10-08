#希尔排序是插入排序的一种，也叫缩小增量排序，是更高效的改进版本，是非稳定排序算法
arr = [8,9,1,7,2,3,5,4,6,0] 
"""
[8,3]
[9,5]
[1,4]
[7,6]
[2,0]
"""
def shell_sort(arr):
    n = len(arr)
    gap = n//2
    while gap > 0:
        for i in range(gap,n):  #分成range(gap,n)组
            key = arr[i]
            j=i  #j相当于游标
            while j>= gap and arr[j - gap] > key: #索引j要在gap之后，保证j-gap不会出现负数的情况
                arr[j] = arr[j-gap] #将j-gap的元素移到j位置
                j -= gap #遍历完该组的所有元素
            arr[j] = key #最后将key插入放置到合适的位置
        gap //= 2
    return arr
arr1 = [9,4,5,2,1,6,7,8,3]
result = shell_sort(arr1)
print(result)