from lines import Cell
import time
import random


class Maze:
    def __init__(self,
                 x1,
                 y1,
                 num_rows,
                 num_cols,
                 cell_size_x,
                 cell_size_y,
                 win=None,
                 seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []

        self._create_cells()
        self._break_entrance_and_exit()
        if seed is None:
            random.seed(seed)
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self.num_rows):
            rows = []
            for j in range(self.num_cols):
                rows.append(Cell(self.win))
            self._cells.append(rows)

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self.win is None:
            return
        curr_x1 = self.x1 + (j * self.cell_size_x)
        curr_y1 = self.y1 + (i * self.cell_size_y)
        curr_x2 = curr_x1 + self.cell_size_x
        curr_y2 = curr_y1 + self.cell_size_y
        self._cells[i][j].draw(curr_x1,
                               curr_y1,
                               curr_x2,
                               curr_y2)
        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self.num_rows-1][self.num_cols-1].has_bottom_wall = False
        self._draw_cell(0, 0)
        self._draw_cell(self.num_rows-1, self.num_cols-1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            index_list = []
            if i != 0:
                top_adjacent = self._cells[i-1][j]
                if not top_adjacent.visited:
                    index_list.append((i-1, j))
            if i != self.num_rows-1:
                bottom_adjacent = self._cells[i+1][j]
                if not bottom_adjacent.visited:
                    index_list.append((i+1, j))
            if j != 0:
                left_adjacent = self._cells[i][j-1]
                if not left_adjacent.visited:
                    index_list.append((i, j-1))
            if j != self.num_cols-1:
                right_adjacent = self._cells[i][j+1]
                if not right_adjacent.visited:
                    index_list.append((i, j+1))
            if len(index_list) == 0:
                self._draw_cell(i, j)
                return
            else:
                rand_dir = random.choice(index_list)
                adj_i = rand_dir[0]
                adj_j = rand_dir[1]
                if adj_i < i:
                    self._cells[i][j].has_top_wall = False
                if adj_i > i:
                    self._cells[i][j].has_bottom_wall = False
                if adj_j < j:
                    self._cells[i][j].has_left_wall = False
                if adj_j > j:
                    self._cells[i][j].has_right_wall = False
                self._break_walls_r(adj_i, adj_j)

    def _reset_cells_visited(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._cells[i][j].visited = False

    def solve(self):
        if self._solve_r(0, 0):
            return True
        return False

    def _solve_r(self, i, j):
        print(i, j)
        self._animate()
        curr = self._cells[i][j]
        curr.visited = True

        if curr == self._cells[self.num_rows-1][self.num_cols-1]:
            return True
        top = (i-1, j)
        bottom = (i+1, j)
        right = (i, j+1)
        left = (i, j-1)
        frontier = []

        if not curr.has_top_wall and not self._cells[top[0]][top[1]].visited:
            frontier.append(top)
        if not curr.has_bottom_wall and not self._cells[bottom[0]][bottom[1]].visited:
            frontier.append(bottom)
        if not curr.has_left_wall and not self._cells[left[0]][left[1]].visited:
            frontier.append(left)
        if not curr.has_right_wall and not self._cells[right[0]][right[1]].visited:
            frontier.append(right)

        if j == 0:
            print(frontier)

        for cell in frontier:
            if cell[0] == -1 and cell[1] == 0:
                continue
            curr.draw_move(self._cells[cell[0]][cell[1]])
            if self._solve_r(cell[0], cell[1]):
                return True
            curr.draw_move(self._cells[cell[0]][cell[1]], True)
        return False
