"""Main module for running the application."""

import argparse
import os
from itertools import combinations

from matplotlib import pyplot as plt
from shapely.geometry import Point, shape
from tqdm import tqdm

from src.utils import (
    get_circle_intersects,
    get_intersect_lines_for_point,
    get_intersect_points,
    get_lines_from_file,
    plot_all_lines,
)

OUT_FILE_NAME = "roads.png"


def get_command_line_params():
    """Returns the command line parameters"""

    parser = argparse.ArgumentParser(description="Streets Colouring Program")
    parser.add_argument(
        "-i", "--input", required=True, help="Path to the input shapefile"
    )
    parser.add_argument(
        "-o",
        "--output",
        default="./out",
        help="Path to the output directory",
    )
    parser.add_argument(
        "-d", "--dpi", default=300, help="Set the out image dpi", type=int
    )
    return parser.parse_args()


if __name__ == "__main__":
    params = get_command_line_params()
    input_path, out_dir, dpi = (
        params.input,
        params.output,
        params.dpi,
    )

    # Check if input file exists
    if not os.path.isfile(input_path):
        raise Exception(f"File {input_path} does not exist")

    # create the output directory if it doesn't exist
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # make out dir with out file name
    out_file_path = f"{out_dir}/{OUT_FILE_NAME}"

    plt.figure()

    all_lines = get_lines_from_file(input_path)

    # get the minimum distance for the radius of the circle
    minimal_distance = min(all_lines, key=lambda x: x.get_length()).get_length()
    intersect_points = get_intersect_points(all_lines)

    """
    1. Generate a circle at the intersection of the lines with the radius of the shortest line
    2. Find the points and lines of intersection of the circle radius
    3. Sort the points by their distance from each other
    4. Merge the lines with the longest distance in descending order
    
    Note: Since we end up merging all the lines we need,
    we can even make a new shp file with the streets!
               
         #####
        #  |  #
        #  |  #
    ----#--+--#----
        #  |  #
        #  |  #
         #####
    """
    for point in tqdm(intersect_points.items()):
        point = Point(point[0], point[1])
        circle = point.buffer(minimal_distance)

        # Place for optimization,
        # we do not need to always recalculate the lines for the intersection point this way,
        # but so far this is the easiest option
        intersect_lines = get_intersect_lines_for_point(point, all_lines)
        intersect_data_circle = []

        for line in intersect_lines:
            intersect_circle_result = get_circle_intersects(line, circle)

            if intersect_circle_result is None:
                continue
            (begin, end) = intersect_circle_result

            if begin != point:
                intersect_data_circle.append((begin, line))
            else:
                intersect_data_circle.append((end, line))

        # We want to sort the lines by the distance between them.
        # The lines whose points are at the greatest distance, we will merge
        sorted_distances = list(
            map(
                lambda x: (x[0][1], x[1][1]),
                sorted(
                    combinations(intersect_data_circle, 2),
                    key=lambda x: x[0][0].distance(x[1][0]),
                    reverse=True,
                ),
            )
        )

        # We only can connect two lines per iteration
        for i in range(0, int(len(intersect_data_circle) / 2)):
            (first_line, second_line) = sorted_distances[i]

            if first_line not in all_lines or second_line not in all_lines:
                continue

            first_line.merge_line(second_line, point)
            all_lines.remove(second_line)

    plot_all_lines(plt, all_lines)
    plt.savefig(out_file_path, dpi=dpi)
