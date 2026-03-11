import random
import numpy as np
from finding_lip import challenge1


def freq(value, matrix):
    dim = len(matrix) * len(matrix[0])
    count = sum(row.count(value) for row in matrix)
    return count / dim


def unique_count(matrix):
    return len(set(val for row in matrix for val in row))


if __name__ == '__main__':

    np.random.seed(42)
    random.seed(42)

    distributions = ['normal', 'uniform', 'geometric']  # added geometric
    normal_ranges = {
        'thin': (0, 1),
        'medium': (0, 10),
        'long': (0, 100)
    }
    uniform_ranges = {
        'thin': (0, 10),
        'medium': (0, 100),
        'long': (0, 1000)
    }
    # For geometric, p values control skew
    geometric_ranges = {
        'thin': 0.1,  # more spread, larger numbers
        'medium': 0.3,
        'long': 0.5  # more small numbers
    }

    # Added 10×10 and 20×20 matrix sizes
    matrix_sizes = {
        'xs': (5, 5),
        's': (10, 10),
        'm': (20, 20),
        'l': (50, 50),
        'xl': (100, 150)
    }

    num_trials = 100

    for dist in distributions:
        # Select range dict
        ranges = normal_ranges if dist == 'normal' else (uniform_ranges if dist == 'uniform' else geometric_ranges)

        for rname, rrange in ranges.items():
            for sname, (rows, cols) in matrix_sizes.items():

                challenge_values = []
                unique_counts = []
                max_freqs = []
                min_freqs = []
                matrices_list = []

                for _ in range(num_trials):
                    # Generate matrix
                    if dist == 'normal':
                        mu, sigma = rrange
                        mat = np.random.normal(loc=mu, scale=sigma, size=(rows, cols))
                        mat = np.round(mat).astype(int)
                    elif dist == 'uniform':
                        low, high = rrange
                        mat = np.random.randint(low, high + 1, size=(rows, cols))
                    else:  # geometric
                        p = rrange
                        mat = np.random.geometric(p, size=(rows, cols))

                    matrix = mat.tolist()
                    matrices_list.append(matrix)

                    # Frequencies and unique count
                    elements = set(val for row in matrix for val in row)
                    freqs = [freq(val, matrix) for val in elements]
                    max_freqs.append(max(freqs))
                    min_freqs.append(min(freqs))
                    unique_counts.append(unique_count(matrix))

                    # challenge1
                    challenge_values.append(challenge1(matrix))

                # challenge1 analysis
                min_c = min(challenge_values)
                max_c = max(challenge_values)
                most_common = max(set(challenge_values), key=lambda x: challenge_values.count(x))
                most_common_count = challenge_values.count(most_common)

                avg_ucount = sum(unique_counts) / len(unique_counts)
                avg_max_freq = sum(max_freqs) / len(max_freqs)
                avg_min_freq = sum(min_freqs) / len(min_freqs)

                # Average matrix frequency for matrices where challenge1 == most_common
                matrix_freqs = []
                for i, mat in enumerate(matrices_list):
                    if challenge_values[i] == most_common:
                        elements = set(val for row in mat for val in row)
                        freqs = [freq(val, mat) for val in elements]
                        matrix_freqs.append(sum(freqs) / len(freqs))

                avg_matrix_freq = sum(matrix_freqs) / len(matrix_freqs) if matrix_freqs else 0

                print(f"Distribution: {dist}, Range: {rname}, Size: {sname} ({rows}x{cols})")
                print(f"  Average unique count: {avg_ucount:.2f}")
                print(f"  Average max frequency: {avg_max_freq:.4f}")
                print(f"  Average min frequency: {avg_min_freq:.4f}")
                print(
                    f"  challenge1 -> min: {min_c}, max: {max_c}, most common: {most_common} (occurred {most_common_count} times)")
                print(f"  Average frequency of matrices with challenge1 == most common: {avg_matrix_freq:.4f}")
                print("-" * 60)
