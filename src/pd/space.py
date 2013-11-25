'''
@date 20131124
@author: mjbommar

The Space package defines topologies or spaces
in which the PD games will play out, e.g.,
Lattice2D.
'''

# Load standard packages
import numpy

class Cell(object):
    '''
    The cell class represents a cell or single "unit" of space
    in a lattice or grid.
    '''
    
    # Basic properties
    exclusive = True
    
    def __init__(self, position, exclusive=True):
        '''
        Constructor
        '''
        # Set basic properties
        self.position = position
        self.inhabitants = []
        self.exclusive = exclusive
        
    def add(self, inhabitant):
        '''
        Add an inhabitant to a cell.
        '''
        if self.exclusive == True and len(self.inhabitants) > 0:
            return False
        else:
            self.inhabitants.append(inhabitant)
            return True
        
    def remove(self, inhabitant):
        '''
        Remove an inhabitant to a cell.
        '''
        self.inhabitants.remove(inhabitant)
    
    def get_inhabitants(self):
        '''
        Return inhabitants.
        '''
        return self.inhabitants
    
    def clear_inhabitants(self):
        '''
        Clear all inhabitants.
        '''
        self.inhabitants = []        
        
    def __repr__(self):
        '''
        String representation
        '''
        return "Cell position={0}, inhabitant={1}".format(self.position, self.inhabitants)
        

class Lattice2D(object):
    '''
    The Lattice2D class represents a 2D lattice in which
    agents exist.
    '''
    
    # Basic parameters
    num_cols = 0
    num_rows = 0
    neighborhood_type = None
    
    def __init__(self, num_cols, num_rows, neighborhood_type="von Neumann"):
        '''
        Constructor for the 2D lattice.
        '''
        
        # Set the basic parameters
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.neighborhood_type = neighborhood_type
        self.space = []
        
        # Initialize our space
        # Iterate over rows
        for i in xrange(num_rows):
            row = []
            # Iterate over columns
            for j in xrange(num_cols):
                # Create our cell and add to row
                cell = Cell((i,j))
                row.append(cell)
                
            self.space.append(row)
    
    def get(self, position):
        '''
        Get the cell at a given position.
        '''
        return self.space[position[0]][position[1]]
    
    def put(self, position, inhabitant):
        '''
        Put an inhabitant into a given position.
        '''
        return self.space[position[0]][position[1]].add(inhabitant)
    

    def get_neighbors_von_neumann(self, position, distance):
        '''
        Get von Neumann neighbors.
        '''
        # Initialize
        neighbor_positions = []
        
        # Get the positions
        for i in xrange(-distance, distance+1):
            for j in xrange(-distance, distance+1):
                # Skip self
                if i ==0 and j == 0:
                    continue
                
                # Check boundaries
                if position[0] - i < 0:
                    continue
                elif position[0] + i >= self.num_rows:
                    continue
                elif position[1] - j < 0:
                    continue
                elif position[1] + j >= self.num_cols:
                    continue
                
                # Check Manhattan distance
                if numpy.abs(i) + numpy.abs(j) <= distance:
                    neighbor_positions.append((position[0] + i,
                                               position[1] + j))
        
        # Build full neighbor list
        neighbors = []
        for p in neighbor_positions:
            neighbors.extend(self.get(p).get_inhabitants())

        return neighbors

    
    def get_neighbors(self, position, distance=1):
        '''
        Get the neighbors for a position.
        '''
        if self.neighborhood_type == "von Neumann":
            return self.get_neighbors_von_neumann(position, distance)
        elif self.neighborhood_type == "Moore":
            return self.get_neighbors_moore(position, distance)
        else:
            raise NotImplementedError("Neighborhood type {0} not implemented.".format(self.neighborhood_type))
        
    def __repr__(self):
        '''
        String representation
        '''
        return "Lattice2D ({0},{1}) ({2})".format(self.num_cols, self.num_rows, self.neighborhood_type)