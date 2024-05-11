import random


def main():
    size = get_positive_integer("Enter the size of list: ")
    seed = get_positive_integer("Enter the seed: ")

    rand_list = rand_tuple(size, seed)

    print(f"Unsorted: {rand_list}")
    print()

    div_n_con = div_algo(rand_list)
    print(f"Divide and Conquer: {div_n_con} Total activities: {len(div_n_con)}")
    print()

    dynamic = dynamic_algo(rand_list)
    print(f"Dynamic Programming: {dynamic} Total activities: {len(dynamic)}")
    print()

    greed = greedy_algo(rand_list)
    print(f"Greedy algo: {greed} Total activities: {len(greed)}")
    print()

    print(f"Sorted: {rand_list}")


def greedy_algo(activities):
    # Sort activities by finish time
    activities.sort(key=lambda x: x[1])

    # The first activity is always selected
    i = 0
    final = [activities[0]]
    size = len(activities)

    # Consider rest of the activities
    for j in range(size):
        # If this activity has start time greater than or equal to the finish time of previously selected activity, then select it
        if activities[j][0] >= activities[i][1]:
            final.append(activities[j])
            i = j
    return final


def div_algo(activities):
    if len(activities) <= 1:  # O(1)
        return activities

    mid = len(activities) // 2  # O(1)
    left = activities[:mid]   # O(1)
    right = activities[mid:]  # O(1)

    left = div_algo(left)  # O(n/2)
    right = div_algo(right)  # O(n/2)

    return merge(left, right)  # O(n)


def merge(left, right):
    merged = []
    i = j = 0  # O(1)

    while i < len(left) and j < len(right):  # O(n)
        if merged:
            # Case where merged[] has content/s
            # Check for activity with the least finish time
            if left[i][1] < right[j][1] and left[i][0] >= merged[-1][1]:
                merged.append(left[i])  # O(1)
                i += 1
            elif left[i][1] > right[j][1] and right[j][0] >= merged[-1][1]:
                merged.append(right[j])  # O(1)
                j += 1  # O(1)
            else:
                # If finish times are the same, choose the one that has lesser duration
                if left[i][1] - left[i][0] <= right[j][1] - right[j][0] and left[i][0] >= merged[-1][1]:
                    merged.append(left[i])  # O(1)
                    i += 1  # O(1)
                else:
                    if right[j][0] >= merged[-1][1]:
                        merged.append(right[j])  # O(1)
                    j += 1  # O(1)
        else:
            # Case where merged[] is empty
            # Check for activity with the least finish time
            if left[i][1] < right[j][1]:
                merged.append(left[i])  # O(1)
                i += 1  # O(1)
            elif left[i][1] > right[j][1]:
                merged.append(right[j])  # O(1)
                j += 1  # O(1)
            else:
                # Filter for overlapping time and same finish time
                # If finish times are the same, choose the one that has lesser duration
                if left[i][1] - left[i][0] <= right[j][1] - right[j][0]:
                    merged.append(left[i])  # O(1)
                    i += 1  # O(1)
                else:
                    merged.append(right[j])  # O(1)
                    j += 1  # O(1)

    # Append any remaining activities from either list
    while i < len(left) or j < len(right):  # O(n)
        # If there are activities in both halves
        if i < len(left) and j < len(right):
            left_act = left[i]  # O(1)
            right_act = right[j]  # O(1)
            # Choose the activity with the lowest duration
            if left_act[1] - left_act[0] < right_act[1] - right_act[0]:
                if not merged or left_act[0] >= merged[-1][1]:
                    merged.append(left_act)  # O(1)
                i += 1  # O(1)
            else:
                if not merged or right_act[0] >= merged[-1][1]:
                    merged.append(right_act)  # O(1)
                j += 1  # O(1)
        # If there are only activities in the left half
        elif i < len(left):
            left_act = left[i]  # O(1)
            if not merged or left_act[0] >= merged[-1][1]:
                merged.append(left_act)  # O(1)
            i += 1  # O(1)
        # If there are only activities in the right half
        elif j < len(right):
            right_act = right[j]  # O(1)
            if not merged or right_act[0] >= merged[-1][1]:
                merged.append(right_act)  # O(1)
            j += 1  # O(1)

    return merged


def dynamic_algo(activities):
    # Sort activities according to their finish time
    activities.sort(key=lambda x: x[1])

    n = len(activities)

    # Array to store solutions of sub-problems
    dp = [0 for _ in range(n)]
    selected = [[] for _ in range(n)]

    # The first activity always gets selected
    dp[0] = 1
    selected[0] = [activities[0]]

    # Fill entries in dp[] using for-loop
    for i in range(1, n):
        # Find the maximum number of activities that can be performed by including the i-th activity
        for j in range(i):
            if activities[j][1] <= activities[i][0] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                selected[i] = selected[j].copy()
        if not selected[i] or (selected[i] and selected[i][-1][1] <= activities[i][0]):
            selected[i].append(activities[i])

    # Find the index of the maximum value in dp[]
    max_index = dp.index(max(dp))

    return selected[max_index]


def rand_tuple(size, seed):
    random.seed(seed)

    tuple_list = []
    for _ in range(size):
        while True:
            s = random.randint(1, 24)
            f = random.randint(1, 24)
            # Start time is less than finish time
            if s < f:
                # Avoid duplicates
                if (s, f) not in tuple_list:
                    tuple_list.append((s, f))
                    break
    return tuple_list


# For handling input verification
def get_positive_integer(n):
    while True:
        try:
            value = int(input(n))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Please enter a positive integer.")


if __name__ == "__main__":
    main()
