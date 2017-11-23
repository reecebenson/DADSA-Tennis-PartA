"""Pure implementation of quick sort algorithm in Python"""
def quick_sort(arr, attr = None):
    arr_len = len(arr)

    if(arr_len <= 1):
        return arr
    else:
        piv = None
        gt = None
        lt = None

        if(attr == None):
            piv = arr[0]
            gt  = [ e for e in arr[1:] if e > piv ]
            lt  = [ e for e in arr[1:] if e <= piv ]
        else:
            piv = arr[0]
            gt  = [ e for e in arr[1:] if e.highest_score(attr, False) > piv.highest_score(attr, False) ]
            lt  = [ e for e in arr[1:] if e.highest_score(attr, False) <= piv.highest_score(attr, False) ]


        return quick_sort(lt, attr) + [piv] + quick_sort(gt, attr)