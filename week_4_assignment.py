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
DEBUG_UP = True
DEBUG_PT = True

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
                if DEBUG_UP:
                    print self
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
        move = ""
        count = 0
        if DEBUG_SIT:
            print "target_row, target_col", target_row, target_col
            print "solved_tile_location", solved_tile_location
            print "zero_location", zero_location
        #need some checks here to determine if the position is already solved

        #case1: 0 tile is straight below location of tile being solved
        if solved_tile_location[1] == target_col and solved_tile_location[0] != target_row:
            count = 0
            while zero_location[0] > solved_tile_location[0]:
                move = "u"
                self.update_puzzle(move)
                solution_string += move
                count +=1
                zero_location = self.current_position(0, 0)
                if DEBUG_SIT:
                    print zero_location[0], solved_tile_location[0]
                    print self
            while count > 1:
                move = "lddru"
                self.update_puzzle(move)
                solution_string += move
                count -= 1
                if DEBUG_SIT:
                    print self
        #case2: 0 tile is directly to the right of the tile being solved
        elif solved_tile_location[0] == target_row and solved_tile_location[1] < zero_location[1]:
            if DEBUG_SIT:
                print "case2"
            count = 0
            while solved_tile_location[1] < target_col:
                move = "l"
                self.update_puzzle(move)
                solution_string += move
                count += 1
                zero_location = self.current_position(0, 0)
                solved_tile_location = self.current_position(target_row, target_col)
                if DEBUG_SIT:
                    print "case2: count += 1"
                    print "solved_tile_location[1]", solved_tile_location[1]
                    print "target_col", target_col
                    print self
            while count > 1:
                if DEBUG_SIT:
                    print "case2: count > 1"
                    print self
                move = "urrdl"
                self.update_puzzle(move)
                solution_string += move
                count -= 1

        #case 3: 0 tile is below and to the left of the tile being solved
        elif zero_location[0] > solved_tile_location[0] and zero_location[1] < solved_tile_location[1]:
            if DEBUG_SIT:
                print "case3"
            #first move should be up so we don't break invariance.
            while zero_location[0] > solved_tile_location[0]:
                move = "u"
                self.update_puzzle(move)
                solution_string += move
                zero_location = self.current_position(0, 0)
            #next move should be into horizontal position
            while zero_location[1] < solved_tile_location[1]:
                move = "r"
                self.update_puzzle(move)
                solution_string += move
                zero_location = self.current_position(0, 0)
            if DEBUG_SIT:
                print "moved 0 to target tile"
                print self

            #now lets move the tile into its correct position. Horizontally first
            one = ""
            two = ""
            three = ""
            four = ""
            while solved_tile_location[1] > target_col:
                #subcase - tile is on the top row
                if solved_tile_location[0] == 0:
                    one = "d"
                    three = "u"
                #subcase - tile not on the top row
                else:
                    one = "u"
                    three = "d"
                #move = "dllur"
                two = "l"
                four = "r"
                move = one + two + two + three + four
                self.update_puzzle(move)
                solution_string += move
                solved_tile_location = self.current_position(target_row, target_col)
            #then move 0 tile underneath it
            if DEBUG_SIT:
                print "moved target tile into horizontal position"
                print self
            move = "dl"
            self.update_puzzle(move)
            solution_string += move
            solved_tile_location = self.current_position(target_row, target_col)
            zero_location = self.current_position(0, 0)

            #finally for case 3, move the tile down. We go around to the left to avoid breaking invariance
            while solved_tile_location[0] < target_row:
                move = "ulddr"
                self.update_puzzle(move)
                solution_string += move
                solved_tile_location = self.current_position(target_row, target_col)

        #case 4: 0 tile is below and to the right of the tile being solved
        elif zero_location[0] > solved_tile_location[0] and zero_location[1] > solved_tile_location[1]:
            #first move should be up so we don't break invariance.
            if DEBUG_SIT:
                print "case4"
            while zero_location[0] > solved_tile_location[0]:
                move = "u"
                self.update_puzzle(move)
                solution_string += move
                zero_location = self.current_position(0, 0)
            #next move should be into horizontal position
            while zero_location[1] > solved_tile_location[1]:
                move = "l"
                self.update_puzzle(move)
                solution_string += move
                zero_location = self.current_position(0, 0)

            #now lets move the tile into its correct position. Horizontally first
            one = ""
            two = ""
            three = ""
            four = ""
            if solved_tile_location[0] == 0:
                one = "d"
                three = "u"
                #subcase - tile not on the top row
            else:
                one = "u"
                three = "d"
            two = "r"
            four = "l"
            move = one + two + two + three + four
            while solved_tile_location[1] < target_col:
                #subcase - tile is on the top row
                #move = "dllur"
                self.update_puzzle(move)
                solution_string += move
                solved_tile_location = self.current_position(target_row, target_col)
                if DEBUG_SIT:
                    print "moving target tile horizontally"
                    print "target_col", target_col
                    print "solved_tile_location[1]", solved_tile_location[1]
                    print self
            #then move 0 tile underneath it
            if DEBUG_SIT:
                print "moved target tile into horizontal position"
                print self
            move = "d" + two
            self.update_puzzle(move)
            solution_string += move
            solved_tile_location = self.current_position(target_row, target_col)
            zero_location = self.current_position(0, 0)

            #finally for case 4, move the tile down. We go around to the left to avoid breaking invariance
            while solved_tile_location[0] < target_row-1:
                move = "ulddr"
                self.update_puzzle(move)
                solution_string += move
                solved_tile_location = self.current_position(target_row, target_col)
                if DEBUG_SIT:
                    print "moving target tile down"
                    print self
            while solved_tile_location[0] == target_row-1:
                move = "u"
                self.update_puzzle(move)
                solution_string += move
                solved_tile_location = self.current_position(target_row, target_col)

        #post cases check really belongs in solve col_0 tile
        #check if tile one to the left of target is already in position
        if self.current_position(target_row, target_col-1) == (target_row, target_col-1):
            if DEBUG_SIT:
                print "post - case1"
            #tile one to the left is ok, move to top of next row
            zero_location = self.current_position(0, 0)
            if zero_location[0] == target_row:
                move = "u"
            else:
                move = ""
            zero_location = self.current_position(0, 0)
            distance_r = self.get_width() - zero_location[1]
            for dummy_idx in range(distance_r-1):
                move += "r"
            self.update_puzzle(move)
            solution_string += move

        else:
            zero_location = self.current_position(0, 0)
            if DEBUG_SIT:
                print "post - case 2"
            #otherwise move 0 to the space one to the left of where the solved tile is
            move = ""
            if zero_location[1] > 0:
                move = "l"
            self.update_puzzle(move)
            solution_string += move
            zero_location = self.current_position(0, 0)
            #if we're not on the bottom row or the solved row, move down
            if zero_location[0] < self.get_height()-1 and zero_location[0] < target_row:
                print "post - case 2.1"
                move = "d"
                self.update_puzzle(move)
                solution_string += move


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
            if DEBUG_SIT:
                print "post - case 3"
            move = "lddru"
            solution_string += move
            self.update_puzzle(move)
            solved_tile_location = self.current_position(target_row, target_col)
            if DEBUG_SIT:
                print self
        #assert self.lower_row_invariant(target_row, target_col)
        return solution_string

    def get_location(self, target_number):
        return self.current_position(target_number / self.get_width(), target_number % self.get_width())


    def position_tile(self, target_row, target_col, target_number):
        target_tile_location = self.get_location(target_number)
        zero_tile_location = self.get_location(0)
        move = ""
        move_string = ""
        one = ""
        two = ""
        three = ""
        four = ""

        #move zero into correct row
        if zero_tile_location[0] > target_tile_location[0]:
            one = "u"
        if zero_tile_location[0] < target_tile_location[0]:
            one = "d"
        #while zero_tile_location[0] != target_tile_location[0]:
        #move one away
        while abs(zero_tile_location[0]-target_tile_location[0]) > 1:
            move_string += one
            self.update_puzzle(one)
            zero_tile_location = self.get_location(0)
        #move zero into correct col
        if zero_tile_location[1] > target_tile_location[1]:
            one = "l"
        if zero_tile_location[1] < target_tile_location[1]:
            one = "r"
        #move one away horizontally
        while abs(zero_tile_location[1]-target_tile_location[1]) > 1:
        #move on top
        #while zero_tile_location[1] != target_tile_location[1]):
            move_string += one
            self.update_puzzle(one)
            zero_tile_location = self.get_location(0)


        #at this point 0 tile should be 1 space (8 directionally) away from target tile
        #begin moving target tile into horizontal position
        if target_tile_location[0] > target_row:
            #we need to move it down
            if DEBUG_PT:
                print "A"
            one = "d"
            three = "u"
        elif target_tile_location[0] < target_row:
            #we need to move it up
            if DEBUG_PT:
                print "B"
            one = "u"
            three = "d"
        else:
            #well, we need something for moving stuff around if it's on the same row or col
            #if we're at the bottom, don't go down first.
            if target_tile_location[0] == self.get_height()-1:
                if DEBUG_PT:
                    print "C"
                one = "u"
                three = "d"
            #if we're at the top, don't go up first.
            elif target_tile_location[0] == 0:
                if DEBUG_PT:
                    print "D"
                one = "d"
                three = "u"
            #catch all
            else:
                if DEBUG_PT:
                    print "E"
                one = "d"
                three = "u"

        if target_tile_location[1] > target_col:
            # we need ot move it left
            two = "r"
            four = "l"
        elif target_tile_location[1] < target_col:
            # we need to move it right
            two = "l"
            four = "r"
        else:
            #well, we need something for moving stuff around if it's on the same row or col
            two = "r"
            four = "l"
        #first horizontal move will only be four places
        if target_tile_location[1] != target_col:
            #slightly hacky way to stop the move going off the board
            zero_tile_location = self.get_location(0)
            if zero_tile_location[0] == self.get_height()-1:
                move = "u" + two + "d" + four
            elif zero_tile_location[0] == 0:
                move = "d" + two + "u" + four
            else:
                move = one + two + three + four
            move_string += move
            if DEBUG_PT:
                print move
            self.update_puzzle(move)
            target_tile_location = self.get_location(target_number)

        #now do additional horizontal moves
        while target_tile_location[1] != target_col:
            if zero_tile_location[0] == self.get_height()-1:
                move = four + "u" + two + "d" + four
            elif zero_tile_location[0] == 0:
                move = four + "d" + two + "u" + four
            else:
                move = four + one + two + three + four
            move_string += move
            if DEBUG_PT:
                print move
            self.update_puzzle(move)
            target_tile_location = self.get_location(target_number)

        #first vertical move will only be three places, 0 should currently be one vertical space above or below target tile
        if target_tile_location[0] != target_row:
            move = one + two + three
            move_string += move
            self.update_puzzle(move)
            if DEBUG_PT:
                print move
            target_tile_location = self.get_location(target_number)

        #now do additional vertical moves
        while target_tile_location[0] != target_row:
            move = three + four + one + two + three
            move_string += move
            self.update_puzzle(move)
            if DEBUG_PT:
                print move
            target_tile_location = self.get_location(target_number)

        #end
        return move_string


    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        solution_string = ""
        solved_tile_location = self.current_position(target_row, 0)
        zero_location = self.current_position(0, 0)
        move = ""
        count = 0
        if zero_location == (target_row+1, 0):
            move = "ur"
            self.update_puzzle(move)
            return move
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

bug_one = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print bug_one
#bug_one.solve_interior_tile(2, 2)
bug_two = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [7, 0, 8]])
#bug_two.solve_interior_tile(2, 1)

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
#question_8.solve_interior_tile(3, 1)
#print question_8

#poc_fifteen_gui.FifteenGUI(question_8)


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


errors
[-5.0 pts] For obj = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]]), obj.row0_invariant(0) expected True but received False
[-4.8 pts] For obj = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]]), obj.row1_invariant(1) expected True but received False
[-8.0 pts] For obj = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]]), obj.solve_2x2() returned incorrect move string ''
[-8.0 pts] For obj = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [0, 7, 8]]), obj.solve_col0_tile(2) returned incorrect move string ''
[-8.0 pts] For obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]]), obj.solve_interior_tile(2, 2) returned incorrect move string (Exception: AssertionError) "move off grid: d" at line 128, in update_puzzle
[-25.0 pts] For obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]]), obj.solve_puzzle() returned incorrect move string ''
[-8.0 pts] For obj = Puzzle(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]]), obj.solve_row0_tile(2) returned incorrect move string ''
[-8.0 pts] For obj = Puzzle(3, 3, [[2, 5, 4], [1, 3, 0], [6, 7, 8]]), obj.solve_row1_tile(2) returned incorrect move string ''
"""