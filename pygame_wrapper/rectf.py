class RectF:
    __slots__ = ('_x', '_y', '_w', '_h')

    def __init__(self, *args):
        # Supports: RectF(x, y, w, h), RectF((x, y), (w, h)),
        # or RectF(other) where other has x, y, width, height.
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, RectF):
                self._x, self._y = arg.x, arg.y
                self._w, self._h = arg.width, arg.height
            elif hasattr(arg, 'x') and hasattr(arg, 'y') and hasattr(arg, 'width') and hasattr(arg, 'height'):
                self._x = float(arg.x)
                self._y = float(arg.y)
                self._w = float(arg.width)
                self._h = float(arg.height)
            elif isinstance(arg, (list, tuple)):
                if len(arg) == 4:
                    self._x, self._y, self._w, self._h = map(float, arg)
                elif len(arg) == 2:
                    pos, size = arg
                    if (isinstance(pos, (list, tuple)) and len(pos) == 2 and
                            isinstance(size, (list, tuple)) and len(size) == 2):
                        self._x, self._y = map(float, pos)
                        self._w, self._h = map(float, size)
                    else:
                        raise ValueError("Invalid tuple format for RectF")
                else:
                    raise ValueError("Invalid tuple length for RectF")
            else:
                raise ValueError("Invalid argument for RectF")
        elif len(args) == 2:
            pos, size = args
            if (isinstance(pos, (list, tuple)) and len(pos) == 2 and
                    isinstance(size, (list, tuple)) and len(size) == 2):
                self._x, self._y = map(float, pos)
                self._w, self._h = map(float, size)
            else:
                raise ValueError("Invalid arguments for RectF")
        elif len(args) == 4:
            self._x, self._y, self._w, self._h = map(float, args)
        else:
            raise ValueError("RectF() takes 1, 2, or 4 arguments")

    def __repr__(self):
        return f"RectF({self._x}, {self._y}, {self._w}, {self._h})"

    def __iter__(self):
        return iter((self._x, self._y, self._w, self._h))

    def __eq__(self, other):
        try:
            return (float(self.x) == float(other.x) and
                    float(self.y) == float(other.y) and
                    float(self.width) == float(other.width) and
                    float(self.height) == float(other.height))
        except AttributeError:
            return False

    # --- Core attributes ---
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = float(value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = float(value)

    @property
    def width(self):
        return self._w

    @width.setter
    def width(self, value):
        self._w = float(value)

    @property
    def height(self):
        return self._h

    @height.setter
    def height(self, value):
        self._h = float(value)

    # --- Derived properties ---
    @property
    def left(self):
        return self.x

    @left.setter
    def left(self, value):
        self.x = float(value)

    @property
    def right(self):
        return self.x + self.width

    @right.setter
    def right(self, value):
        self.x = float(value) - self.width

    @property
    def top(self):
        return self.y

    @top.setter
    def top(self, value):
        self.y = float(value)

    @property
    def bottom(self):
        return self.y + self.height

    @bottom.setter
    def bottom(self, value):
        self.y = float(value) - self.height

    @property
    def center(self):
        return (self.x + self.width / 2, self.y + self.height / 2)

    @center.setter
    def center(self, value):
        cx, cy = value
        self.x = float(cx) - self.width / 2
        self.y = float(cy) - self.height / 2

    @property
    def centerx(self):
        return self.x + self.width / 2

    @centerx.setter
    def centerx(self, value):
        self.x = float(value) - self.width / 2

    @property
    def centery(self):
        return self.y + self.height / 2

    @centery.setter
    def centery(self, value):
        self.y = float(value) - self.height / 2

    @property
    def size(self):
        return (self.width, self.height)

    @size.setter
    def size(self, value):
        if isinstance(value, (list, tuple)) and len(value) == 2:
            self.width, self.height = map(float, value)
        else:
            raise ValueError("size must be a 2-tuple")

    @property
    def area(self):
        return self.width * self.height

    @property
    def topleft(self):
        return (self.x, self.y)

    @topleft.setter
    def topleft(self, value):
        self.x, self.y = map(float, value)

    @property
    def bottomleft(self):
        return (self.x, self.y + self.height)

    @bottomleft.setter
    def bottomleft(self, value):
        vx, vy = map(float, value)
        self.x = vx
        self.y = vy - self.height

    @property
    def topright(self):
        return (self.x + self.width, self.y)

    @topright.setter
    def topright(self, value):
        vx, vy = map(float, value)
        self.x = vx - self.width
        self.y = vy

    @property
    def bottomright(self):
        return (self.x + self.width, self.y + self.height)

    @bottomright.setter
    def bottomright(self, value):
        vx, vy = map(float, value)
        self.x = vx - self.width
        self.y = vy - self.height

    @property
    def midtop(self):
        return (self.centerx, self.top)

    @midtop.setter
    def midtop(self, value):
        cx, ty = map(float, value)
        self.centerx = cx
        self.top = ty

    @property
    def midleft(self):
        return (self.left, self.centery)

    @midleft.setter
    def midleft(self, value):
        lx, cy = map(float, value)
        self.left = lx
        self.centery = cy

    @property
    def midbottom(self):
        return (self.centerx, self.bottom)

    @midbottom.setter
    def midbottom(self, value):
        cx, by = map(float, value)
        self.centerx = cx
        self.bottom = by

    @property
    def midright(self):
        return (self.right, self.centery)

    @midright.setter
    def midright(self, value):
        rx, cy = map(float, value)
        self.right = rx
        self.centery = cy

    # --- Methods ---
    def copy(self):
        return RectF(self.x, self.y, self.width, self.height)

    def move(self, dx, dy):
        return RectF(self.x + dx, self.y + dy, self.width, self.height)

    def move_ip(self, dx, dy):
        self.x += dx
        self.y += dy
        return self

    def move_to(self, x, y):
        return RectF(x, y, self.width, self.height)

    def move_to_ip(self, x, y):
        self.x = x
        self.y = y
        return self

    def inflate(self, dw, dh):
        new_w = self.width + dw
        new_h = self.height + dh
        new_x = self.x - dw / 2
        new_y = self.y - dh / 2
        return RectF(new_x, new_y, new_w, new_h)

    def inflate_ip(self, dw, dh):
        self.x -= dw / 2
        self.y -= dh / 2
        self.width += dw
        self.height += dh
        return self

    def clamp(self, other):
        # other must be rect-like (with x, y, width, height)
        r = self.copy()
        ox, oy, ow, oh = float(other.x), float(
            other.y), float(other.width), float(other.height)
        # Horizontal clamp
        if r.width <= ow:
            if r.x < ox:
                r.x = ox
            elif r.right > ox + ow:
                r.x = ox + ow - r.width
        else:
            r.x = ox
        # Vertical clamp
        if r.height <= oh:
            if r.y < oy:
                r.y = oy
            elif r.bottom > oy + oh:
                r.y = oy + oh - r.height
        else:
            r.y = oy
        return r

    def clamp_ip(self, other):
        clamped = self.clamp(other)
        self.x, self.y = clamped.x, clamped.y
        return self

    def union(self, other):
        ox, oy, ow, oh = float(other.x), float(
            other.y), float(other.width), float(other.height)
        new_left = min(self.left, ox)
        new_top = min(self.top, oy)
        new_right = max(self.right, ox + ow)
        new_bottom = max(self.bottom, oy + oh)
        return RectF(new_left, new_top, new_right - new_left, new_bottom - new_top)

    def union_ip(self, other):
        u = self.union(other)
        self.x, self.y, self.width, self.height = u.x, u.y, u.width, u.height
        return self

    def unionall(self, rects):
        u = self.copy()
        for r in rects:
            u = u.union(r)
        return u

    def clip(self, other):
        ox, oy, ow, oh = float(other.x), float(
            other.y), float(other.width), float(other.height)
        new_left = max(self.left, ox)
        new_top = max(self.top, oy)
        new_right = min(self.right, ox + ow)
        new_bottom = min(self.bottom, oy + oh)
        if new_right < new_left or new_bottom < new_top:
            return RectF(new_left, new_top, 0, 0)
        return RectF(new_left, new_top, new_right - new_left, new_bottom - new_top)

    def contains(self, other):
        # Returns True if self completely contains other rect.
        try:
            return (self.left <= other.left and self.right >= other.right and
                    self.top <= other.top and self.bottom >= other.bottom)
        except AttributeError:
            raise ValueError(
                "Argument must have x, y, width, and height attributes")

    def colliderect(self, other):
        try:
            return (self.left < other.right and self.right > other.left and
                    self.top < other.bottom and self.bottom > other.top)
        except AttributeError:
            raise ValueError(
                "Argument must have x, y, width, and height attributes")

    def colliderect_point(self, other: 'RectF'):
        """
        Returns the collision point as the center of the intersection rectangle.
        If there's no collision, returns None.
        """
        if not self.colliderect(other):
            return None

        # Compute intersection boundaries.
        inter_left = max(self.left, other.left)
        inter_right = min(self.right, other.right)
        inter_top = max(self.top, other.top)
        inter_bottom = min(self.bottom, other.bottom)

        # Compute the center of the intersection rectangle.
        center_x = (inter_left + inter_right) / 2
        center_y = (inter_top + inter_bottom) / 2

        return (center_x, center_y)

    def collidepoint(self, x, y=None):
        if y is None:
            try:
                x, y = x
            except (TypeError, ValueError):
                raise ValueError("collidepoint() requires a point (x, y)")
        return (self.left <= x < self.right and self.top <= y < self.bottom)

    def collidelist(self, rect_list):
        for index, rect in enumerate(rect_list):
            if self.colliderect(rect):
                return index
        return -1

    def collidelistall(self, rect_list):
        return [index for index, rect in enumerate(rect_list) if self.colliderect(rect)]

    def collidedict(self, rect_dict):
        for key, rect in rect_dict.items():
            if self.colliderect(rect):
                return key
        return None

    def collidedictall(self, rect_dict):
        return [key for key, rect in rect_dict.items() if self.colliderect(rect)]

    def clipline(self, *args):
        # Supports:
        # clipline(x1, y1, x2, y2)
        # clipline(((x1, y1), (x2, y2)))
        # clipline((x1, y1), (x2, y2))
        if len(args) == 1:
            pts = args[0]
            if (isinstance(pts, (list, tuple)) and len(pts) == 2):
                (x1, y1), (x2, y2) = pts
            else:
                raise ValueError("Invalid argument for clipline")
        elif len(args) == 2:
            (x1, y1), (x2, y2) = args
        elif len(args) == 4:
            x1, y1, x2, y2 = args
        else:
            raise ValueError("clipline() accepts 1, 2, or 4 arguments")

        # Liang-Barsky clipping algorithm
        xmin, ymin = self.left, self.top
        xmax, ymax = self.right, self.bottom
        dx = x2 - x1
        dy = y2 - y1
        p = [-dx, dx, -dy, dy]
        q = [x1 - xmin, xmax - x1, y1 - ymin, ymax - y1]

        u1, u2 = 0.0, 1.0
        for pi, qi in zip(p, q):
            if pi == 0:
                if qi < 0:
                    return ()  # Line is parallel and outside.
            else:
                # Note: using -qi/pi to match the typical formulation.
                t = -qi / pi
                if pi < 0:
                    if t > u2:
                        return ()
                    if t > u1:
                        u1 = t
                else:
                    if t < u1:
                        return ()
                    if t < u2:
                        u2 = t
        if u2 < u1:
            return ()
        cx1, cy1 = x1 + u1 * dx, y1 + u1 * dy
        cx2, cy2 = x1 + u2 * dx, y1 + u2 * dy
        return (cx1, cy1, cx2, cy2)

    def update(self, *args):
        # Accepts: update(x, y, w, h) or update((x, y, w, h)) or update(rect)
        if len(args) == 1:
            arg = args[0]
            if hasattr(arg, 'x') and hasattr(arg, 'y') and hasattr(arg, 'width') and hasattr(arg, 'height'):
                self.x, self.y = float(arg.x), float(arg.y)
                self.width, self.height = float(arg.width), float(arg.height)
            elif isinstance(arg, (list, tuple)):
                if len(arg) == 4:
                    self.x, self.y, self.width, self.height = map(float, arg)
                else:
                    raise ValueError(
                        "update() with a sequence requires 4 values")
            else:
                raise ValueError("Invalid argument for update()")
        elif len(args) == 4:
            self.x, self.y, self.width, self.height = map(float, args)
        else:
            raise ValueError("update() requires 1 or 4 arguments")

    def normalize(self):
        if self.width < 0:
            self.x += self.width
            self.width = -self.width
        if self.height < 0:
            self.y += self.height
            self.height = -self.height
        return self

    # --- Conversion methods ---
    def to_pygame(self):
        import pygame
        return pygame.Rect(round(self.x), round(self.y), round(self.width), round(self.height))

    @classmethod
    def from_pygame(cls, pg_rect):
        return cls(pg_rect.x, pg_rect.y, pg_rect.width, pg_rect.height)
