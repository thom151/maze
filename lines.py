

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, color):
        x1 = self.p1.x
        y1 = self.p1.y

        x2 = self.p2.x
        y2 = self.p2.y
        canvas.create_line(x1, y1, x2, y2, fill=color, width=2)


class Cell:
    def __init__(self, window=None):
        self.visited = False
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = window

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        left_line = Line(Point(x1, y1), Point(x1, y2))
        right_line = Line(Point(x2, y1), Point(x2, y2))
        top_line = Line(Point(x1, y1), Point(x2, y1))
        bottom_line = Line(Point(x1, y2), Point(x2, y2))

        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            self._win.draw_line(left_line)
        else:
            self._win.draw_line(left_line,  "#d9d9d9")
        if self.has_right_wall:
            self._win.draw_line(right_line)
        else:
            self._win.draw_line(right_line,  "#d9d9d9")
        if self.has_top_wall:
            self._win.draw_line(top_line)
        else:
            self._win.draw_line(top_line, "#d9d9d9")
        if self.has_bottom_wall:
            self._win.draw_line(bottom_line)
        else:
            self._win.draw_line(bottom_line, "#d9d9d9")

    def draw_move(self, to_cell, undo=False):
        x_mid = (self._x2 + self._x1)/2
        y_mid = (self._y2 + self._y1)/2

        to_cell_x_mid = (to_cell._x2 + to_cell._x1)/2
        to_cell_y_mid = (to_cell._y2 + to_cell._y1)/2

        connecting_line = Line(Point(x_mid, y_mid),
                               Point(to_cell_x_mid, to_cell_y_mid))
        if undo:
            self._win.draw_line(connecting_line, "gray")
        else:
            self._win.draw_line(connecting_line, "red")
