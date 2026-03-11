import random
import time
from helper_functions import challenge1_modified as ch

# Thresholds based on empirical results
LIP_THRESHOLDS = {
    "very_small": 6,   # e.g., mn <= 25
    "small": 10,       # e.g., 10x10
    "medium": 15,      # e.g., 50x50
    "large": 22        # maximum considered
}

def estimate_threshold(m, n):
    """Return threshold of LIPs based on matrix size."""
    if m*n <= 25:
        return LIP_THRESHOLDS["very_small"]
    elif m*n <= 100:
        return LIP_THRESHOLDS["small"]
    elif m*n <= 2500:
        return LIP_THRESHOLDS["medium"]
    else:
        return LIP_THRESHOLDS["large"]


def generate_matrix_with_LIPs(m, n, p, low=1, high=30):
    """
    returns a random matrix of size m x n
    containing at least p LIPs, or raises an error if p is impossible.
    """
    max_attempts = 500
    threshold = estimate_threshold(m, n)
    if p > threshold:
        raise ValueError(f"Requested p={p} exceeds threshold {threshold} for {m}x{n} matrix.")

    attempts = 0
    start_time = time.time()

    while attempts < max_attempts:
        attempts += 1
        matrix = [[random.randint(low, high) for _ in range(n)] for _ in range(m)]
        lip_length, spawns = ch(matrix)

        if len(spawns) >= p:
            return matrix

    raise RuntimeError(f"Failed to generate a matrix with  at least {p} LIP's after {max_attempts} attempts.")



if __name__ == "__main__":
    m, n, p = 5, 5, 6  # specify the matrix size and the number of LIP's that must be contained inside
    low, high = 1, 10  # specify the range within which the values of the matrix are going to be picked
    matrix = generate_matrix_with_LIPs(m, n, p,  low, high)
    for row in matrix:
        print(row)
