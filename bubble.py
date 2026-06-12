bubble_list1 = [1,2,3,9,0,3,0,0,3,2,5]
# bubble_list2 = [0,1,2,3,9,0,3,0,3,2,5] # after iteration 1
# bubble_list3 = [0,0,1,2,3,9,0,3,3,2,5] # after iteration 2
# bubble_list4 = [0,0,0,1,2,3,9,3,3,2,5] # after iteration 3

def bubble(arr):
    
    for n in arr:
        if n == 0:
            arr.remove(n)
            arr.insert(0, n)
    return arr

sorted_bubble_list = bubble(bubble_list1)

print(sorted_bubble_list)