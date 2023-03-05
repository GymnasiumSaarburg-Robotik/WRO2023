import math


class CCblock:
    def __init__(self, x_pos, y_pos, size, direction, x_center=None, y_center=None, width=None, height=None):
        self.x_pos = x_pos
        self.y_pos = y_pos

        if x_center is not None:
            self.x_center = x_center
        if y_center is not None:
            self.y_center = y_center

        if width is not None:
            self.width = width
        if height is not None:
            self.height = height

        if width is None:
            self.width = int(math.sqrt(size))
        if height is None:
            self.height = int(math.sqrt(size))

        if x_pos is None:
            self.x_center = x_center - self.width
        if y_pos is None:
            self.y_center = y_center - self.height

        self.size = size
        self.direction = direction

    def __str__(self) -> str:
        return "Block({}, {}, size: {}, direction: {})".format(self.x_pos, self.y_pos, self.size, self.direction)

    def __unicode__(self) -> str:
        return "Block({}, {}, size: {}, direction: {})".format(self.x_pos, self.y_pos, self.size, self.direction)

    def __repr__(self) -> str:
        return "Block({}, {}, size: {}, direction: {})".format(self.x_pos, self.y_pos, self.size, self.direction)
