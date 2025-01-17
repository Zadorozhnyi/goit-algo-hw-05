def binary_search(arr, target):
    # Implements binary search for a sorted array of floating-point numbers.
    # Returns a tuple (number of iterations, upper bound).

    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2

        if arr[mid] == target:
            # Found exact match
            return iterations, arr[mid]
        
        if arr[mid] < target:
            left = mid + 1
        else:
            # Update upper bound
            upper_bound = arr[mid]
            right = mid - 1
            
    # Return the closest larger element if target is not found
    return iterations, upper_bound 

# Example usage
sorted_array = [0.5, 1.2, 2.3, 3.5, 4.8, 5.9, 7.1, 8.6, 9.9]
target_value = 4.0

# Run and print results
result = binary_search(sorted_array, target_value)
print("Number of iterations:", result[0])
print("Upper bound:", result[1])
