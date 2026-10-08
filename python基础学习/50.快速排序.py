#快速排序：常见且高效的用分治策略的排序算法，通过选取基准元素，通过一次排序将待排序的数据分割成独立两部分
#小于基准的放左边，大于基准的放在右边，然后递归对左右两部分进行排序
def quick_sort(arr):
    #终止递归的条件
    if len(arr) <= 1:
        return arr
    #选择基准值
    pivot = arr[0]
    left = [x for x in arr if x <pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x>pivot]

    return quick_sort(left) + middle +quick_sort(right)
arr = [8,9,1,7,2,3,5,4,6,0]
result = quick_sort(arr)
print(result)