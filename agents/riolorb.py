'''
@date 20131124
@author: mjbommar
'''

import agents

class RioloAgentB(agents.Agent):
    '''
    The Agent class is a base class, meant to be extended by
    our individual players in the PD world.

    The Agent class defines a shared set of methods and variables
    that the World needs to assume are available to "run."
    '''

    # Agent name
    name = None

    # World context; agent needs to know this to ask about its surroundings.
    world = None

    def __init__(self, world):
        '''
        Constructor, which initializes our agent.
        '''
        super(RioloAgentB, self).__init__(world=world)
        # Set the name and world
        self.name = "RioloB"
        self.world = world
        self.agent_id = 1
        self.resources = world.starting_resources
        self.x = 0
        self.y = 0
        self.request_birth = False


    def tryBirth(self):
        print("%d tryBirth" % ( self.agent_id  ) )


    def step(self):
        print("%d step "  % ( self.agent_id  ) )





    def __repr__(self):
        '''
        String representation for our Agent.
        '''
        return "Agent {0}".format(self.name)
