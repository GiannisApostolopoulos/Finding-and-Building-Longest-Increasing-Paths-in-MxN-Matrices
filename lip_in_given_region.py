import random
import helper_functions as hf


def lip_into_region(m: int, n: int, region: list[int]) -> list[list[int]]:
    """
    Function that will generate a matrix whose longest increasing path (LIP)
    is restricted to lie entirely inside a user-specified sub-region.

    :param m: number of rows
    :param n: number of columns
    :param region: list with bounds of the sub-region [lower, upper, left, right]
                   where the path is allowed to move
    :return: matrix satisfying the constraints
    """

    # Extract the boundary limits of the region in which the path must remain
    lower, upper, left, right = region

    # Initialize the matrix with None values for clarity
    matrix = [[None] * n for _ in range(m)]

    # Possible moves from any cell: up, down, left, right
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Select a random starting point inside the required region
    starting_i = random.randint(lower, upper)
    starting_j = random.randint(left, right)

    # Assign an initial random value to the starting cell
    matrix[starting_i][starting_j] = random.randint(1, 100)

    # Chain will hold the cells that form the increasing path
    chain = [(starting_i, starting_j)]

    # The LIP always starts with length 1 (single cell)
    path_len = 1
    i, j = starting_i, starting_j
    prev_val = matrix[i][j]

    # Keep extending the chain until no valid moves remain
    while True:
        valid_moves = []

        # Check all possible moves from the current cell
        for move in moves:
            ni, nj = i + move[0], j + move[1]

            # Move must stay inside the region and must not revisit the chain
            if (lower <= ni <= upper and left <= nj <= right
                    and (ni, nj) not in chain):
                valid_moves.append(move)

        # If there are no valid moves, the chain cannot be extended further
        if not valid_moves:
            break

        # Choose one of the valid moves randomly
        move = random.choice(valid_moves)
        i += move[0]
        j += move[1]

        # Assign a strictly increasing value
        matrix[i][j] = random.randint(prev_val + 1, prev_val + 5)
        prev_val = matrix[i][j]

        # Update path length and record the new cell
        path_len += 1
        chain.append((i, j))

    # Barrier the path to guarantee that the LIP does not accidentally extend
    matrix, filled = hf.barrier_path(matrix, chain, m, n)

    # All cells belonging to the chain or the barrier
    chain_set = set(chain).union(filled)

    # Fill the remaining non-path, non-barrier cells
    for i in range(m):
        for j in range(n):
            if (i, j) not in chain_set:
                # Fill with values that cannot extend the LIP
                matrix[i][j] = random.randint(1, path_len - 1)
                chain_set.add((i, j))

    return matrix



if __name__ == "__main__":

    from finding_lip import challenge1

    # Test 1: Medium-size matrix with a centered region
    print("Test case 1: 20x20 matrix, central 10x10 region")
    mat1 = lip_into_region(20, 20, [5, 14, 5, 14])
    print("Computed LIP =", challenge1(mat1))

    # Test 2: Small region (harder case)
    print("\nTest case 2: 15x15 matrix, tiny 3x3 region")
    mat2 = lip_into_region(15, 15, [6, 8, 6, 8])
    print("Computed LIP =", challenge1(mat2))

    # Test 3: Region equals full matrix (should behave like general LIP)
    print("\nTest case 3: Full-region 12x12 matrix")
    mat3 = lip_into_region(12, 12, [0, 11, 0, 11])
    print("Computed LIP =", challenge1(mat3))

    # Edge case 2: Very narrow region (1xN horizontal strip)
    print("\nEdge case 2: Horizontal strip region")
    mat5 = lip_into_region(10, 10, [5, 5, 2, 8])
    print("Computed LIP =", challenge1(mat5))

    # Edge case 3: Very narrow region (Mx1 vertical strip)
    print("\nEdge case 3: Vertical strip region")
    mat6 = lip_into_region(10, 10, [2, 8, 4, 4])
    print("Computed LIP =", challenge1(mat6))

