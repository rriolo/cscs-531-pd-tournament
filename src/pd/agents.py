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
    by changing the agent step method, you can make your
    agnts arbiraily  complicated stratigies,   the also can see father,
    go faster and disperse ooffspring farther, but at a cost.

     here is a list of mthods the agents must make available[
     fioollowed by a list of methods they must provide,
      the variables iyt nakes available in the __init__ method.



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
     "vision"   "speed"   "dispeal"   and values are the requwestws cap,
     the world use that ti calg charge oerstep,

   and the birth threshhol whuch is sum(operstepchsrges) * birthnultiplier z9 3 )



more TBA
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
        # prob want space here too   **RR
        self.x = 0
        self.y = 0
        self.is_alive = True
        self.request_birth = False
        self.agent_record = None
        if world:
            self.resources = world.starting_resources
        self.agentCapabiitiesDict = {}
        self.birthThreshold = 10
        ##
        # more TBA
        #

    def printAgent ( self ):
        arec = self.agent_record
        print((self, self.agent_id, self.is_alive, self.resources, arec.age))



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
        print("%s tryBirth: resources %1f  threw %.1f" %\
                  (self.agent_id, self.resources, self.birthThreshold))
        # checjk for open spae
        ag = agents.Agent( self.world )
        # we wabt nam t o be  p


        ag.name =  self.name
        agrec = AgentRecord(ag, self.world )
        ag.agent_record = agrec
        ag.agent_id = agrec.agent_id
        ag.resources = ag.birthThreshold
        self.resources =- ag.resources
        print "************************ created agrec aid >%s< for agid >%s< " %\
            ( agrec.agent_id, ag.agent_id  )
        print "offsp of %s  %s" % (  self.name  , self.agent_id)
        world.agent_list.append( ag )
        print "%d on agent_list" % ( len(world.agent_list))
        world.agent_records_dict[ag.agent_id] = agrec
        world.births  += 1

        #self.mutated  += 0


    def step(self):
        '''
         first choose  an action  to request., ie move or play the pd.
         some agents may loook at thr ooponents history, or
         at thrir own witution. others might play a "pure" dtrategy               or a random one.
         this ;particular agent shooses pd 50%, 50% move

             ex
  *wihou t  lokin at whhat is leagal! so t easeds a lot of turn.s
        '''
        print("Ag .%s step " % (self.agent_id))

        if len( world.agent_list ) < 2 :

            print "cant run with 1 or fewer agents"
            return None

        if  random.random() < 0.5:
             # play pd now, pick ran oppdo
            print "Chose to playe,,,"
            other = world.pickRandomOther( self )
            play = world.cooperate
            grec = world.requestPlayPD ( self, other, play)

        else:
            # see if theere is  randomly chosesn place to momve
            print "Chose to move,,,"
            there = None
            world.requestMoveTo ( self , there )




    def __repr__(self):
        '''
        String representation for our Agent.
        '''
        return "Agent {0}".format(self.name)

if __name__ == "__main__":
    a = Agent(None)



###############################################################

