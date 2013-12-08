

'''
@date 20131124
@author: mjbommar

The World package and class define the context in which the
 PD games play out


need
* history strucrure
* vision info
  vislble-agents
  empty cells


*  make all woelr par vlaues availabe;





'''

# Load standard packages
import os
import sys
import random

# Load our agents module
import agents
import space


class AgentRecord(object):
    '''
the AgentRecord will keep trak  of
        * te agents current resource_level
        * the agevts caoabities (max speed, etc
        *  the agents total_decrement_per_step
        * die_step
        * a pointer to the agent object
        * step_status (eg so it cant moce twicw un  inw step

        '''
    # World context; agent needs to know this to ask about its surroundings.
    def __init__(self, agent_ptr, world):
        self.world = world
        self.max_lifetime = 100
        self.name = agent_ptr.name
        self.agent_id = "%16s-%09s" % (agent_ptr.name, self.world.next_ID)
        self.world.next_ID += 1
        self.agent_ptr = agent_ptr
        self.die_step = self.world.curT + self.max_lifetime - 1
        self.resources = world.starting_resources

        # fake srtuuff
        self.total_decrement_Per_Step = 2
        # step-statuse

       # &etc


#################################################################
################################################################



class World(object):
    '''
    The World class defines the base class for
    repeated PD games with an arbitrary pool of players
    in a lattice.  It k\eeeps track of the values of model parameters:
      stopT - number of ticks in one model run. each tick every agent
         ; in rasndom order. is sent the step message
      worldSize  wall size of square
      baseResCostPerT
      costPerCellVisRange
      costPerUnitSpeed
      costPerCellDispersalRange


      nextInt = 0

    '''

    #
    next_ID = 0
    # Space
    space = None



    def __init__(self, sysargv1):
        '''
        Constructor
        '''
        # Set parameters defaolts
        self.agent_path = "agents/"
        self.stopT = 150
        self.worldSize = 40
        self.costPerTbaseResMetabol = 3
        self.costPerCellVisRange = 1
        self.costPerUnitSpeed = 1
        self.costPerCellDispersalRange = 1
        self.curT = 0
        self.max_lifetime = 50
        self.payoff_multiplier = 2
        self.debug = 0
        self.verbose = 0

        self.starting_resources = 21


        # puts vak=ls from runcmd line in self-vars
        self.processCmdLineArgs(sysargv1)

        # Initialize agents_record_dict, agent snd newborns list
        self.agent_list = []
        self.agent_records_dict = {}
        self.newborns = []

        # Load agents
        # populate the agent_list, the agent_records_dict and
        # whatever "space" there is
        self.load_agents(self.agent_path)

        # Initialize space
        self.space = None  # TBI



    def processCmdLineArgs(self, args):
        # Process command line arguments of the form
            #   parName=value | -h | --help
        for arg in args:
            if arg == '-h' or arg == '--help':
                help()
                quit()
            # Split about the equal sign, into name and value of the argument.
            arg = arg.split('=')
            name = arg[0]
            value = arg[1]
            # print  "arg='%s' name='%s'  value='%s'\n" % (arg, name, value )
            if name == 'agent_path' or name == 'aP':
                self.agent_path = value
            elif name == 'stopT' or name == 'T':
                self.stopT = int(value)
            elif name == 'worldSize' or name == 'wSz':
                self.worldSz = int (value)
            elif name == 'debug' or name == 'D':
                self.debug = int(value)
            elif name == 'verbose' or name == 'V':
                    self.debug = int(value)
            elif name == 'max_lifetime' or name == 'mlt':
                self.max_lifeime = int(value)
            elif name == 'starting_resources' or name == 'sr':
                self.starting_resources = int(value)
            #
            # FILL In THE RESt
            #

            else:
                print  " Unknown name in arg='%s'name='%s' value='%s'\n" % \
                    (arg, name, value)
                help()





    def load_agents(self, agent_path):
        '''
        Load all tournament agents from a given path onto the agent_list.
        Fir each agent loaded, create a AgentRecord instance and
         add it to the current_players_dict, with a  key the agnet id assigne
         by thrr world whne agents are loaded or bormn,
         agents have a species_name =  creators lastname_first initial,
         followed by     a unique integer nextID is appended in sttring f]orm,'
        the AgentRecord will keep trak  of
        * te agents current resource_level
        * the agevts caoabities (max speed, etc),
        *  the agents total_decrement_per_step
        * max_step_alive
        * a pointer to the agent object
        * step_status (eg so it cant moce twicw un  inw step

        assumes agent_list ans agent_records_dict are initualized
        '''

        if self.debug > 0:
            print ("       +++ load_agents from %s >>>" % (self.agent_path))

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

            if self.debug > 0:
                print ("       +++  open %s >>>" % (module_name))

            # Now iterate over module contents.
            for object_name in dir(sys.modules[module_name]):
                object_value = getattr(sys.modules[module_name], object_name)
                try:
                    # Instantiate.
                    object_instance = object_value(self)
                    # If the variable matches the Player class type, include.
                    if isinstance(object_instance,
                                  agents.Agent):
                        print("Adding " + object_name)
                        # Set ourself as the tournament
                        object_instance.tournament = self

                        # create a record for it
                        agrec = AgentRecord(object_instance, self)
                        object_instance.agent_record = agrec
                        self.agent_records_dict[ object_instance.agent_id ] = object_instance

                        # Add to list
                        self.agent_list.append(object_instance)
                except Exception, E:
                    pass



    def printAllAgents (self):
        print "      agent_id            agent            agentRecord  "
        print "     agent_id    age    resources          resources  "
        for a in self.agent_list:
            aRec = a.agent_record
            age = aRec.max_lifetime - self.curT  ####  +/- 1   ??
            print("%s  %.1f  %.1f %.1f" % (a.agent_id, age , a.resources, aRec.resources))


    def compute(self):
        '''
        the main dynamics each step
        shuffle the agent_list
        give eah agent a chance to step out
              move or play or give birth
        then the world checjs and cleabn out  the dead/
        then add new born to the worlgd
        then print out stats
        '''
        if self.debug > 0:
            print (">>>Start step %d >>>" % (self.curT))

        # get a bettr rng
        random.shuffle(self.agent_list)

        # the agent might ask to move or play
        for a in self.agent_list:
            a.step()

        # paty  their bills
        for a in self.agent_list:
            arec = self.agent_records_dict[ a.agent_id ]
#            a.resources =  a.resources - arec.total_decrement_Per_Step
#            arec.resources = arec.resources -  arec.total_decrement_Per_Step

        self.applyTheGrimReaper()

        for a in self.agent_list:
            if a.request_birth:
                a.tryBirth()

        if self.verbose > 3:
            self.printAllAgents()
        elif self.verbose > 0:
            self.printStepSummary()


    def requestMoveTo (self, agent, destination_loc):
        '''
        agnt wants to move; chech that
        dest_loc us open and withibn agents range'
        if so, move and return true; if noyt return false
        '''

        # TBA
        # dist caj=lculatr
        # mover

        return False


    def requestPlayPD (self, requestor, other, play):
        '''
        agent reqestor has picked an opponent and a play
         the world will ask that player fo a response, which is
         a) world.refuse
         b) world.cooperate
         c) world,defect
         th world thy cals ho owes  or gains, tells both agbnts th results,
         uodates ita agentrecord, chwcks uf wythwr euither is dead;

         '''
        pass



    def applyTheGrimReaper (self):
        if self.debug > 0:
            print("++++++ applyThegrimReaper stp %d >>>" % (self.curT))
            for a in self.agent_list:
                if a.agent_record.max_lifetime < self.curT:
                    print("%s should die at %d." % \
                       (a, agent_id, a.agent_record.max_lifetime , self.curT))


    def printStepSummary(self):
        '''
        print s]ummary stats eg counts of each agent type

        '''
        if self.debug > 0:
            print ("       +++ printStepSummary %d >>>" % (self.curT))


    def printFinalStats(self):
        '''
        print  stats eg counts of each agent type

        '''
        if self.debug > 0:
            print ("       +++ printFinalStats %d >>>" % (self.curT))





    def __repr__(self):
        '''
        String representation
        '''
        return "World (player_pool={0})"\
            .format(len(self.agents))

#################################################################
##############################################################333

if __name__ == "__main__":
    print  str(sys.argv)  # for cmd line parameters

    # create world, which inits space, create agents agentrecords
    world = World (sys.argv[1:])
    agents.world = world
    AgentRecord.world = world

    print("\nThe players:")
    world.printAllAgents()
    while  world.curT < world.stopT:
        world.compute()
        world.curT += 1

    print("\nFinal scores:")
    world.printAllAgents()

    print("All done.")



