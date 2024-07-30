import numpy as np


def get_lowline_of_polylines(polylines):
    lowline = [min([polylines[i][j] for i in range(len(polylines))])
               for j in range(len(polylines[0]))]
    return lowline


def get_highline_of_polylines(polylines):
    return [max([polylines[i][j] for i in range(len(polylines))])
            for j in range(len(polylines[0]))]


def get_cos_sim(a: np.ndarray, b: np.ndarray) -> float:
    """
    Calculate the cosine similarity between two vectors.

    Parameters:
        a (np.ndarray): First vector.
        b (np.ndarray): Second vector.

    Returns:
        float: Cosine similarity between the two vectors.
    """
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)
