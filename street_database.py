from geometry import Vec, Segment


class StreetLookupException(Exception):
    pass


class InvalidStreetException(Exception):
    pass


class Street:
    def __init__(self, name, points):
        self.set_name(name)
        self.set_points(points)

    def set_name(self, name):
        if len(name) == 0:
            raise InvalidStreetException("Street name cannot be empty")
        self.name = name

    def set_points(self, points):
        if len(points) < 2:
            raise InvalidStreetException("Street must have atleast 2 points")

        self.points = []
        for (x, y) in points:
            self.points.append(Vec(x, y))

        self.segments = []
        for i in range(len(self.points) - 1):
            a = self.points[i]
            b = self.points[i + 1]
            self.segments.append(Segment(a, b))

    def change_points(self, points):
        self.set_points(points)


"""
throws LookupError if street name is not found
"""


class StreetDatabase:
    def __init__(self):
        self.streets = {}

    def add_street(self, name, points):
        # street created with original name,
        # but indexed by lowercased street name
        s = Street(name, points)
        if name.lower() not in self.streets:
            self.streets[name.lower()] = s
        else:
            raise StreetLookupException("Street {} already exists".format(name))

    def get_street(self, name):
        if name.lower() not in self.streets:
            raise StreetLookupException("Street {} does not exist".format(name))
        return self.streets.get(name.lower())

    def change_street(self, name, points):
        street = self.get_street(name)
        street.change_points(points)

    def delete_street(self, name):
        street = self.get_street(name)
        del self.streets[name.lower()]

    def get_all_streets_except(self, except_street):
        return (s for (_, s) in self.streets.items() if s != except_street)

    def print_db(self):
        print "---"
        for _, street in self.streets.items():
            segments = street.segments

            print "{}: (".format(street.name)
            for seg in segments:
                print "  {!s}->{!s}".format(seg.u, seg.v)
            print ")"
        print "---"
        print ""
