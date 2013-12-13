'''
@date 20131124
@author: mjbommar
'''
import world
import random
import agents
import agentsC
from world import *


class AgentC(object):
    '''
      *********    this claass always cooperates   **********

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
        self.num_offspring = 0
        if world:
            self.resources = world.starting_resources
        self.agentCapabilitiesDict = world.make_capa_amt_dict ( 3, 1,1,1)
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
            s = "agentCapabilitiesDict.keys():"
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
        clone
        '''
        vis = self.agentCapabilitiesDict["vision"]
        sp = self.agentCapabilitiesDict["speed"]
        disp = self.agentCapabilitiesDict["dispersal"]
        costs = world.calc_total_cost_per_step ( self.agentCapabilitiesDict )
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
         at thrir own witution. others might play a "pure" dtrategy               or a random one.
         this ;particular agent shooses pd 50%, 50% move

             ex
  *wihou t  lokin at whhat is leagal! so t easeds a lot of turn.s
        '''
        if world.debug > 1 :
            print("Ag .%s step " % (self.agent_id))



        if len( world.agent_list ) < 2 :

            print "cant run with 1 or fewer agents"
            return None

        other = world.pickRandomOther( self )
        play =  world.cooperate
        grec = world.requestPlayPD ( self, other, play)



    def __repr__(self):
        '''
        String representation for our Agent.
        '''
        return "Agent {0}".format(self.name)

if __name__ == "__main__":
    a = Agent(None)



###############################################################

