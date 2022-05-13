import numpy as np


def unit_vector(vector):
    """Returns the unit vector of the vector."""
    return vector / np.linalg.norm(vector)


def get_vectors_angle(first_vector, second_vector):
    """Returns the angle between two vectors"""
    v1_u = unit_vector(first_vector)
    v2_u = unit_vector(second_vector)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def close_geometry(geometry) -> Polygon:
    if geometry.empty or geometry[0].empty:
        return geometry  # empty

    if geometry[-1][-1] == geometry[0][0]:
        return geometry  # already closed

    result = None
    for linestring in geom:
        if result is None:
            resultstring = linestring.clone()
        else:
            resultstring.extend(linestring.coords)

    geom = Polygon(resultstring)

    return geom
