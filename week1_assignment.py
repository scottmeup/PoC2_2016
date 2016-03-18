"""

@author: andrewscott
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

try:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
except ImportError:
    import simplegui

try:
    import codeskulptor
    codeskulptor.set_timeout(20)
except ImportError as exp:
#except Error as exp:
    print "Codeskulptor not found"
    print exp
    #print exp

# debug vars
DEBUG_CDF = False
DEBUG_MZ = False
DEBUG_MH = False
DEBUG_ME = True
DEBUG_VM = True
DEBUG_GD = True
DEBUG_BM = True

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        #self._cells[row][col] = ZOMBIE
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        index = 0
        len_zombie_list = len(self._zombie_list)
        while index < len_zombie_list:
            yield self._zombie_list[index]
            index += 1
        return

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        index = 0
        len_human_list = len(self._human_list)
        while index < len_human_list:
            yield self._human_list[index]
            index += 1
        return
              
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        grid_width = poc_grid.Grid.get_grid_width(self)
        grid_height = poc_grid.Grid.get_grid_height(self)
        self._visited = poc_grid.Grid(grid_height, grid_width)
        self._distance_field = [[grid_width*grid_height for dummy_col in range(0, grid_width)] for dummy_row in range(0, grid_height)]
        self._boundary_list = poc_queue.Queue()        
        if entity_type == ZOMBIE:
            for entity in self._zombie_list:
                self._boundary_list.enqueue(entity)    
        elif entity_type == HUMAN:
            for entity in self._human_list:
                self._boundary_list.enqueue(entity)    
        else:
            print "Invalid Entity"
            return
        
            
        #set all initial distance to 0
        for boundary in self._boundary_list:
            self._distance_field[boundary[0]][boundary[1]] = 0           
        
        #each step outward of unoccupied space gets +1 distance to their 
        #corresponding field position
        while len(self._boundary_list)>0:
            #if DEBUG_CDF:
            #    print "len(self._boundary_list)", len(self._boundary_list)
            boundary = self._boundary_list.dequeue()
            if boundary == None:
                return self._distance_field
            self._visited.set_full(boundary[0], boundary[1])
            #self._distance_field[boundary[0], boundary[1]] = distance
            neighbors = self.four_neighbors(boundary[0], boundary[1])
            for neighbor in neighbors:
                #check if iterated over tile this calculation
                if self._visited.is_empty(neighbor[0], neighbor[1]) and self.is_empty(neighbor[0], neighbor[1]):
                    self._distance_field[neighbor[0]][neighbor[1]] =  self._distance_field[boundary[0]][boundary[1]] + 1
                    self._boundary_list.enqueue(neighbor)
                    self._visited.set_full(neighbor[0], neighbor[1])
        #if DEBUG_CDF:
        #    for line in self._distance_field:
        #        print line
        return self._distance_field
            
        
        #print "w", grid_width     
        #print "h", grid_height
        #for line in self._visited:
        #    print line
        
    
    def best_move(self, entity_type, moves_list, distance_list):
        """
        Find and return the optimal coordinate to move to
        """
        if DEBUG_BM:
            print "best_move()"
            print "BM - entity_type", entity_type
            print "BM - moves_list", moves_list
            print "BM - distance_list", distance_list
        best_distance = float("-inf")
        try:
            best_moves = list(moves_list[-1])
        except TypeError as exp:
            print "best_move() exception"
            print type(moves_list)
            print moves_list
            print exp
        
        #Zombies want to move closer, humans further
        if entity_type == ZOMBIE:
            for dummy_idx in range(0, len(distance_list)):
                distance_list[dummy_idx] *= -1
                
        #Create list containing all coordinates that are "best" distance away
        for dummy_idx in range(0,len(moves_list)):
            if DEBUG_BM:
                print "BM - moves_list[",dummy_idx,"]", moves_list[dummy_idx]
            move_distance = distance_list[dummy_idx]
            if move_distance > best_distance:
                best_distance = move_distance
                best_moves = [moves_list[dummy_idx]]
            if move_distance == best_distance:
                best_moves.append(moves_list[dummy_idx])
                
        #return random entry from list of moves
        return best_moves[(random.randrange(len(best_moves)))]
            
            
    def move_humans(self, distance_field):
        """
        Really just sends HUMAN + distance field to move_entity
        """
        self._human_list = self.move_entity(HUMAN, distance_field)
        
    
    def move_zombies(self, distance_field):
        """
        Really just sends ZOMBIE + distance field to move_entity
        """
        self._zombie_list = self.move_entity(ZOMBIE, distance_field)
                     
    def move_entity(self, entity_type, distance_field):
        """
        Try to abstract move function to take zombie or human
        as an argument and work accordingly
        """ 
        def valid_move_gen(neighbor_function, location):
            """
            Should take a coordinate and an entity type and work out the valid
            moves it can make
            """
            if DEBUG_VM:
                print "valid_moves()"
            moves = list(neighbor_function(location[0], location[1]))
            #Make sure standing still is an option
            moves.append(location)
            #make sure move coordinate isn't full and return
            #list comprehension style
            #return [move for move in moves if self.is_empty(move[0], move[1])]
            #generator style
            for move in moves:
                if self.is_empty(move[0], move[1]):
                    if DEBUG_VM:
                        print "VM - yielding move", move
                    yield move
                    
        if DEBUG_ME:
            print "move_entity()"
            print "ME - entity_type", entity_type
            print "ME - distance_field", distance_field
        new_entity_list = []
        neighbor_function = 0
        if entity_type == HUMAN:
            entity_list = self._human_list
            neighbor_function = self.eight_neighbors
        elif entity_type == ZOMBIE:
            entity_list = self._zombie_list
            neighbor_function = self.four_neighbors
        for entity in entity_list:
            if DEBUG_ME:
                print "ME -entity_list", entity_list
                print "ME - neighbor_function", neighbor_function
            valid_moves = [move for move in valid_move_gen(neighbor_function, entity)]
            if DEBUG_ME:
                print "ME - valid_moves", valid_moves
            #working... but want to eliminate distances method
            #new_entity_list.append(self.best_move(entity_type, valid_moves, [distance for distance in self.distances(valid_moves, distance_field)] ))
            new_entity_list.append(self.best_move(entity_type, valid_moves, [distance_field[move[0]][move[1]] for move in valid_moves ] ))
        if DEBUG_ME:
            print "ME - new_entity_list", new_entity_list
        return new_entity_list
            

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

#failed tests
#obj = Apocalypse(20, 30, [(4, 15), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10)], [], [(18, 14), (18, 20), (14, 24), (7, 24), (2, 22)]) 
#for line in obj.compute_distance_field(HUMAN):
#    print line

#obj = Apocalypse(20, 30, [(4, 15), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10)], [(12, 12), (7, 12)], [])
#for line in obj.compute_distance_field(ZOMBIE):
#    print line
#try:
#    poc_zombie_gui.run_gui(Apocalypse(20, 30, [(4, 15), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10)], [], [(18, 14), (18, 20), (14, 24), (7, 24), (2, 22)]))
#except:
#    "Test Failed"


#poc_zombie_gui.run_gui(Apocalypse(30, 40))
try:
    poc_zombie_gui.run_gui(Apocalypse(30, 40))
except Exception as e:
    print "gui initialization failed"
    print e
#test = Apocalypse(30, 40)