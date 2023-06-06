import matplotlib as plt

class Vec:
    """A simple vector in 2D. Also used as a position vector for points"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scale):
        """Multiplication by a scalar"""
        return Vec(self.x * scale, self.y * scale)
        
    def dot(self, other):
        return self.x * other.x + self.y * other.y
        
    def lensq(self):
        return self.dot(self)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)
        
        
def signed_area(a, b, c):
    """Twice the area of the triangle abc.
       Positive if abc are in counter clockwise order.
       Zero if a, b, c are colinear.
       Otherwise negative.
    """
    p = b - a
    q = c - a
    return p.x * q.y - q.x * p.y

def is_on_segment(p, a, b):
    area = signed_area(a, b, p)
    if area == 0:
        if min(a.x, b.x) <= p.x <= max(a.x, b.x):
            if min(a.y, b.y) <= p.y <= max(a.y, b.y):
                return True
    return False


def is_ccw(a, b, c):
    """True iff triangle abc is counter-clockwise."""
    p = b - a
    q = c - a
    area = p.x * q.y - q.x * p.y
    # May want to throw an exception if area == 0
    return area > 0

def classify_points(line_start, line_end, points):
    left_count = 0
    right_count = 0
    line_direction = line_end - line_start
    for point in points:
        point_direction = point - line_start
        if is_ccw(Vec(0,0), line_direction, point_direction):
            left_count += 1
        else:
            right_count += 1
    return (right_count, left_count)

def intersecting(a,b,c,d):
    orientations1 = is_ccw(a,b,c) != is_ccw(a,b,d)
    orientations2 = is_ccw(c,d,a) != is_ccw(c,d,b)
    if orientations1 is True and orientations2 is True:
        return True
    return False

def is_strictly_convex(vertices):
    n = len(vertices)
    if n < 3:
        return False
    for i in range(n):
        a = vertices[i]
        b = vertices[(i + 1) % n]
        c = vertices[(i + 2) % n]
        if not is_ccw(a, b, c):
            return False
    return True

def gift_wrap(points):
    """ Returns points on convex hull in CCW using the Gift Wrap algorithm"""
    # Get the bottom-most point (and left-most if necessary).
    assert len(points) >= 3
    bottommost = min(points, key=lambda p: (p.y, p.x))
    hull = [bottommost]
    done = False
    
    # Loop, adding one vertex at a time, until hull is (about to be) closed.
    while not done:
        candidate = None
        # Loop through all points, looking for the one that is "rightmost"
        # looking from last point on hull
        for p in points:
            if p is hull[-1]:
                continue
            if candidate is None or is_ccw(candidate, hull[-1], p):
                candidate = p
        if candidate is bottommost:
            done = True    # We've closed the hull
        else:
            hull.append(candidate)

    return hull


class PointSortKey:
    """A class for use as a key when sorting points wrt bottommost point"""
    def __init__(self, p, bottommost):
        """Construct an instance of the sort key"""
        self.direction = p - bottommost
        self.is_bottommost = self.direction.lensq() == 0  # True if p == bottommost
        
    def __lt__(self, other):
        """Compares two sort keys. p1 < p2 means the vector the from bottommost point
           to p2 is to the left of the vector from the bottommost to p1.
        """
        if self.is_bottommost:
            return True   # Ensure bottommost point is less than all other points
        elif other.is_bottommost:
            return False  # Ensure no other point is less than the bottommost
        else:
            area = self.direction.x * other.direction.y - other.direction.x * self.direction.y
            return area > 0

def simple_polygon(points):
    assert len(points) >= 3
    bottommost  = min(points, key=lambda p: (p.y, p.x))
    sorted_points = sorted(points, key=lambda p: PointSortKey(p, bottommost))
    hull = []
    for p in sorted_points:
        hull.append(p)
    return hull

def graham_scan(points):
    n = len(points)
    simple = simple_polygon(points)
    stack_h = [simple[0], simple[1], simple[2]]
    for i in range(3, n):
        while not is_ccw(stack_h[-2], stack_h[-1], simple[i]):
            stack_h.pop()
        stack_h.append(simple[i])
    return stack_h

