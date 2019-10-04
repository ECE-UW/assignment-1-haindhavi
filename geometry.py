TOL = 1e-5


def isclose(a, b):
    return abs(a - b) <= TOL


def inrange(a, x, b):
    return a - TOL <= x <= b + TOL


class Vec:
    def __init__(u, x, y):
        u.x = 1.0 * x
        u.y = 1.0 * y

    def plus(u, v):
        return Vec(u.x + v.x, u.y + v.y)

    def minus(u, v):
        return Vec(u.x - v.x, u.y - v.y)

    def mult(u, t):
        return Vec(u.x * t, u.y * t)

    def cross(u, v):
        return 1.0 * (u.x * v.y - u.y * v.x)

    def dot(u, v):
        return 1.0 * (u.x * v.x + u.y * v.y)

    def __hash__(u):
        return hash("{:.2f} {:.2f}".format(u.x, u.y))

    def __eq__(u, v):
        return isclose(u.x, v.x) and isclose(u.y, v.y)

    def __ne__(u, v):
        return not u.__eq__(v)

    def __str__(u):
        return "({:.2f},{:.2f})".format(u.x, u.y)


"""
Finds if 2 line segments intersect at _exactly_ one point

a, b, c, d are all of class Vec

approach taken from: https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect

represent line segment b/w `a` and `b` as
  p to p + r (where p, r are vectors)

represent line segment b/w `c` and `d` as
  q to q + s

any point on the first segment is represented as p + tr, t is a scalar in [0,1]
any point on the second segment is represented as q + us, u is a scalar in [0,1]

for both line segments to intersect, for some value of t and u
  p + tr = q + us

"""


def findIntersection(a, b, c, d):
    p, r = a, b.minus(a)
    q, s = c, d.minus(c)

    if isclose(r.cross(s), 0.0):
        # lines are collinear
        if isclose(q.minus(p).cross(r), 0.0):
            AB = Segment(a, b)

            c_in_AB = AB.contains(c)
            d_in_AB = AB.contains(d)

            if c_in_AB and not d_in_AB:
                return c

            if d_in_AB and not c_in_AB:
                return d

            return None

        # lines are parallel but don't intersect
        return None

    t = q.minus(p).cross(s) / r.cross(s)
    u = q.minus(p).cross(r) / r.cross(s)

    if inrange(0.0, t, 1.0) and inrange(0.0, u, 1.0):
        intersection = p.plus(r.mult(t))
        return intersection

    return None


"""
stores a line segment between 2 points (vectors) u and v
  u --> v
"""


class Segment:
    def __init__(self, u, v):
        self.u = u
        self.v = v

    def intersect(self, other):
        return findIntersection(self.u, self.v, other.u, other.v)

    def contains(self, w):
        u, v = self.u, self.v
        vu = v.minus(u)
        wu = w.minus(u)

        return isclose(vu.cross(wu), 0) and (
            -TOL <= vu.dot(wu) <= ((u.x - v.x) ** 2 + (u.y - v.y) ** 2)
        )
