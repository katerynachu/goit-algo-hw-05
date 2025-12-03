def binary_search_bounds(array,target):
    i = 0
    low = 0
    high = len(array) - 1
    upper_bound = None

    while low <= high:
        i +=1
        mid = (low + high) // 2 
        guess = array[mid]
        if guess == target:
            upper_bound = guess
            break
        if guess > target:
            upper_bound = guess
            high = mid - 1
        if guess < target:
            low = mid + 1  
    return (i, upper_bound)       

data = [1.5, 3.2, 4.0, 6.8, 8.5, 9.1]

print(binary_search_bounds(data,6.0))


