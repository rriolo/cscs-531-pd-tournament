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
import numpy
import pickle

# Load our agents module
import agents
import agentsC
import space
from space import *

############################################################


class GameRecord(object):

    '''
    Record what happ]ens for every step() message executed
    focal = ptr agent executing thr step
    action = wha foval choose to do: 'world.move' = move , eorlf.pd
    move = for M acion, disance mmoved
          for P. world.eefuse,cooperate. defect
     result  = sc]ore  in pd, dist moved, or refused payoff, or None
     othrer = ptr to oth er agent


these are added to curGameRecorList, whihx xhanges at start of tuime steop,
  the  lists are in  the game_histories dict, keyed by curT whenplayed
    '''

    def __init__(self, focal, action, rmv, omv, fresult, oresult, other):
        self.focal = focal
        self.action = action
        self.requestor_move = rmv
        self.other_move = omv
        self.other = other
        self.focals_result = fresult
        self.other_result = oresult

#########################################################


class AgentRecord(object):

    '''
    the AgentRecord will keep trak
        * te agents current resource_level
        * the agevts caoabities (max speed, etc
        *  the agents total_decrement_per_step
        * max_lifetime (die_step)
        * a pointer to the agent object
        * step_status (eg so it cant moce twicw un  inw step

        '''
    # World context; agent needs to know this to ask about its surroundings.

    def __init__(self, agent_ptr, world):
        # Set pointer to world
        self.world = world

        # Set agent record parameters
        self.time_born = self.world.curT
        self.max_age = self.world.max_lifetime
        self.max_lifetime = world.curT + self.max_age
        self.name = agent_ptr.name
        s = "%s-%03d-%03d" % (agent_ptr.name, world.curT, World.next_ID)
        if world.debug > 1:
            print "in ag  init aid >%s<" % (s)
        self.agent_id = s
        World.next_ID += 1
        self.agent_ptr = agent_ptr
        # self.die_step = self.world.curT + self.max_lifetime - 1
        # self.age = 0
        self.resources = world.starting_resources

        # fake srtuuff
        self.total_decrement_Per_Step = 2
        # step-statuse


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

    # Player response and gneeral enum
    refuse = 2
    cooperate = 0
    defect = 1
    pd = 3
    move = 4
    payoff_matrix = [[(3, 3), (0, 5)],
                     [(5, 0), (1, 1)]]

    def playPD(self, move1, move2):
        pay1, pay2 = world.payoff_matrix[move1][move2]
        return pay1 * self.payoff_multiplier, pay2 * self.payoff_multiplier

    def __init__(self, sysargv1):
        '''
        Constructor
        '''
        # Set parameters defaolts
        self.agent_path = ""  # "agents/"
        self.stopT = 150
        self.worldSize = 30

        self.days_costs_required = 2
        self.costPerTbaseResMetabol = 3
        self.costPerCellVisRange = 1
        self.costPerUnitSpeed = 1
        self.costPerCellDispersalRange = 1

        self.prob_mut = 0.0
        self.curT = 0
        self.num_created_agents = 4
        self.max_lifetime = 50
        self.payoff_multiplier = 3
        self.debug = 0
        self.debugb = 4
        self.verbose = 0
        self.rebirth_prob = 0.0
        self.starting_resources = 21
        self.refusal_cost = 3
        self.initial_agent_type = "random"

        # puts vak=ls from runcmd line in self-vars
        self.processCmdLineArgs(sysargv1)

        # Initialize agents_record_dict, agent snd newborns list
        self.agent_list = []
        self.agent_records_dict = {}
        self.newborns = []
        self.game_histories = {}  # dict key is tim step int. valueameRecorda
        self.saveFilename = "zoc.sav"

        # Initialize space
        print "aabout to create space:"
        self.space = Lattice2D(
            self, self.worldSize, self.worldSize, True, "Moore")
        self.max_pop = self.worldSize * self.worldSize

        # Initialize agents_record_dict, agent snd newborns list
        self.agent_list = []
        self.agent_types_dict = {}

        self.capability_costs = {"vision": self.costPerCellVisRange,
                                 "speed": self.costPerUnitSpeed,
                                 "dispersal": self.costPerCellDispersalRange,
                                 "basemetab": self.costPerTbaseResMetabol}

        # stats
        self.totnumMove = 0
        self.totnumofferpd = 0
        self.totnumrefuse = 0
        self.totnumdef = 0
        self.totnumcoop = 0
        self.totnumstarved = 0
        self.totnumold = 0
        self.births = 0
        self.mutated = 0

        self.popAvgVis = 0.0
        self.popAvgSpd = 0.0
        self.popAvgDis = 0.0
        self.firstThisStep = False  # conrold printing

        # Load agents
        # populate the agent_list, the agent_records_dict and
        # whatever "space" there is with agents in *py files
        # in the agent_path. if agent_path  is "", create copies
        # of the base src/pd/agents.py class.
        if self.agent_path != "":
            self.load_agents(self.agent_path)
        else:
            print "about to call creaye unit agents"
            self.create_initial_agents(self)

        # Initialize placenent in space
        print("clling random place agents ...")
        self.space.randomlyPlaceInSpace(self.agent_list)
        if self.verbose > 1:
            self.space.displaySpace()

    def calc_total_cost_per_step(self, amtsDict):
        '''
        costs ar the same, buyt amuts vary
        '''
        tot = self.capability_costs["basemetab"]
        tot += self.capability_costs["vision"] * amtsDict["vision"]
        tot += self.capability_costs["speed"] * amtsDict["speed"]
        tot += self.capability_costs["dispersal"] * amtsDict["dispersal"]
        return tot

    def make_capa_costs_dict(self, metab, vis, sp, disp):
        self.capability_costs = {"vision": vis,
                                 "speed": sp, "dispersal": disp, 
                                 "basemetab": metab}

    def make_capa_amt_dict(self, metab, vis, sp, disp):
        return {"vision": vis,
                "speed": sp, "dispersal": disp, "basemetab": metab}

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
                self.worldSz = int(value)

            elif name == 'debugb' or name == 'birs':
                self.debugb = int(value)
            elif name == 'debug' or name == 'D':
                self.debug = int(value)

            elif name == 'verbose' or name == 'V':
                self.verbose = int(value)
            elif name == 'max_lifetime' or name == 'mlt':
                self.max_lifetime = int(value)
            elif name == 'rbp':
                self.rebirth_prob = float(value)
            elif name == 'starting_resources' or name == 'sr':
                self.starting_resources = int(value)
            elif name == 'num_created_agents' or name == 'nca':
                self.num_created_agents = int(value)

            elif name == 'prob_mut' or name == 'prm':
                self.prob_mut = float(value)

            elif name == 'costPerTbaseResMetabol' or name == 'cM':
                self.costPerTbaseResMetabol = int(value)
            elif name == 'costPerCellVisRange' or name == 'cpv':
                self.costPerCellVisRange = int(value)
            elif name == 'costPerUnitSpeed' or name == 'cps':
                self.costPerUnitSpeed = int(value)
            elif name == 'costPerCellDispersalRange' or name == 'cpdr':
                self.costPerCellDispersalRange = int(value)

            elif name == 'days_costs_required' or name == 'dcr':
                self.days_costs_required = int(value)

            elif name == 'verbose' or name == 'v':
                self.verbose = int(value)
            elif name == 'refusal_cost' or name == 'rc':
                self.refusal_cost = int(value)

            elif name == 'payoff_multiplier' or name == 'pm':
                self.payoff_multiplier = int(value)

            elif name == 'initial_agent_type' or name == 'iat':
                self.initial_agent_type = value

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

            module_name = os.path.basename(file_name).replace(".py", "")
            print("pr module name >%s<  filename >%s<" %
                  (module_name, file_name))
            # Import the module
            __import__(module_name, globals(), locals(), ['*'])

            print("done module name >%s<  filename >%s<" %
                  (module_name, file_name))

            if self.debug > 0:
                print ("       +++  open %s >>>" % (module_name))

            # Now iterate over module contents.
            for object_name in dir(sys.modules[module_name]):
                print "object_name >%s< " % (object_name)
                if object_name == "numpy":
                    print "skipping  nympy..."
                    break
                object_value = getattr(sys.modules[module_name], object_name)
                print "objectr valuie"
                # print object_value
                try:
                    # Instantiate.
                    print "try to instantiate..."
                    object_instance = object_value(self)
                    print object_instance
                    print "--> instance {0} ".format(object_instance)
                    # If the variable matches the Player class type, include.
                    if isinstance(object_instance,
                                  agents.Agent):
                        print("Adding " + object_name)

                        # create a record for it
                        try:
                            agrec = AgentRecord(object_instance, self)
                        except Exception as E:
                            print E
                        object_instance.agent_record = agrec
                        object_instance.agent_id = agrec.agent_id

                        print "created agrec aid >%s< for agid >%s< " % \
                            (agrec.agent_id, object_instance.agent_id)
                        self.agent_list.append(object_instance)
                        print "%d on agent_list" % (len(self.agent_list))

                        try:
                            self.agent_records_dict[
                                object_instance.agent_id] = agrec
                        except Exception as E:
                            print E
                        print("max_age %d  max_lifetime %d (curT %d)" %
                              agrec.max_age, agrec.max_lifetime, self.curT)
                        # Add to list
                        self.agent_list.append(object_instance)
                        print "%d on agent_list" % (len(self.agent_list))
                except Exception as E:
                    pass

    def create_initial_agents(self, world):
        '''
        if not loadagents via agents_path, create agents.
        by deafualt it wil ttry o create copies of the class
        Created_Agents and or agents.Agent the baseclass.

        '''
        print "create_initial_agents "

        for i in range(self.num_created_agents):
            if self.initial_agent_type == "allC":
                ag = agentsC.AgentC(self)
            else:
                ag = agents.Agent(self)
            ag.name = "c%d" % (i)
            agrec = AgentRecord(ag, self)
            ag.agent_record = agrec
            ag.agent_id = agrec.agent_id
            if self.debug > 0:
                print "created agrec aid >%s< for agid >%s< " % \
                    (agrec.agent_id, ag.agent_id)
            self.agent_list.append(ag)
            # print "%d on agent_list" % ( len( self.agent_list))
            self.agent_records_dict[ag.agent_id] = agrec
            ag.agentCapabilitiesDict["vision"] = i
            ag.agentCapabilitiesDict["speed"] = i
            ag.agentCapabilitiesDict["dispersal"] = i
            ag.total_decrement_Per_Step = self.calc_total_cost_per_step(
                ag.agentCapabilitiesDict)
            ag.resources = ag.world.starting_resources
            agrec.resources = ag.world.starting_resources

    def requestOffspring(self, ag, vis, sp, disp, end):
        '''
        worlld ddoes calcs for min end
        thrn checkd that aag sent rnouh
        and thasjt it resourcees cna acover it
        then ckheck for place
        ikf its all good,,  make neborn,
        trna end, set up capa'

        reutn None if somehn if went swrong
        '''
        capa = self.make_capa_amt_dict(
            self.costPerTbaseResMetabol, vis, sp, disp)
        costs = self.calc_total_cost_per_step(capa)
        if costs * self.days_costs_required > end:
            print "costs > endowment no offspring given"
            return None

        if len(self.agent_list) + len(self.newborns) >= self.max_pop:
            if self.firstThisStep:
                print "FAILED birth: world is full with %d agents + %d newborns at T=%d" % \
                    (len(self.agent_list), len(self.newborns), self.curT)
                self.firstThisStep = False
            return None

        disp = ag.agentCapabilitiesDict["dispersal"]
        openposlist = self.space.getOpenSpaces(ag.position, disp)
        if len(openposlist) == 0:
            print "there is no openspaces for offspring"
            print "ag %s, disp=%d  pos=%s" % \
                (ag.agent_id, disp, self.space.posStr(ag.position))
            return None

        # pick one pos at  random
        r = random.randint(0, len(openposlist) - 1)
        newbornpos = openposlist[r]

        agrec = ag.agent_record
        if self.debug > 2:
            print((agrec.resources, ag.resources))
        if agrec.resources != ag.resources:
            print "agent record resources does not equal agent resources "
            print((ag.agent_id, ag.resources, agrec.agent_id, agrec.resources))
            return None

        if ag.resources < costs:
            print((agrec.resources, ag.resources, costs))
            print "agent resources are less than actual costs"
            return None

        # we ca make the offsoping
        if self.initial_agent_type == "allC":
            newag = agentsC.AgentC(self)
        else:
            newag = agents.Agent(world)
        ag.num_offspring += 1  # we wabt nam t o be  p
        newag.agentCapabilitiesDict = capa

        #####
        # assign to an openspce
        #######
        newag.name = ag.name
        newagrec = AgentRecord(newag, newag.world)
        newag.agent_id = newagrec.agent_id
        newag.agent_record = newagrec
        newagrec.resources = end
        newag.resources = end
        ag.resources -= end
        agrec.resources -= end
        self.space.putAt(newag, newbornpos)
        if self.debug > 0:
            print "************************ created agrec aid >%s< for agid >%s< " % \
                (agrec.agent_id, newag.agent_id)
            print "offsp of %s  %s" % (ag.name, ag.agent_id)
        world.newborns.append(newag)

        if world.debug > 1:
            print "%d on newborns_" % (len(world.newborns))
        world.agent_records_dict[newag.agent_id] = agrec
        world.births += 1

        # mut each capb qith low prob
        num_mu_c0z = 0
        for k in newag.agentCapabilitiesDict.keys():
            if random.random() < self.prob_mut:
                if random.random() < 0.5:
                    mut = 1
                else:
                    mut = -1
                newag.agentCapabilitiesDict[k] += mut
                if newag.agentCapabilitiesDict[k] < 0:
                    newag.agentCapabilitiesDict[k] = random.randint(0, 4)

        # coun t mutation
        num_mu = 0
        for k in newag.agentCapabilitiesDict.keys():
            if ag.agentCapabilitiesDict[k] != newag.agentCapabilitiesDict[k]:
                num_mu += 1
        self.mutated += num_mu

    def printAllAgents(self, fmt):
        if fmt == 's':
            print(("Agent", "ID", "Alive?", "Resources", "Age"))
        elif fmt == 'm':
            print(("Agent", "ID", "Alive?", "Resources", "Age"))
        else:
            print(("Agent", "ID", "Alive?",
                  "Resources", "Arec resources", "Age"))

        for a in self.agent_list:
            a.printAgent(fmt, self.curT)

    def get_living_agents(self):
        '''
        Return only living agents.
        '''
        return [agent for agent in self.agent_list if agent.is_alive == True]

    def compute(self):
        '''
        the main dynamics each step
        add newborns
        shuffle the agent_list
        give eah agent a chance to step out
              move or play ; request newborn
        then the world checjs and cleabn out  the dead/
        cooletneewborns
        then print out stats
        '''
        if self.debug > 2:
            print (">>>Start step %d >>>" % (self.curT))

        # upgdate history books
        self.game_histories[self.curT] = []
        self.cur_game_history = self.game_histories[self.curT]

        if len(self.newborns) > 0:
            self.agent_list.extend(self.newborns)
            self.newborns = []

        # Shuffle agent order
        numpy.random.shuffle(self.agent_list)

        # the agent might ask to move or play
        for a in self.get_living_agents():
            self.firstThisStep = True  # rest thies fklag
            # Run the agent step
            agrec = a.agent_record
            a.step()

            # make paymebnts
            # print(( a, a.agent_record, type (agrec) ))
            amt = -(agrec.total_decrement_Per_Step)
            self.update_resources(a, amt)
            age = self.curT - agrec.time_born
            # print((2, self.curT,a, a.agent_id, a.is_alive, a.resources, age))
            # chech if a wantys ti rwewt a birh
            if a.check_if_want_birth():
                a.request_birth = True
            else:
                a.request_birth = False

        self.applyTheGrimReaper()

        for a in self.get_living_agents():
            if a.request_birth:
                a.tryBirth()

        if self.verbose > 3 or self.debug > 1:
            self.printAllAgents('m')
        elif self.verbose > 0 or self.debug > 0:
            self.printStepSummary()

    def update_resources(self, a, amt):
        '''
         amt is already pos or neg as need be
        '''
        a.resources += amt
        a.agent_record.resources += amt

    def check_agents_resources(self):
        for ag in self.agent_list:
            if ag.resources != ag.agent_record.resources:
                print "*** RESOURCE MISMATCH ===> ag %d res %.6f != agrec.res %.6f" % \
                    (ag.agent_id, ag.resources, ag.agent_record.resources)

    def requestMoveTo(self, agent, destPos):
        '''
        agnt wants to move; chech that
        dest_loc us open and withibn agents range'
        if so, move and return true; if noyt return false
        we will be  a little stingy with the deinition of distasnce
        they can travel and say they can go to all the celllls they can see eit
        an euqvent visionrannge, whixh means thet ca get to any cell
        in a /- distance around thei pos/

        '''
        agrange = agent.agentCapabilitiesDict["speed"]
        destrow = destPos.row
        destcol = destPos.col
        agrow = agent.position.row
        agcol = agent.position.col

        rowdist = abs(agrow - destrow)
        coldist = abs(agcol - destcol)

        retn = None  # ## for grec

        if rowdist > agrange or coldist > agrange:
            print "ag %s denied reque\st to to move--toofar" % (agent.agent_id)

        elif not self.space.isEmptyPosition(destPos):
            print "ag %s denied reque\st to to move--not openr" % (agent.agent_id)

        else:
            # ok to move
            self.totnumMove += 1
            if self.debug > 1:
                print "agent %s Chose to movdTo,,," % (agent.agent_id)

            # move,  create game rec and add to history
            self.space.moveTo(agent, agent.position, destPos)
            retn = destPos

        #     focal, action, rmv, omv, fresult , oresult, other ):
        grec = GameRecord(agent, World.move, retn, None, None, None, None)
        self.add_to_history(grec)

    def pickRandomOther(self, me):
        '''
        from all agents pickone at random, buut not me.
        '''
        if len(self.agent_list) < 2:
            print "cabnt rrun wit 1 or fewer adebnts"
            exit

        pick = me
        while pick == me:
            r = random.randrange(len(self.agent_list))
            pick = self.agent_list[r]
        return pick

    def requestPlayPD(self, requestor, other, focals_play):
        '''
        agent reqestor has picked an opponent and a play
         the world will ask that player fo a response, which is
         a) world.refuse
         b) world.cooperate
         c) world,defect

         the world then calcs who owes  or gains, tells both agbnts th results,
         uodates ita agentrecord, checks if either s dead;
         return GameRecord or None

    def __init__( self, focal, action, rmv, omv, fresult , oresult, other ):

         '''

        if self.debug > 1:
            print "agent %s Chose pd,,," % (requestor.agent_id)

        self.totnumofferpd += 1

        # check if other in range and alive'
        # Skip for now
        ineligible = False
        if ineligible:
            return None

        # Get opponents play
        others_play = other.choose_reply(requestor)

        if others_play == World.refuse:
            # update resources
            self.totnumrefuse += 1
            amt = self.refusal_cost
            self.update_resources(requestor, amt)
            self.update_resources(other, -amt)
            if self.debug > 1:
                print "agent %s Chose to refuse,,," % (other.agent_id)
            grec = GameRecord(requestor, World.pd, focals_play,
                              others_play, amt, -amt, other)

        else:
            # theyboth chose to play
            focals_payoff, others_payoff = self.playPD(
                focals_play, others_play)
            self.update_resources(requestor, focals_payoff)
            self.update_resources(other, others_payoff)
            if self.debug > 1:
                print ("PD: req  %s %d  pay %.2f  other  %s  %d pay %.2f ") % \
                    (requestor.agent_id, focals_play, focals_payoff,
                     other.agent_id, others_play, others_payoff)

            if focals_play == world.cooperate:
                self.totnumcoop += 1
            else:
                self.totnumdef += 1

            if others_play == world.cooperate:
                self.totnumcoop += 1
            else:
                self.totnumdef += 1

            # record the ganme
            grec = GameRecord(requestor, World.pd, focals_play,
                              others_play, focals_payoff,
                              others_payoff, other)

        # in either case record and return ptr to other
        self.add_to_history(grec)
        return other

    def add_to_history(self, grec):
        self.cur_game_history.append(grec)

    def applyTheGrimReaper(self):
        if self.debug > 0:
            print("++++++ applyThegrimReaper stp %d >>>" % (self.curT))

        '''
        Iterate over agents and remove any who have passed their
        or who have non-positive resources.
        '''
        for a in self.get_living_agents():  # .reverse():
            # Check if the agent has reached max lifetime
            # if self.curT  >=
            # self.agent_records_dict[a.agent_id].max_lifetime:
            if self.curT >= a.agent_record.max_lifetime:
                if self.debug > 0:
                    arec = a.agent_record
                    print(
                        "@@@@@@@@@@@@@2%s reached max age %d at max lifetime (curT) at %d." %
                        (a.agent_id, arec.max_age, arec.max_lifetime))
                # Set to dead
                a.is_alive = False
                self.totnumold += 1
                # remove from the space
                self.space.removeFromSpace(a, a.position)

            # Check if the agent has non-positive resources
            if a.resources <= 0:
                if self.debug > 0:
                    print("============>]>>>>> %s starved at %d." %
                          (a, self.curT))
                # Set to dead
                a.is_alive = False
                self.totnumstarved += 1
                self.space.removeFromSpace(a, a.position)

        for a in self.agent_list:
            if not a.is_alive:
                if random.random() < self.rebirth_prob:
                    a.resources = world.starting_resources
                    a.max_lifetime = self.max_lifetime
                else:
                    # renmove from akk lists an dicts
                    if world.debug > 1:
                        print "$$$$$$$$$$$$$$$$$$$$$  %s is being removed..." % (a)
                    # del self.agent_records_dict[ a.agent_id ]
                    # **RRR jey error
                    self.agent_list.remove(a)
                    if a.position is not None:
                        self.space.removeFromSpace(a, a.position)

################################################################
    def count_types(self):
        '''
        coujn t numer of speciers, feddefunred as agents wth sne nbhe
        'keep a dict, key is name
        '''
        tot_resources = 0
        tot = 0
        agent_amts_dict = {}
        agent_types_dict = {}
        for a in self.agent_list:
            name = a.name
            tot += 1
            tot_resources += a.resources
            if name in agent_types_dict:
                # we  tab going,,,]
                agent_types_dict[name] += 1
                agent_amts_dict[name] += a.resources
            else:
                agent_types_dict[name] = 1
                agent_amts_dict[name] = a.resources

        print " type  cnt   tot4type  avg/type"
        for a in self.agent_list:
            name = a.name
            if agent_types_dict[name] > 1:
                avg = agent_amts_dict[name] / float(agent_types_dict[name])
            else:
                avg = agent_amts_dict[name]
            print " %s   %d   %.3f  %.4f " % \
                (name, agent_types_dict[name],
                 agent_amts_dict[name], avg)

    def calcPopAvgTraits(self):

        self.popAvgVis = numpy.mean(
            [ag.agentCapabilitiesDict["vision"] for ag in self.agent_list])
        self.popAvgSpd = numpy.mean(
            [ag.agentCapabilitiesDict["speed"] for ag in self.agent_list])
        self.popAvgDis = numpy.mean(
            [ag.agentCapabilitiesDict["dispersal"] for ag in self.agent_list])

    def printPopAvgs(self):
        pop = len(self.agent_list)
        newb = len(self.newborns)
        if pop == 0:
            print "no living agents"
            return
        self.calcPopAvgTraits()
        print "====> step %d   pop %d  newb %d  Avg  vis %.3f  spd  %.3f  disp  %.3f" % \
            (self.curT, pop, newb, self.popAvgVis,
             self.popAvgSpd, self.popAvgDis)

    def printStepSummary(self):
        '''
        print s]ummary stats eg counts of each agent type

        '''
        if self.debug > 0:
            print ("  XS     +++ printStepSummary %d >>>" % (self.curT))

    def printActionCounts(self):
        print "%d totnumMove,%d totnumofferpd , %d totnumrefuse , %d totnumdef)" % \
            (self.totnumMove, self.totnumofferpd,
             self.totnumrefuse, self.totnumdef)

        print " %d totnumcoop %d totnumstarved  %d totnumold  %d births %d mutated" % \
            (self.totnumcoop, self.totnumstarved,
             self.totnumold, self.births, self.mutated)

    def printFinalStats(self):
        '''
        print  stats eg counts of each agent type

        '''
        if self.debug > 0:
            print ("       +++ printFinalStats %d >>>" % (self.curT))

        # stats
        self.printActionCounts()

    def testSpace(self):
        '''
        positiom are ns sare tuples

        get( pos)
        put( pos, oj
        get_neighbors_von_neumann
        get_neaighbors(pos, dist) )
        get_Moore-neighbors( pos , dist )
        '''
        self.space = Space(6, 6, "Moore")

    def chechAgentsInSpace(self):
        '''
        be s ure there cahced loction matches where thye reallly are
        '''
        err = 0
        for r in range(self.space.num_rows):
            for c in range(world.space.num_cols):
                pos = Position(r, c)
                if self.space.isOccupiedPosition(pos):
                    ag = self.space.getOccupant(pos)
                    if not self.space.checkLocationInSpace(ag, pos):
                        err += 1
        if err > 0:
            print "chechAgentsInSpace found errs."

    def saveDS(self):
#

        # p = pickle.Pickler ( self.saveFilename, 2 )
        # p.dump(self.game_histories)

        fh = open(self.saveFilename, 'wb')

        pickle.dump(self.game_histories, fh, -1)

        pickle.dump(self.agent_list, fh, -1)
        pickle.dump(self.agent_records_dict, fh, -1)
        pickle.dump(self.newborns, fh, -1)
        pickle.dump(self.game_histories, fh, -1)
        pickle.dump(self.space, fh, -1)
        fh.close()
        return

        '''
        pickle.dump(boolean, open("filename.pkl", "wb"))

        pickle.dump(self.game_histories, fh)
        # pickle.dump(
        '''
        print"pickling things  in '%s'" % (self.saveFilename)

# depreicated     def get_cost_of_offspring(self, resources, sight_value, distance_value):
        # '''
        # Get the cost of an offspring with a given set of resources.
        # '''
        # return resources + sight_value * self.per_sight_offspring_cost \
        #   + distance_value * self.per_distance_offspring_cost

    def __repr__(self):
        '''
        String representation
        '''
        return "World (player_pool={0})"\
            .format(len(self.agents))

#################################################################
# 333


######################################
# LOADING FUNCTIONS
######################################
def saveObject(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def loadObject(filename):
    m = None
    with open(filename, 'rb') as input:
        m = pickle.load(input)
        return m

# 3
# 3


if __name__ == "__main__":
    # print  str(sys.argv)  # for cmd line parameters

    # create world, which inits space, create agents agentrecords
    world = World(sys.argv[1:])
    if world.initial_agent_type == "allC":
        agentsC.world = world
    else:
        agents.world = world
    AgentRecord.world = world

    if world.debug > 0:
        print("\nThe players:")
        world.printAllAgents('f')

    while world.curT < world.stopT:
        if world.debug > 0:
            print " "
            print " "
            print "\n\n  ======================= start step %d ================\n" \
                % (world.curT)
        if world.debug > 3:
            world.printAllAgents('f')
            world.printActionCounts()
            world.count_types()

        world.compute()  # the top level step dynamics

        world.printPopAvgs()

        if len(world.agent_list) == 0:
            print " all agents dead"
            break
        world.printPopAvgs()
        world.check_agents_resources()
        world.curT += 1

    print("\nFinal scores:")
    world.printAllAgents('f')
    world.count_types()
    world.printActionCounts()

    if world.verbose > 1:
        world.space.displaySpace()

    world.chechAgentsInSpace()

    world.printPopAvgs()

    world.saveDS()

    print("All done.")
