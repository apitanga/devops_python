def two_sum(nums, target):
    seen_numbers = {}  # This dictionary will store numbers and their indices

    # Now we go through each number in the list
    for i, number in enumerate(nums):
        # We calculate what number is needed to reach the target
        needed_number = target - number

        # Check if this needed number is in our dictionary
        if needed_number in seen_numbers:
            # If it is, we found our two numbers: number and needed_number
            # We return their indices
            return [seen_numbers[needed_number], i]

        # If not, we add the current number and its index to the dictionary
        seen_numbers[number] = i

    # If we finish the loop and didn't return, there's no solution
    return []

def two_sum_brute_force(nums, target):
    # Iterate over each number in the list
    for i in range(len(nums)):
        # Iterate over each other number in the list
        for j in range(i + 1, len(nums)):
            # Check if the current pair adds up to the target
            if nums[i] + nums[j] == target:
                # If they do, return their indices
                return [i, j]
    # If no pair is found, return an empty list
    return []
