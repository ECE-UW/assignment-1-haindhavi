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
            # check if they intersect at one point only
            if a == c and b != d:
                return a

            if a == d and b != c:
                return a

            if b == c and a != d:
                return b

            if b == d and a != c:
                return b

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
