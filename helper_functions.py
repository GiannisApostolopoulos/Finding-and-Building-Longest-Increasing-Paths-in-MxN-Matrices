def are_adjacent(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1

def in_matrix(cell: tuple[int, int], matrix: list[list[int]]) -> bool:
    m, n = len(matrix), len(matrix[0])
    return (0 <= cell[0] < m) and (0 <= cell[1] < n)


def barrier_path(matrix: list[list[int]], chain: list[tuple], m: int, n: int):
    """
    Barrier the longest increasing path (LIP) in a matrix.

    This prevents other increasing paths from entering the constructed
    LIP, changing the final LIP.

    matrix: The matrix being filled to create the LIP.
    chain: The LIP to protect/barrier.
    m, n: Number of rows, columns in the matrix - serve as boundaries
    :return: A set of all cells filled, including LIP cells and barrier cells.
    """

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    filled = set(chain) # for faster lookups
    max_val = matrix[chain[-1][0]][chain[-1][1]]
    fill_val = max_val + 1  # We will surround the path with one number, larger than the maximum value of our path

    # Barrier all elements in the chain with values larger than the maximum value of the path, except for the last one,
    # which we will handle separately
    for i, j in chain:
        for d in directions:
            ni, nj = i + d[0], j + d[1]
            if (0 <= ni < m) and (0 <= nj < n) and (ni, nj) not in filled:
                matrix[ni][nj] = fill_val
                filled.add((ni, nj))

    # Special barrier for the last element of the chain. We can't surround this will elements larger than itself because
    # this will extend the path, so we will surround it with elements equal to it
    last_i, last_j = chain[-1]
    for d in directions:
        ni, nj = last_i + d[0], last_j + d[1]
        if (0 <= ni < m) and (0 <= nj < n) and (ni, nj) not in chain:
            matrix[ni][nj] = matrix[last_i][last_j]
            filled.add((ni, nj))

    return matrix, filled



def challenge1_modified(matrix: list[list[int]]):
    """
    Function that will return the length of the LIP of the given matrix, as well as the cells from which
    the paths with the maximum length spawn (thus giving as their count too)
    :param matrix: 2D list of integers
    :return: tuple (length of the longest increasing path, list of starting cells of LIPs)
    """
    # Matrix dimensions
    m, n = len(matrix), len(matrix[0])

    # Dictionary to store computed LIP values
    check = {}

    # Possible moves: right, down, left, up
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Recursive function to compute LIP starting from cell (i, j)
    def lip(i: int, j: int) -> int:
        val = matrix[i][j]
        res = 1  # At least the cell itself

        for move in moves:
            ni, nj = i + move[0], j + move[1]
            if ni < 0 or ni >= m or nj < 0 or nj >= n:
                continue
            if matrix[ni][nj] <= val:
                continue

            if (ni, nj) in check:
                res = max(res, check[(ni, nj)] + 1)
            else:
                res = max(res, lip(ni, nj) + 1)

        check[(i, j)] = res
        return res

    # Compute LIP for every cell
    final_res = 0
    spawns = []
    for i in range(m):
        for j in range(n):
            cur_lip = lip(i, j)
            if cur_lip > final_res:
                final_res = cur_lip
                spawns = [(i, j)]
            elif cur_lip == final_res:
                spawns.append((i, j))

    return final_res, spawns








