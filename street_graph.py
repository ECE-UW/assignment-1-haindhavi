from operator import attrgetter


class StreetGraph:
    def __init__(self, db):
        self.vertices = dict()
        self.edges = set()
        self.VERTEX_ID = 1

        for key, street in db.streets.items():
            for seg in street.segments:
                other_streets = db.get_all_streets_except(street)
                curr_vertices = find_all_vertices_on_segment(seg, other_streets)

                for v in curr_vertices:
                    if v not in self.vertices:
                        self.vertices[v] = {"name": self.VERTEX_ID}
                        self.VERTEX_ID += 1

                for i in range(len(curr_vertices) - 1):
                    self.edges.add((curr_vertices[i], curr_vertices[i + 1]))

    def print_graph(self):
        print "V = {"
        for v, data in self.vertices.items():
            name = data["name"]
            print "  {}:\t{!s}".format(name, v)
        print "}"

        print "E = {"
        lines = []
        for (u, v) in self.edges:
            lines.append(
                "  <{},{}>".format(self.vertices[u]["name"], self.vertices[v]["name"])
            )
        if lines:
            print ",\n".join(lines)
        print "}"


"""
returns a list of vertices that lie on a line segment after all intersections 
with all line segments of the given streets have been computed
"""


def find_all_vertices_on_segment(seg, streets):
    vertices = set()
    for street in streets:
        for other_seg in street.segments:
            intersection = seg.intersect(other_seg)
            if intersection is not None:
                vertices.add(intersection)

    if len(vertices) != 0:
        # since there is atleast one intersection, both endpoints of this
        # line segment (seg) are also vertices
        # else, there are no intersections, and no vertices can lie on
        # this line segment
        endpoints = {seg.u, seg.v}
        vertices = vertices.union(endpoints)
        vertices = sorted(vertices, key=attrgetter("x", "y"))

    return vertices
