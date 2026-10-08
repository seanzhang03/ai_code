arr = [64,34,43,12,22,11,55]
i = 1
def selection_sort(arr):
    for i in range(len(arr)): #其实也相当于冒泡排序中，每次剔除一个元素，最坏情况执行len(arr)次
        min_idx = i
        for j in range(i+1,len(arr)):  #从第i个元素后的所有元素跟第i个元素进行大小比较
            if arr[min_idx] > arr[j]:
                min_idx = j  #找到i之后的最小的那个元素的索引，以来将最小值更新为j索引的值
        arr[i],arr[min_idx] = arr[min_idx],arr[i]  #遍历完i后的元素，找到了最小值的索引，将i对应值和最小值进行位置交换
    return arr

result = selection_sort(arr)
print(f"选择排序后的列表:{result}")