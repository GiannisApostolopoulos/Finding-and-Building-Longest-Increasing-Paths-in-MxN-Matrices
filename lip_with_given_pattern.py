
import helper_functions as hf


def create_matrix_with_given_pattern(m: int, n: int, pattern: list[tuple[int, int]]) -> list[list[int]]:
    """Create a random m x n matrix where the LIP follows a given pattern.

    pattern: list of moves (dx, dy) defining shape we want to give the LIP.
    m, n: Number of rows, columns in the matrix
    """
    import random
    import math

    # Initialize an empty matrix
    matrix = [[0] * n for _ in range(m)]

    # Choose a starting position. For the demonstrations here, we define the starting cell to be always in the center
    # of the matrix. We could choose this randomly, but it would frequently mess up our structures in the examples
    starting_i, starting_j = m // 2, n // 2
    starting_value = random.randint(1, 100)
    matrix[starting_i][starting_j] = starting_value

    # Initialize the chain (longest increasing path)
    chain_len = 1
    chain = [(starting_i, starting_j)]

    i, j = starting_i, starting_j

    # Build the longest increasing path according to the pattern
    for move in pattern:
        prev_val = matrix[i][j]
        if not ((0 <= i + move[0] < m) and (0 <= j + move[1] < n)):
            break  # if there is no space to build the patter, abandon and work with what you have until now
        i += move[0]
        j += move[1]
        matrix[i][j] = random.randint(prev_val + 1, prev_val + 3)
        chain.append((i, j))
        chain_len += 1

    # Apply the barrier function to prevent other increasing paths from overtaking
    # filled = barrier_path(matrix, chain, m, n)
    matrix, filled = hf.barrier_path(matrix, chain, m, n)

    # Fill remaining cells randomly, avoiding the filled positions
    if  len(pattern)  + 1 < math.log(m*n) - 1:
        # In this case, we are looking for an "outlier", and by randomly generating the rest of the elements would
        # need many attempts to achieve the desired result, so we fill manually
        # Careful that we don't want to accidentally create a longer LIP than the one we constructed, so we must limit the
        # length of the interval from which we are going to choose values to fill the matrix
        starting_value_to_fill = random.randint(1, chain_len - 1)
        for i in range(m):
            for j in range(n):
                if (i, j) not in filled:
                    matrix[i][j] = random.randint(
                        starting_value_to_fill, starting_value_to_fill + chain_len - 1
                    )
    else:
        from finding_lip import challenge1
        res = -1
        while res != len(pattern) + 1:
            for i in range(m):
                for j in range(n):
                    if (i, j) not in filled:
                        matrix[i][j] = random.randint(1, 100)
            res = challenge1(matrix)
    return matrix



if __name__ == "__main__":
    from finding_lip import challenge1
    import numpy as np

    snake_pattern = [ (0, 1), (0, 1), (0, 1), (1, 0),  (0, -1), (0, -1), (0, -1) ]
    stairs_ascending = [(0, 1), (1, 0), (0, 1), (1, 0), (0, 1), (1, 0), (0, 1)]
    stairs_descending = [(0, -1), (-1, 0), (0, -1), (-1, 0), (0, -1), (-1, 0), (-1, 0)]
    spiral_inwards_counterclockwise = [
        (0, 1), (0, 1), (0, 1), (0, 1),  (1, 0), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1),
        (-1, 0), (-1, 0), (-1, 0), (0, 1), (0, 1), (0, 1), (1, 0), (1, 0), (0, -1), (0, -1), (-1, 0), (0, 1)
    ]
    spiral_outwards_clockwise = [
        (0, 1), (1, 0), (0, -1), (0, -1), (-1, 0), (-1, 0), (0, 1), (0, 1), (0, 1), (1, 0), (1, 0), (1, 0),
        (0, -1), (0, -1), (0, -1), (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, 1), (0, 1), (0, 1), (0, 1)
    ]

    print(np.matrix(create_matrix_with_given_pattern(10, 10, snake_pattern)), '\n')
    print(np.matrix(create_matrix_with_given_pattern(10, 10, stairs_ascending)), '\n')
    print(np.matrix(create_matrix_with_given_pattern(10, 10, stairs_descending)), '\n')
    print(np.matrix(create_matrix_with_given_pattern(10, 10, spiral_inwards_counterclockwise)), '\n')
    print(np.matrix(create_matrix_with_given_pattern(10, 10, spiral_outwards_clockwise)), '\n')


