"""Functions for different line operations"""

import fiona
import numpy as np
from shapely.geometry import Point, Polygon, shape

from src.core import Line


def get_intersect_lines_for_point(point: Point, lines: list) -> list:
    """Returns a list of lines that intersect with the point"""
    out_data = []
    for line in lines:
        if line.get_start() == point or line.get_end() == point:
            out_data.append(line)
    return out_data


def get_circle_intersects(line: Line, circle: Polygon):
    """Returns a line that intersect with the circle"""
    intersection_point = line.get_intersection(shape(circle))

    # if intersection_point is MultiLineString,
    # We don't need to do anything,
    # it means that the intersection point itself is in the circle
    if intersection_point.geom_type != "LineString":
        return None

    intersection_data = intersection_point.coords.xy

    return (
        Point(intersection_data[0][0], intersection_data[1][0]),
        Point(intersection_data[0][1], intersection_data[1][1]),
    )


def get_lines_from_file(path_to_shp):
    """Returns a list of all lines objects from a shapefile"""
    shape_file = fiona.open(path_to_shp)
    lines = []
    for geometry in shape_file:
        lines.append(Line.make_line_from_geometry(geometry))
    return lines


def get_intersect_points(lines: list):
    """Returns a list of all lines objects from a shapefile"""

    intersect_points = {}

    for line in lines:
        (start, end) = (line.get_start(), line.get_end())

        # convert to tuple, because Point is not hashable
        start = (start.x, start.y)
        end = (end.x, end.y)

        if intersect_points.get(start) is None:
            intersect_points[start] = False
        else:
            intersect_points[start] = True

        if intersect_points.get(end) is None:
            intersect_points[end] = False
        else:
            intersect_points[end] = True
    # get points with lines greater than two
    return dict(filter(lambda x: bool(x[1]), intersect_points.items()))


def plot_all_lines(plt, lines: list):
    """Plots all lines from a list with random colors."""
    for line in lines:
        line_coordinates = line.coordinates
        # convert coordinates to xy
        x_array = [coordinate.x for coordinate in line_coordinates]
        y_array = [coordinate.y for coordinate in line_coordinates]
        # plot with unqie color
        plt.plot(
            x_array,
            y_array,
            color=np.random.rand(
                3,
            ),
            linewidth=0.3,
        )
