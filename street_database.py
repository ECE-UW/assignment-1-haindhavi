from geometry import Vec, Segment


class Street:
    def __init__(self, name, points):
        self.set_name(name)
        self.set_points(points)

    def set_name(self, name):
        self.name = name

    def set_points(self, points):
        if len(points) < 2:
            raise NotImplementedError

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
        s = Street(name, points)
        if s.name not in self.streets:
            self.streets[s.name] = s

    def get_street(self, name):
        return self.streets.get(name)

    def get_all_streets(self):
        return self.streets

    def change_street(self, name, points):
        street = self.get_street(name)
        street.change_points(points)

    def delete_street(self, name):
        del self.streets[name]
        
    def get_all_streets_except(self, except_street):
        return (s for (_, s) in self.streets.items() if s != except_street)

    def print_db(self):
        print "---"
        for k in self.streets.keys():
            street = self.streets[k]
            segments = street.segments

            print "{}: (".format(k)
            for s in segments:
                print "  {!s}->{!s}".format(s.u, s.v)
            print ")"
        print "---"
        print ""
