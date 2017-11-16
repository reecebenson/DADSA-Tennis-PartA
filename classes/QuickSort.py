"""Pure implementation of quick sort algorithm in Python"""
def quick_sort(arr):
    arr_len = len(arr)

    if(arr_len <= 1):
        return arr
    else:
        piv = arr[0]
        gt  = [ e for e in arr[1:] if e > piv ]
        lt  = [ e for e in arr[1:] if e <= piv ]
        return quick_sort(lt) + [piv] + quick_sort(gt)