def binary_search(num_list,target_num):
    num_list.sort()  #从小到大进行排序，会改变原始列表，sorted()函数不会改变原始列表
    low = 0
    hight = len(num_list) - 1
    while low <= hight:
        mid = (low + hight)  //2
        mid_num = num_list[mid]
        if mid_num == target_num:
            return mid
        elif mid_num > target_num:
            hight = mid -1
        else:
            low = mid + 1
    return None
num_list = [6,4,7,8,1,3,8]
target_num = 3
result = binary_search(num_list,target_num)
print(f"排序后的列表：{num_list}")
if result !=None:
    print(f"找到目标值{target_num}在索引{result}")
else:
    print("未找到元素!")
