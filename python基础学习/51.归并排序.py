#典型的分治思想应用，将大问题分解成了两个小问题，分别解决这两个小问题，然后将解决的小问题合并起来，得到大问题的解
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left,right)

def merge(left,right):
    merged = []
    left_index = 0
    right_index = 0
    while left_index < len(left) and right_index < len(right): #判断是否有元素
        if left[left_index] < right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index+=1
    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged

arr = [8,9,1,7,2,3,5,4,6,0]
result = merge_sort(arr)
print(f"{result}")