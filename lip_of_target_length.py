from finding_lip import challenge1
import helper_functions as hf
import random
from itertools import cycle


def create_random_matrix_with_target_lip(m: int, n: int, target: int) -> list[list[int]]:
    """
    Create an m x n matrix whose longest increasing path (LIP) has a 
    specific target length.

    The function handles three cases:
    1. target = 1 -> all cells have the same value
    2. target is very small relative to the matrix → random generation 
       until the LIP equals target
    3. Otherwise -> construct a guaranteed path of length target and
       fill the rest of the matrix while preventing longer paths.
    """

    # Case 1: target = 1, we just fill the matrix with the same value
    if target == 1:
        val = random.randint(1, 100)
        return [[val for _ in range(n)] for _ in range(m)]

    # Case 2: target is very small, rely on random generation
    if target < 10 :
        res = -1
        # Keep generating matrices until the LIP equals target
        while res != target:
            val = random.randint(1, 100)
            matrix = [
                [random.randint(val, val + target - 1) for _ in range(n)]
                for _ in range(m)
            ]
            res = challenge1(matrix)

        return matrix

    # Case 3: target is large enough that we need to construct the path manually
    matrix = [[0 for _ in range(n)] for _ in range(m)]
    i, j = 0, 0  # start creating the path from the top-left cell

    # Define possible move directions: right, left, up, down
    right, left, up, down = (0, 1), (0, -1), (-1, 0), (1, 0)
    directions = cycle([down, left, up, right])  # cycle directions for spiral-like path

    path_len = 1
    val = random.randint(1, 100)
    matrix[i][j] = val  # assign the first value
    chain = {(i, j)}  # set to store the path coordinates
    path = [(i, j)]   # list to preserve order of path
    prev_val = matrix[i][j]
    move = right  # initial move

    # Build the increasing path
    while path_len < target:
        # If next move is out of bounds or already in the chain, change direction
        if (not (0 <= i + move[0] < m and 0 <= j + move[1] < n)) or \
           ((i + move[0], j + move[1]) in chain):
            move = next(directions)
            continue

        # Update coordinates
        i += move[0]
        j += move[1]

        # Assign increasing value to the new cell
        matrix[i][j] = prev_val + random.randint(1, 3)
        prev_val = matrix[i][j]

        # Update path tracking
        path_len += 1
        chain.add((i, j))
        path.append((i, j))

    # Barrier the path to prevent accidental longer increasing paths
    matrix, filled = hf.barrier_path(matrix, path, m, n)

    # Fill the remaining cells randomly within the safe range
    fill = random.randint(1, 100)
    for i in range(m):
        for j in range(n):
            if (i, j) not in filled:
                matrix[i][j] = random.randint(val, val + target)

    return matrix


if __name__ == '__main__':
    import time

    flags = []
    start_time = time.time()
    for _ in range(1000):
        target = random.choice(range(1, 50))
        small = create_random_matrix_with_target_lip(10, 10, target)
        med = create_random_matrix_with_target_lip(40, 40, target)
        big = create_random_matrix_with_target_lip(100, 100, target)
        flag = (challenge1(small) == target) and (challenge1(big) == target) and (challenge1(med) == target)
        flags.append(flag)
    total_time = time.time() - start_time
    print(all(flags))
    print(f'Average time for the generation of a matrix: {total_time / 1000}')  # ~ 0.06 in my machine


