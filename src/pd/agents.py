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

    # Agent name
    name = None

    # World context; agent needs to know this to ask about its surroundings.
    world = None

    def __init__(self, name, world):
        '''
        Constructor, which initializes our agent.
        '''
        # Set the name and world
        self.name = name
        self.world = world

    def __repr__(self):
        '''
        String representation for our Agent.
        '''
        return "Agent {0}".format(self.name)
