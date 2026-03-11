from finding_lip import challenge1
import random
from itertools import cycle
import math
import time


def create_matrix_with_lip_in_given_range(m: int, n: int, lower: int, upper: int) -> list[list[int]]:
    """
    Create an m x n matrix whose longest increasing path (LIP) falls within
    a given range [lower, upper].

    If the desired LIP is small, it can emerge naturally in a random matrix.
    Otherwise, the path is constructed manually to ensure the minimum length.

    m, n: Dimensions of the matrix
    lower, upper: Desired range for the LIP
    :return: A matrix meeting the specified LIP constraints
    """
    matrix = [[0] * n for _ in range(m)]
    threshold = math.log(m * n) + 5

    # Case 1: the desired LIP is small, we can rely on random generation
    if lower < threshold:
        res = -1
        # Keep generating random matrices until the LIP is in the desired range
        while not lower <= res <= upper:
            matrix = matrix = [[random.randint(1, 100) for _ in range(n)] for _ in range(m)]
            res = challenge1(matrix)
        return matrix

    # Case 2: we need to construct the path ourselves to guarantee the minimum LIP because it's rare to
    # randomly fall into the given range
    else:
        # start from the top-left corner
        i, j = 0, 0
        # define movement directions
        right, left, up, down = (0, 1), (0, -1), (-1, 0), (1, 0)
        directions = cycle([down, left, up, right])  # cycle through directions for spiral-like path

        path_len = 1
        matrix[i][j] = random.randint(1, 100)  # initial value
        chain = {(i, j)}
        prev_val = matrix[i][j]
        move = right  # initial move

        # Build the path to ensure length of LIP is at least lower
        while path_len < lower:
            ni, nj = i + move[0], j + move[1]
            if not (0 <= ni < m and 0 <= nj < n) or (ni, nj) in chain:
                move = next(directions)
                continue
            i, j = ni, nj
            matrix[i][j] = prev_val + 1
            prev_val = matrix[i][j]
            path_len += 1
            chain.add((i, j))

        # Fill the remaining cells, ensuring the LIP does not exceed upper
        res = -1
        while res < lower or res > upper:
            for x in range(m):
                for y in range(n):
                    if (x, y) not in chain:
                        matrix[x][y] = random.randint(1, 100)
            res = challenge1(matrix)
        return matrix



if __name__ == "__main__":
    import numpy as np

    # Example 1: Small matrix
    start_time = time.time()
    mat1 = create_matrix_with_lip_in_given_range(5, 5, 3, 6)
    end_time = time.time()
    print(np.matrix(mat1))
    print(challenge1(mat1))
    print("Time taken:", end_time - start_time, "\n")

    # Example 2: Medium matrix
    start_time = time.time()
    mat2 = create_matrix_with_lip_in_given_range(20, 20, 6, 10)
    end_time = time.time()
    print(np.matrix(mat2))
    print(challenge1(mat2))
    print("Time taken:", end_time - start_time, "\n")

    # Example 3: Large matrix
    start_time = time.time()
    mat3 = create_matrix_with_lip_in_given_range(100, 100, 50, 10000)
    end_time = time.time()
    print(np.matrix(mat3))
    print(challenge1(mat3))
    print("Time taken:", end_time - start_time)

    # Example 3: Large matrix with small LIP
    start_time = time.time()
    mat4 = create_matrix_with_lip_in_given_range(100, 100, 3, 7)
    end_time = time.time()
    print(np.matrix(mat4))
    print(challenge1(mat4))
    print("Time taken:", end_time - start_time)
