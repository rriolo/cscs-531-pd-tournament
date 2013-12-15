'''
@date 20131124
@author: mjbommar

The Space package defines topologies or spaces
in which the PD games will play out, e.g.,
Lattice2D.

before using, afyter yiu f=have imported oacw, you;ll'want set the
Position cvlaases rows and cols class varuiables to the jdimensuins of the spac, and sewte tyorus true or falsree as needed i f yiy wsnt

then yiu ill need to get numbers into Positines by
 pos = Position( ror, col ) or;
 pos.setr( d ) ssetc (d)

'''

# Load standard packages
import numpy
import random
import sys



class Cell(object):
    '''
    The cell class represents a cell or single "unit" of space
    in a lattice or grid.
    '''

    # Basic properties
    exclusive = True

    def __init__(self, position,exclusive=True):
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

#################################################################
################################################################

class Lattice2D(object):
    '''
    The Lattice2D class represents a 2D lattice in which
    agents exist.
    '''

    # Basic parameters
    num_cols = 0
    num_rows = 0
    neighborhood_type = None
    world = None

    def __init__(self, world, num_cols, num_rows, torus,  neighborhood_type="von Neumann"):
        '''
        Constructor for the 2D lattice.
        '''

        # Set the basic parameters
        self.world = world
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.neighborhood_type = neighborhood_type
        self.space = []
        self.torus = torus
        # use this position class
        self.spacePosition = Position
        Position.cols = num_cols
        Position.rows = num_rows
        # Initialize our space
        # Iterate over rows
        for i in xrange(num_rows):
            row = []
            # Iterate over columns
            for j in xrange(num_cols):
                # Create our cell and add to row
                cell = Cell((i, j))
                row.append(cell)

            self.space.append(row)

        print "space is consructed.."


    def get(self, pos ):
        '''

        then put Get a copy of cell contents cell at a
        given position.
        '''
        return self.space[pos.row][pos.col]





    def pop(self, pos ):
        '''
        Get a copy of cell contents cell at a given position.
        returns None if noby thre
        puts Nlone in regardless
        '''
        ret = None
        ret = self.space[pos.row][pos.col]
        self.space[pos.row][pos.col].add(None)


    def get_neighbors_von_neumann(self, position, distance):
        '''
        Get von Neumann neighbors.
        '''
        # Initialize
        neighbor_positions = []

        # Get the positions
        for i in xrange(-distance, distance + 1):
            for j in xrange(-distance, distance + 1):
                # Skip self
                if i == 0 and j == 0:
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


    ##############################################################
    ###############################################################\
    ############################################################  \#
    ##  use only metuhods from
    ############ ##########   here to next red line
    #############

#@####@@00--switcgh to col, row


    def randomlyPlaceInSpace ( self, alist ):

        numags = len( alist )
        if numags >  self.world.max_pop:
            print "too mny agents to fit in the world."
            exit

        if numags >  self.world.max_pop / 2:
            print "it may tahe awghile yto gind spce for kl these"

        wsz = self.world.worldSize
        numdone = 0
        while len(alist) > numdone:
            notfound = True
            while notfound:
                r = random.randint(0,wsz-1 )
                c = random.randint(0,wsz-1 )
                p1 = Position(r,c)
                if  self.isEmptyPosition(p1):
                    ag = alist[numdone]
                    numdone += 1
                    self.putAt( ag, p1 )   # put adent in world
                    ag.position = p1        # tell thr agebt whre it is
                    notfound = False
                    if numdone % 5 == 0 :
                        print ".5."
        print "done loading innit adgents randomly  space"


    def isEmptyPosition ( self, pos ):

        l = self.space[pos.row][pos.col].inhabitants
        if len(l) > 0:
            return False
        return True

    def isOccupiedPosition ( self, pos ):

        l = self.space[pos.row][pos.col].inhabitants
        if len(l) > 0:
            return True
        return False


    def getOccupant (self, pos ):
        '''
        return copy of pointer in cell
        '''
        return self.space[pos.row][pos.col].inhabitants[0]



    def putAt(self,  inhabitant, pos):
        '''
        Put an inhabitant into a given position.
        assume is legak. tell thre agent where it is
        '''
        inhabitant.position = pos
        return self.space[pos.row][pos.col].inhabitants.append(inhabitant)


    def checkLocationInSpace(self,  inhabitant, pos):
        '''
        see if tthi s gyuy is where he thinks he is
        '''
        ir  = inhabitant.position.row
        ic = inhabitant.position.col
        if ir != pos.row or ic != pos.col:
            print "**@@@*** agent %s" %\
                ( inhabitant.agent_id )
            print " fouind its pos %s not the expected one," % \
                ( posStr(inhabitant.position),  posStr(pos) )
            return False
        return True

    def posStr( self, pos ):
        return "%d,%d" % ( pos.row, pos.col )


    def removeFromSpace (self, ag, pos ):
        if pos != None:
            self.space[pos.row][pos.col].inhabitants = []
        else:
            print "**@#@*** REMOVAL failed: no onoe at pos."


    def moveTo ( self, what, fromPos, toPos ):
        self.space[toPos.row] [toPos.col].inhabitants.append ( what )
        what.position = toPos

        self.space[fromPos.row] [fromPos.col].inhabitants = []
        return self



    def  getVisibleAgents( self, agent ):

        '''
        return klistof pointers to agnts this agnt can see
        '''
        # tr,tc is where we wre looking
        # run it acroos col for eah row, ask he spacw
         # if hr is ajything threr
        vis = agent.agentCapabilitiesDict["vision"]

        retlist = []
        cntrR = pos.row
        cntrC = pos.col
        minR = cntrR - vis
        maxR = cntrR + vis
        minC = cntrC - vis
        maxC = cntrC + vis
        if self.world.debugb > 0:
            print "agenys in vis %d of %d,%d:" %\
                ( vis, cntrR,cntrC)
        for tr in range ( minR, maxR ):
            for tc in xrange ( minC , maxC ):
                tpos = Position(tr, tc )
                if not self.isEmptyPosition( tpos ):
                    cell = self.space[tpos.row][tpos.col]
                    foundag = cell.inhabitants[0]
                    if foudag != ag:
                        # cant see yoiur selkf
                        retlist.append( foundag )
                else:
                    if self.world.debugb > 3:
                        print "empty: "
        if self.world.debugb > 3:
            print [  a.agent_id for a in retlist ]
        return retlist


    def  getPlayableAgents( self, agent ):
        retlist = []
        pos = agent.position
        cntrR = pos.row
        cntrC = pos.col
        minR = cntrR - 1
        maxR = cntrR + 1
        minC = cntrC - 1
        maxC = cntrC + 1
        if self.world.debugb > 0:
            print "agenys in 1 of %d,%d:" %\
                (  cntrR,cntrC)
        for tr in range ( minR, maxR ):
            for tc in xrange ( minC , maxC ):
                tpos = Position(tr, tc )
                if not self.isEmptyPosition( tpos ):
                    cell = self.space[tpos.row][tpos.col]
                    foundag = cell.inhabitants[0]
                    if foundag != agent:
                        # dont includes the lookin agent
                        retlist.append( foundag )
                else:
                    if self.world.debugb > 3:
                        print "empty: "
        if self.world.debugb > 3:
            print "playable (d=1) agents"
            print [  a.agent_id for a in retlist ]



    def openVisibleCells( self, agent ):
        dist = agent.agentCapabilitiesDict["vision"]
        pos = agent.position
        return self.getOpenSpaces( pos, dist )


    def getOpenSpaces( self, pos, dist ):
        '''
        retuen positioms or open cell im hte square pos+/-dist
        dist < worldsize / 2 to respec tour
        '''

        retlist = []
        cntrR = pos.row
        cntrC = pos.col
        minR = cntrR - dist
        maxR = cntrR + dist
        minC = cntrC - dist
        maxC = cntrC + dist
        if self.world.debugb > 0:
            print "open cells inn %d of %d,%d:" %\
                ( dist, cntrR,cntrC)
        for tr in range ( minR, maxR ):
            for tc in xrange ( minC , maxC ):
                tpos = Position(tr, tc )
                if self.isEmptyPosition( tpos ):
                    retlist.append(  tpos )
        if self.world.debugb > 3:
            print "empty: "
            print [  self.posStr(p) for p in retlist ]
        return retlist



    def displaySpace (  self ):
        ocnt = 0
        print " "
        for r in range( self.num_cols ):
            sys.stdout.write ("-----")
        for r in range ( self.num_rows ):
            for c in range ( self.num_cols ):
                l = self.space[r][c].inhabitants
                if len( l ) == 0:
                    sys.stdout.write( "    |" )
                else:
                    aid = l[0].agent_id
                    ocnt += 1
                    sys.stdout.write("%5.5s|"%( l[0].agent_id))
            sys.stdout.write ("\n")

            #for r in range( self.num_cols ):
            #         sys.stdout.write ("-----")

        for r in range( self.num_cols ):
            sys.stdout.write( "-----")
        print " "
        print "%d cells occupied." % (ocnt)

####################################################################
###################################################################
#####################################################################

class Position (  object ):

    rows = 0
    cols = 0
    torus = True

    def __init__(self, r, c ):
        if self.torus:
            self.row = (r  + (self.rows *  2)) % self.rows
            self.col = (c  + (self.cols *  2)) % self.cols
        else:
            self,row = row
            self,col = c



    def setr  ( r ):
        if self.torus :
            self.row = (r  + (self.rows *  2)) % self.rows
        else:
            self.row = r
        return self


    def setc ( self, c ):
        if self.torus :
            self.col = (c  + (self.cols *  2)) % self.cols
        else:
            self.col = c
        return self


    def changeCBy ( self, amt ):
        '''
        add amt which may be +/- to posionc -dim, thrn norm
        '''
        if self.torus :
            self.col = (self.col + amt  + (self.cols *  2)) % self.cols
        else:
            self.col += amt
        return self


    def changeRBy ( self, amt ):
        '''
        add amt which may be +/- to posionR -dim, thrn norm
        '''
        if self.torus :
            self.row = (self.row + amt  + (self.rows *  2)) % self.rows
        else:
            self.row += amt
        return self
