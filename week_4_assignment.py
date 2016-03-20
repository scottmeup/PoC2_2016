"""
Created on Sat Mar 19 04:34:37 2016

@author: andrewscott
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""
try:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui 
except ImportError: 
    import simplegui

DEBUG_LRI = True
DEBUG_SIT = True

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        width = self.get_width()
        height = self.get_height()
        #first_line = [self.get_number(target_row, dummy_x) for dummy_x in range(target_col+1, width)]
        #remaining_lines = [[self.get_number(dummy_y, dummy_x) for dummy_x in range(0, width)] for dummy_y in range(target_row, height)]
        #invariant_data = first_line
        #for line in remaining_lines:
            #invariant_data += line
        #if DEBUG_LRI:
            #print "first", first_line
            #print "remaining", remaining_lines
            #print "invariant_data", invariant_data
        #eval current line
        if self.get_number(target_row, target_col) == 0:
            pass
        else:
            return False
        for dummy_x in range(target_col+1, width):
            if self.current_position(target_row, dummy_x) == (target_row, dummy_x):
                if DEBUG_LRI:
                    #print "The juicy fruit will hold the wire in place"
                    print "Solved row N:", (target_row, dummy_x), self.get_number(target_row, dummy_x)
            else:
                if DEBUG_LRI:
                    print "Incorrect row N:", (target_row, dummy_x), self.get_number(target_row, dummy_x)
                return False
        for dummy_y in range(target_row+1, height):
            for dummy_x in range(0, width):
                if self.current_position(dummy_y, dummy_x) == (dummy_y, dummy_x):
                    if DEBUG_LRI:
                        #print "The juicy fruit will hold the wire in place"
                        print "Solved row N+1:", (dummy_y, dummy_x), self.get_number(dummy_y, dummy_x)
                else:
                    if DEBUG_LRI:
                        print "Incorrect row N+1:", (dummy_y, dummy_x), self.get_number(dummy_y, dummy_x)
                    return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        #assert self.lower_row_invariant(target_row, target_col)
        #do some solve
        solution_string = ""
        solved_tile_location = self.current_position(target_row, target_col)
        zero_location = self.current_position(0, 0)
        if DEBUG_SIT:
            print "target_row, target_col", target_row, target_col
            print "solved_tile_location", solved_tile_location
            print "zero_location", zero_location
        #case: straight below
        if solved_tile_location[1] == target_col:
            count = 0
            while zero_location[0] < solved_tile_location[0]:
                move = "u"
                self.update_puzzle(move)
                solution_string += move
                count +=1
            while count > 0:
                move = "lddru"
                self.update_puzzle(move)
                solution_string += move
                count -= 1
        """
        #move 0 to target tile position
        if solved_tile_location[0] < target_row:
            while solved_tile_location[1] > zero_location[1]:
                move = "l"
                self.update_puzzle(move)
                solution_string += move
                zero_location = self.current_position(0, 0)
            while solved_tile_location[1] < zero_location[1]:
                #can't move straight right... will break assertion                
                move = "ur"
                self.update_puzzle(move)
                solution_string += move
                zero_location = self.current_position(0, 0)
            while solved_tile_location[0] < zero_location[0]:
                move = "u"
                self.update_puzzle(move)
                solution_string += move
                zero_location = self.current_position(0, 0)
        """
        if DEBUG_SIT:
            print solution_string
            print self
        #cycle target tile down to proper position
        solved_tile_location = self.current_position(target_row, target_col)
        while solved_tile_location != (target_row, target_col):
            move = "lddru"
            solution_string += move
            self.update_puzzle(move)
            solved_tile_location = self.current_position(target_row, target_col)
            if DEBUG_SIT:
                print self
        #assert self.lower_row_invariant(target_row, target_col)
        return solution_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        #get rid of this, it's just for testing
        coordinate_0 = (-1, -1)
        for dummy_x in range(0, self.get_width()):
            for dummy_y in range(0, self.get_height()):
                if self.get_number(dummy_y, dummy_x) == 0:
                    coordinate_0 = (dummy_y, dummy_x)
        self.lower_row_invariant(coordinate_0[0], coordinate_0[1])
        return ""


# Start interactive simulation (default layout)
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
#poc_fifteen_gui.FifteenGUI(Puzzle(2, 2))
#p = Puzzle(4, 4)

question_8 = Puzzle(4, 4)
question_8_input_i = [4, 13, 1, 3, 5, 10, 2, 7, 8, 12, 6, 11, 9, 0, 14, 15]
question_8_input_ii = [4, 0, 1, 3, 5, 13, 2, 7, 8, 10, 6, 11, 9, 12, 14, 15]
question_8_input_iii = [5, 4, 1, 3, 8, 0, 2, 7, 10, 13, 6, 11, 9, 12, 14, 15]
x = 0
for i in range(len(question_8._grid)):
    for j in range(len(question_8._grid[0])):
        question_8.set_number(i, j, question_8_input_i[x])
        x += 1
print question_8

poc_fifteen_gui.FifteenGUI(question_8)


"""
def homework():
    #question 2 answer ddrdrudlulurrrlldluurrrdllldrurrulllddruld (urrulllddruld)
    #q2 options:
    front = "ddrdrudlulurrrlldluurrrdllldr"
    end = []
    end.append("ruldrulld")
    end.append("urrulllddruld")
    end.append("ruldrul")
    end.append("urullddruld")
    for item in end:
        print front + item


    #question 5 answer: "rdlurdlu", "drul"
    #question 8 answer: "lddru"
    #question 9 answer: "ruldrdlurdluurddlur"
    #question 10 answer: "urdlurrdluldrruld"
    
    
    p = Puzzle(4, 4)
    for i in range(len(p._grid)):
        for j in range(len(p._grid[0])):
            print "(y:", i, ", x:", j, ")"
            print p.get_number(i, j)

    #question 1
    #poc_fifteen_gui.FifteenGUI(p)


    question_4 = Puzzle(2, 2)
    question_4_input = [0, 2, 3, 1]
    x = 0
    for i in range(len(question_4._grid)):
        for j in range(len(question_4._grid[0])):
            question_4.set_number(i, j, question_4_input[x])
            x += 1
    #poc_fifteen_gui.FifteenGUI(question_4)

    question_5 = Puzzle(2, 2)
    question_5_input = [0, 3, 1, 2]
    x = 0
    for i in range(len(question_5._grid)):
        for j in range(len(question_5._grid[0])):
            question_5.set_number(i, j, question_5_input[x])
            x += 1
    #poc_fifteen_gui.FifteenGUI(question_5)

    question_8 = Puzzle(4, 4)
    question_8_input = [5, 4, 1, 3, 8, 0, 2, 7, 10, 13, 6, 11, 9, 12, 14, 15]
    x = 0
    for i in range(len(question_8._grid)):
        for j in range(len(question_8._grid[0])):
            question_8.set_number(i, j, question_8_input[x])
            x += 1
    #poc_fifteen_gui.FifteenGUI(question_8)

    x = 0
    question_9 = Puzzle(3, 2)
    question_9_input = [1, 2, 0, 4, 3, 5]
    for i in range(len(question_9._grid)):
        for j in range(len(question_9._grid[0])):
            question_9.set_number(i, j, question_9_input[x])
            x += 1
    #poc_fifteen_gui.FifteenGUI(question_9)

    x = 0
    question_10 = Puzzle(2, 3)
    question_10_input = [3, 4, 1, 0, 2, 5]
    for i in range(len(question_10._grid)):
        for j in range(len(question_10._grid[0])):
            question_10.set_number(i, j, question_10_input[x])
            x += 1
    #poc_fifteen_gui.FifteenGUI(question_10)
"""
