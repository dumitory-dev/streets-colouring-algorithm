""""File for the Line object class."""
from shapely.geometry import Point, shape


class LineException(Exception):
    """Exception for the Line class."""


class Line:
    """The Line object class
    A class for convenient operations on lines"""

    def __init__(self, line_id: str, geometry):
        self.line_id = line_id
        self.coordinates = Line._make_coordinates_from_geometry(geometry)
        self.geometry = geometry

    @staticmethod
    def _make_coordinates_from_geometry(geometry):
        geometry_coordinates = geometry["coordinates"]
        return [
            Point(coordinate[0], coordinate[1]) for coordinate in geometry_coordinates
        ]

    @staticmethod
    def make_line_from_geometry(geometry):
        """Returns a line object from a geometry object"""
        return Line(geometry["id"], geometry["geometry"])

    def get_length(self):
        """Returns the distance of the line"""
        return self.make_shape_geometry().length

    def merge_line(self, line: "Line", point: Point):
        """Merges two Line objects. The result is one line."""

        if self.get_start() == point and line.get_start() == point:
            self.reverse_coordinates()
            self._update_coordinates(self.coordinates + line.coordinates)

        elif self.get_start() == point and line.get_end() == point:
            self._update_coordinates(line.coordinates + self.coordinates)

        elif self.get_end() == point and line.get_start() == point:
            self._update_coordinates(self.coordinates + line.coordinates)

        elif self.get_end() == point and line.get_end() == point:
            line.reverse_coordinates()
            self._update_coordinates(self.coordinates + line.coordinates)
        else:
            LineException(
                f"The lines do not intersect the point. Lines id: {self.line_id} and {line.line_id}, Point: {point.x}, {point.y}"
            )

    def _update_coordinates(self, coordinates):
        self.coordinates = coordinates
        self.geometry["coordinates"] = coordinates

    def reverse_coordinates(self):
        """Reverses the coordinates of the line"""
        self.coordinates.reverse()
        self.geometry["coordinates"] = self.coordinates

    def make_shape_geometry(self):
        """Returns a shapely geometry object from a geometry information"""
        return shape(self.geometry)

    def get_intersection(self, other_geometry):
        """Returns the intersection point of the line with the other geometry object"""
        return self.make_shape_geometry().intersection(other_geometry)

    def is_intersect(self, other_geometry):
        """Returns True if the line intersects with the other geometry object"""
        return self.make_shape_geometry().intersects(other_geometry)

    def get_start(self):
        """Returns the start point of the line."""
        return self.coordinates[0]

    def get_end(self):
        """Returns the end point of the line."""
        return self.coordinates[-1]

    def __hash__(self):
        return hash(self.line_id)

    def __eq__(self, other):
        return self.line_id == other.line_id

    def __ne__(self, other):  # needed for Python 3
        return not self.__eq__(other)

    def __repr__(self):
        return f"<Line {self.line_id}>"
