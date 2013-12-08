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
    '''

    # World context; agent needs to know this to ask about its surroundings.
    world = None

    def __init__(self, world=None):
        '''
        Constructor, which initializes our agent.
        '''
        # Set the name and world
        self.name = "RioloRA"
        self.world = world
        self.agent_id = None
        self.x = 0
        self.y = 0
        self.is_alive = True
        self.request_birth = False

        if world:
            self.resources = world.starting_resources

    def send_agent_id(self):
        return self.agent_id

    def tryBirth(self):
        print("%d tryBirth" % (self.agent_id))


    def step(self):
        print("%d step " % (self.agent_id))

    def __repr__(self):
        '''
        String representation for our Agent.
        '''
        return "Agent {0}".format(self.name)

if __name__ == "__main__":
    a = Agent(None)
