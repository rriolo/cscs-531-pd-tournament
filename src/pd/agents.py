'''
@date 20131124
@author: mjbommar
'''
import world
import random
import agents
from world import *


class Agent(object):
    '''
    The Agent class is a base class, meant to be extended by
    our individual players in the PD world.

    The Agent class defines a shared set of methods and variables
    that the World needs to assume are available to "run."

    this class, taken a a specific example,  implements agents sumilsr to
    the agent in the zones of coop papder,, ]eg,
   a. the play pure c or D stratagies, and dont refusw
   b. they akk haave the same cpbilitgies, ie, max visionrange , smax
   speed and ffospring msx of 1.
   c. hey live in a 30x30 torus , 0 or 1 agent per cell.

    one difference is you can change some of the capabikties, eg,
  '  by changing the agent step method, you can make your
    agnts arbiraily  complicated stratigies,   the also can see father,
 m   go faster and disperse ooffspring farther, but at a cost.

     here is a list of mthods the agents must make available[
     fioollowed by a list of methods they must provide,
      the variables iyt nakes available in the __init__ method.

class Lattice2D(object):


    def __init__(self, world=None):

    def send_agent_id(self):
        return self.agent_id

    def step(self):
        teplevel of agents initiated action per step
        must choose acion,, play pd or move
      def choose_action( self ):

    def choose_reply( self, requestor ):
       somebody offered oplay-you chooseplay or rufeuse

    def tryBirth(self)
   mut have birththres resouces, and there must be n empty cell
    in your dispersal range
     if you meetcriteria you sebd a rfb - request fur bith mess to tworld;
    the msg inludes a capabiliytyDict which is assugns to te cpbiliti ivar
   in the offsping, keys are capab names
     "vision"   "speed"   "dispersal"   and values are the requwestws cap,
     the world use that ti calculate the charge perstep,

   and the birth threshhol whuch is sum of t he basemetab chargfe +'
  all the indiv capality -charges ) * days_costs_required .




    def requestMoveTo (self, agent, destPos ):
    def requestPlayPD (self, requestor, other, focals_play):


ef  getVisibleAgents( self, agent ):
    def  getPlayableAgents( self, agent ):
    def openVisibleCells( self, agent ):
    def getOpenSpaces( self, pos, dist ):
    def displaySpace (  self ):


before creatibngusing position instances, set
    Position.torus = True
    Position.rows = 30
   Position.cols = 30
pos = Position ( r, c ):
    def changeCBy ( self, amt ):
    def changeRBy ( self, amt ):



    def randomlyPlaceInSpace ( self, alist ):
    def isEmptyPosition ( self, pos ):
    def isEmptyPosition ( self, pos ):
    def moveTo ( self, what, fromPos, toPos ):

    def checkLocationInSpace(self,  inhabitant, pos):
    def removeFromSpace (self, ag, pos ):

    def posStr( self, pos ):


    '''


    # World context; agent needs to know this to ask about its surroundings.
    #world = None

    def __init__(self, world ):
        '''
        Constructor, which initializes our agent.
        name identifies the owner and "species"
        agent_id = name + unique id number assigned by world
            this is used as key to this agent's instance
            in the world.agent_records_dict
         x,y its location in the worlds space
          is_alive is set False if the agents resources go <= 0
              and whenit hits max age. i]t can no longer do anythiing'
               and willl be removed by the grm reaper.
          request_bith  the agent can se t it true and the eorld will
            check if thr agent haas the reouces and a place to make offspring

         max_vision
          max_speed
          max_dispersal > 0
        '''
        # Set the name and world
        self.name = "RioloRA"
        self.world = world
        self.agent_id = None

        self.position = None
        self.is_alive = True
        self.request_birth = False
        self.agent_record = None
        self.num_offspring = 0
        if world:
            self.resources = world.starting_resources

        self.agentCapabilitiesDict = world.make_capa_amt_dict ( 3, 1,1,10)
        self.birthThreshold = 10
        ##
        # more TBA
        #






    def printAgent ( self, format, currT ):
        arec = self.agent_record
        age  = currT - arec.time_born

        if format  == 's':
            print((self.name, self.agent_id, self.is_alive, self.resources, arec.age))
        elif format == 'm':
            print((self.name, self.agent_id, self.is_alive, self.resources,\
                       arec.resources, age, self.num_offspring))
        else:
            print((self.name, self.agent_id, self.is_alive, self.resources,\
                       arec.resources, age))
            s = "agentCapabitiesDict.keys():"
            for k in self.agentCapabilitiesDict.keys():
                          ###
                s +=  " %s=%d"   % (  k, self.agentCapabilitiesDict[k])
            s += " total_decrement_Per_Step=%d" % ( \
                arec.total_decrement_Per_Step )
            print s



    def send_agent_id(self):
        return self.agent_id

    def choose_reply( self, requestor ):
        '''
        requestor is ptr to agent who wna t to play PD eith you
           you have to rpely 1 of 3 choices'

           the world will ask that player fo a response, which is
         a) world.refuse
         b) world.cooperate
         c) world,defect


        this is a simple random strategy player

        '''

        r = random.random()
        if r < .333:
            return world.refuse
        elif r < 0.667:
            return world.defect
        else:
            return world.cooperate


    def choose_action( self ):
        '''
        your step, so yhou have t o do
           you have to rpely 1 of 3 choices'

           the world will ask that player fo a response, which is
         a) world.refuse
         b) world.cooperate
         c) world,defect

         this is a simple pure strategy player

        '''
        return world.cooperate



    def tryBirth(self):
        '''
        assemble  info for requesm eg mutationg
        clon
        '''

        vis = self.agentCapabilitiesDict["vision"]
        sp = self.agentCapabilitiesDict["speed"]
        disp = self.agentCapabilitiesDict["dispersal"]
        costs = world.calc_total_cost_per_step  \
( self.agentCapabilitiesDict )
        end = costs * world.days_costs_required

        if end < self.resources:
            world.requestOffspring (self,  vis,sp,disp, end )
            if world.debug > 1 :
                print(("Succeeded in requesting offspring", self, end, self.resources))

	else:
            if world.debug > 1 :
                print(("Failed to request offspring", self, end, self.resources))




    def check_if_want_birth ( self ):
        '''
        a chance to bdelay brth even if they neet technical gpecs
        '''
        return  True



    def step(self):
        '''
         first choose  an action  to request., ie move or play the pd.
         some agents may loook at thr ooponents history, or
         at thrir own witution. others might play a "pure" dtrategy
         or a random one.
         this ;particular agent shooses pd 50%, 50% move

             ex
             *wihou t  lokin at whhat is leagal! so t easeds a lot of turn.s
        '''
        if world.debug > 1 :
            print("Ag .%s step " % (self.agent_id))

        if len( world.agent_list ) < 2 :

            print "cant run with 1 or fewer agents"
            return None

        if world.debug >   0:
            # testing
            openvis = world.space.openVisibleCells( self )
            if world.debugb > 2:
                print "%s at %s can see open  " % \
                ( self.agent_id, world.space.posStr( self.position ) )
            #
            openplay =  world.space.getPlayableAgents( self )

        if  random.random() < 0.5:
             # play pd now, pick ran oppdo
            if world.debug > 1 :
                print "Chose to playe,,,"
            other = world.pickRandomOther( self )
            play = world.cooperate
            grec = world.requestPlayPD ( self, other, play)

        else:
            # see if theere is  randomly chosesn place to momve
            if world.debug > 1 :
                print "Chose to move,,,"
            opensps = world.space.getOpenSpaces( self.position, \
                                         self.agentCapabilitiesDict["speed"] )
            if len(opensps) == 0:
                if world.debug > 1:
                    print " aid %s no where to go"%(agent.agent_id)

                #  focal, action, rmv, omv, fresult , oresult, other ):
                grec = GameRecord( self, World.move, None, None, None, None, None )
                world.add_to_history ( grec )
                return


            #  opick abn oprex cell to go to
            r = random.randrange( len( opensps ) )
            pickpos =  opensps[r]
            grec = world.requestMoveTo ( self , pickpos )




    def __repr__(self):
        '''
        String representation for our Agent.
        '''
        return "Agent {0}".format(self.name)

if __name__ == "__main__":
    a = Agent(None)



###############################################################

