'''
@date 20131124
@author: mjbommar
'''


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





    '''

    # World context; agent needs to know this to ask about its surroundings.
    world = None

    def __init__(self, world=None):
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

        if world:
            self.resources = world.starting_resources

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

         this is a simple pure strategy player

         '''
        return world.cooperate



    def choose_action( self ):
       '''
        yiur etep, so yhou have t o do
           you have to rpely 1 of 3 choices'

           the world will ask that player fo a response, which is
         a) world.refuse
         b) world.cooperate
         c) world,defect

         this is a simple pure strategy player

         '''
        return world.cooperate



    def tryBirth(self):
        print("%d tryBirth" % (self.agent_id))


    def step(self):
        '''
         choose]\  an acrion  to request., ie moce orplay pd.
         normalllyh fogure ou t waht is good opipn

         this ;particlre agernt shooses pd 50%, 505 pfd
         c=before lokin at whjat is leagl
        '''
        print("%d step " % (self.agent_id))


        if  randmom.random 0.5:
             # play pd
            # pick ran oppdo
            other = a rqandomly vhoodrn fro th vis Koponne
            play = cooopt
            requestPlayPD (self, requestor, other, play):

        else:
            # see if theere is  randomly chosesn place to momve
            requestMove ( self , there )




    def __repr__(self):
        '''
        String representation for our Agent.
        '''
        return "Agent {0}".format(self.name)

if __name__ == "__main__":
    a = Agent(None)
