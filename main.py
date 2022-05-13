import math
from typing import List
import geopandas as gpd
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from shapely.geometry import mapping
from itertools import combinations
import fiona
from dataclasses import dataclass
import shapefile as shp  # Requires the pyshp package
from collections import defaultdict

PATH_TO_SHP = "./data/roads.shp"
OUT_DIR = "./out"


if __name__ == "__main__":
    shapefile = gpd.read_file(PATH_TO_SHP)

    points = []
    multiline = shapefile["geometry"]
    plt.figure()

    lines = {}

    # find intersections and append to points list
    for line1, line2 in combinations(list(multiline), 2):
        if line1.intersects(line2):
            # get all coordinates of line1
            coords1 = line1.coords.xy
            coords2 = line2.coords.xy

            # get all intersections for lines

            points.append(line1.intersection(line2))

    for line in list(multiline):
        x, y = line.coords.xy
        # find x in points
        for point in points:
            if point.geom_type == "Point":
                if point.x == x[0]:
                    plt.plot(x, y)

    plt.savefig(f"{OUT_DIR}/road_with_points1.png", dpi=500)
