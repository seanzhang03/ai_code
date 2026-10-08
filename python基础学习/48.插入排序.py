arr = [64,34,43,12,22,11,55]
def insertion_sort(arr):  #初始时认定第一个元素为已排序的有序序列
    for i in range(1,len(arr)): #i表示待被插入到有序序列的元素的索引
        key = arr[i]  #待被插入的元素,用key保留该元素的值
        j = i-1  #i-1为有序序列的最后一个元素的索引
        while j>= 0 and key < arr[j]: #每次和arr[j]比较，若key更小，则将arr[j]向后面的位置移动（会造成2个相等元素，但这是正常现象）
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key  #不满足就赋给j+1的位置，即两个相等元素索引更大的那个位置
    return arr
result = insertion_sort(arr)
print(f"插入排序后的列表{result}")

