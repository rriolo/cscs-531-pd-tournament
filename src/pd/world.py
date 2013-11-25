'''
@date 20131124
@author: mjbommar

The World package and class define the context in which the
repeated PD games play out.
'''

# Load standard packages
import os
import sys

# Load our agents module
import agents
import space

class World(object):
    '''
    The World class defines the base class for 
    repeated PD games with an arbitrary pool of players
    in a lattice.
    '''

    # Pool of agents
    agents = []
    
    # Agent path
    agent_path = None
    
    # Space
    space = None

    def __init__(self, agent_path='agents'):
        '''
        Constructor
        '''
        # Set parameters
        self.agent_path = agent_path

        # Load agents
        self.agents = self.load_agents(agent_path)
        
        # Initialize space
        self.space = 


    def set_pool(self, player_pool):
        '''
        Set the agent pool.
        '''
        # Set the agent pool
        self.agents = agents

    def load_agents(self, agent_path):
        '''
        Load all tournament agents from a given path.
        '''

        # Initialize player list
        agent_list = []

        # Add path to the system path
        sys.path.append(agent_path)

        # Load all the files in path
        for file_name in os.listdir(agent_path):
            # Skip non-py files
            if not file_name.lower().endswith('.py'):
                continue

            # Get module name
            module_name = os.path.basename(file_name).replace(".py", "")

            # Import the module
            __import__(module_name, globals(), locals(), ['*'])

            # Now iterate over module contents.
            for object_name in dir(sys.modules[module_name]):
                object_value = getattr(sys.modules[module_name], object_name)
                try:
                    # Instantiate.
                    object_instance = object_value()

                    # If the variable matches the Player class type, include.
                    if isinstance(object_instance,
                                  agents.Agent):
                        # Set ourself as the tournament
                        object_instance.tournament = self
                        # Add to list
                        agent_list.append(object_instance)
                except Exception:
                    pass

        # Return the player list
        return agent_list


    def __repr__(self):
        '''
        String representation
        '''
        return "World (player_pool={0})"\
            .format(len(self.agents))


if __name__ == "__main__":
    pass