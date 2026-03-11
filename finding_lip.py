def challenge1(matrix: list[list[int]]) -> int:
    """
    Function that will return the longest increasing path (LIP) of the given matrix
    :param matrix: as above
    :return: The length of the longest increasing path
    """
    # Assign the matrix dimensions to variables m, n for easier accessibility
    m, n = len(matrix), len(matrix[0])

    # Dictionary in which we will store the computed values of LIP
    check = {}

    # Possible directions in which we can move from a cell
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Define the function that will calculate the longest increasing path
    # starting form cell (i, j)
    def lip(i: int, j: int) -> int:
        """
        Recursive function that will calculate the solution of cell (i,j)
        :param i: row-coordinate
        :param j: colum-coordinate
        :return: length of the LIP spawning from cell (i,j)
        """
        # Assign the value of the element in that cell to variable val for
        # easier accessibility
        val = matrix[i][j]

        # The length of the chain spawning from this cell is at least 1, since
        # the chain contains this cell itself
        res = 1

        # For every possible direction
        for move in moves:
            # Check if any of the constraints are not satisfied; if so, ignore
            # this move
            if (
                (i + move[0] < 0 or i + move[0] > m - 1)
                or (j + move[1] < 0 or j + move[1] > n - 1)
                or (matrix[i + move[0]][j + move[1]] <= val)
            ):
                continue

            # If the move is valid, first check if the length of the path
            # starting from the cell you're about to move to has already been
            # computed
            if (i + move[0], j + move[1]) in check:
                # If it has, use the stored value and update the current maximum
                res = max(res, check[i + move[0], j + move[1]] + 1)
            else:
                # If it hasn't, compute it recursively and update the current
                # maximum
                res = max(res, lip(i + move[0], j + move[1]) + 1)

        # After computing the longest path starting from this cell, store it in
        # the dictionary and return it
        check[(i, j)] = res
        return res

    # Compute lip for every cell in the matrix and return the overall maximum
    final_res = 0
    for i in range(m):
        for j in range(n):
            final_res = max(final_res, lip(i, j))

    return final_res


if __name__ == '__main__':

    import numpy as np
    import random
    import time

    # Examples with small matrices
    A = [
        [1, 2, 3],
        [2, 9, 4],
        [3, 4, 5]
    ]
    print(np.matrix(A), '\nLIP of matrix A: ', challenge1(A))
    print()

    B = [
        [4, 12, 8, 9],
        [7, 9, 2, 3],
        [5, 10, 1, 1]
    ]
    print(np.matrix(B), '\nLIP of matrix B: ', challenge1(B))
    print()

    C = [
        [21, 22, 23, 24, 25],
        [20, 7, 8, 9, 10],
        [19, 6, 1, 2, 11],
        [18, 5, 4, 3, 12],
        [17, 16, 15, 14, 13]
    ]
    print(np.matrix(C), '\nLIP of matrix C: ', challenge1(C))
    print()

    # Edge cases
    D = [[1] * 5 for _ in range(5)]
    print(np.matrix(D), '\nLIP of matrix D: ', challenge1(D))
    print()

    E = [[42]]
    print(np.matrix(E), '\nLIP of matrix E: ', challenge1(E))
    print()

    F = [[]]
    print(np.matrix(F), '\nLIP of matrix F: ', challenge1(F))
    print('-' * 40)

    # Some statistical analysis for following questions

    # Random small matrices, 2 <= m, n <= 10  -- average LIP turns out to
    # have length ~5.3
    print('For relatively small matrices:')
    lips_small = []
    for _ in range(1000):
        m, n = random.randint(2, 10), random.randint(2, 10)
        matrix = [[random.randint(1, 20) for _ in range(n)] for _ in range(m)]
        lips_small.append(challenge1(matrix))

    print(
        f'The average LIP of a small matrix is: '
        f'{sum(lips_small) / len(lips_small)}'
    )
    print(f'The maximum LIP of a small matrix is: {max(lips_small)}')

    outliers_small = [lip for lip in lips_small if not (3 <= lip <= 7)]
    print(
        'The percentage of small matrices whose LIP falls out of the range '
        f'[3, 7] is: {100 * len(outliers_small) / len(lips_small)}%'
    )
    print()

    # Random "medium" matrices (100 <= m*n <= 10000) -- average LIP turns out
    # to have length ~9.05
    print('For relatively medium matrices:')
    lips_medium = []
    durations = []

    for _ in range(1000):
        start_time = time.time()
        m, n = random.randint(10, 100), random.randint(10, 100)
        matrix = [[random.randint(1, 20) for _ in range(n)] for _ in range(m)]
        lips_medium.append(challenge1(matrix))
        durations.append(time.time() - start_time)

    print(
        f'The average LIP of a medium matrix is: '
        f'{sum(lips_medium) / len(lips_medium)}'
    )
    print(f'The maximum LIP of a medium matrix is: {max(lips_medium)}')
    print(
        'The average duration to calculate the LIP of a medium matrix is: '
        f'{sum(durations) / len(durations)}'
    )

    outliers_medium = [lip for lip in lips_medium if not (6 <= lip <= 12)]
    print(
        'The percentage of medium matrices whose LIP falls out of the range '
        f'[6, 12] is: {100 * len(outliers_medium) / len(lips_medium)}%'
    )
    print()

    # Random large matrices (10000 <= m*n <= 1000000) - average LIP turns out
    # to be ~11.4
    print('For relatively large matrices:')
    lips_large = []
    durations = []

    for _ in range(100):  # average time per calculation ~1 second - multithreading could be useful here
        start_time = time.time()
        m, n = random.randint(100, 1000), random.randint(100, 1000)
        matrix = [[random.randint(1, 20) for _ in range(n)] for _ in range(m)]
        lips_large.append(challenge1(matrix))
        durations.append(time.time() - start_time)
        print('done')

    print(
        f'The average LIP of a large matrix is: '
        f'{sum(lips_large) / len(lips_large)}'
    )
    print(f'The maximum LIP of a large matrix is: {max(lips_large)}')
    print(
        'The average duration to calculate the LIP of a large matrix is: '
        f'{sum(durations) / len(durations)}'
    )

    outliers_large = [lip for lip in lips_large if not (8 <= lip <= 14)]
    print(
        'The percentage of large matrices whose LIP falls out of the range '
        f'[8, 14] is: {100 * len(outliers_large) / len(lips_large)}%'
    )
    print()

    # Random medium matrices but with high element variance -
    # average LIP turns out to have length ~10.5
    print('For relatively medium matrices with large variance:')
    lips_var = []

    for _ in range(1000):
        m, n = random.randint(10, 100), random.randint(10, 100)
        matrix = [[random.randint(1, 20) for _ in range(n)] for _ in range(m)]
        lips_var.append(challenge1(matrix))

    print(
        'The average LIP of a random matrix with large variance is: '
        f'{sum(lips_var) / len(lips_var)}'
    )
    print(
        f'The maximum LIP of a random matrix with variance is: '
        f'{max(lips_var)}'
    )

    outliers_var = [lip for lip in lips_var if not (7 <= lip <= 13)]
    print(
        'The percentage of medium matrices with large variance whose LIP '
        f'falls out of the range [7, 13] is: '
        f'{100 * len(outliers_var) / len(lips_var)}%'
    )
