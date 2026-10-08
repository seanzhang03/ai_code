def bubble_sort(arr):
    for i in range(1,len(arr)):  #最坏情况要排len(arr)-1次
        for j in range(0,len(arr)-i):  #第一轮-1 第二轮-1 每次就相当于-i,相当于每次将最大的那个元素剔除掉，剩下的元素进行位置交换  
            if arr[j] > arr[j+1]:
                arr[j],arr[j+1] = arr[j+1],arr[j]
    return arr

arr = [64,34,25,12,22,11,55]
result = bubble_sort(arr)
print(f"冒泡排序后为{arr}")