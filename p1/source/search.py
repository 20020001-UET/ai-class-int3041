# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    # import Stack
    from util import Stack

    # initialize
    checker = []
    stack = Stack()

    # push the start state in to stack
    stack.push((problem.getStartState(), []))

    # DFS:
    while not(stack.isEmpty()):
	# pop out the *deepest node* and the action to get there
	startState, startAction = stack.pop()
	# set the checker that this state has been visited
	checker.append(startState)

	# goal state checking
	if problem.isGoalState(startState):
	    return startAction

	# get all the node that can be expanded
	successors = problem.getSuccessors(startState)

	"""
	optional - reverse the order of successors:

	successors.reverse()
	"""

	# find the new node to expand
	for nextState, action, cost in successors:
	    if nextState not in checker:
		# make the new action
		nextAction = startAction[:]
		nextAction.append(action)

		# push the new expanded node
		stack.push((nextState, nextAction))

    # return false
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # import Queue
    from util import Queue

    # initialize
    checker = []
    queue = Queue()

    # push the start state in to stack and the checker
    queue.push((problem.getStartState(), []))
    checker.append(problem.getStartState())

    # BFS:
    while not(queue.isEmpty()):
	# pop out the *deepest node* and the action to get there
	startState, startAction = queue.pop()

	# goal state checking
	if problem.isGoalState(startState):
	    return startAction

	# get all the node that can be expanded
	successors = problem.getSuccessors(startState)

	"""
	optional - reverse the order of successors:

	successors.reverse()
	"""

	# find the new node to expand
	for nextState, action, cost in successors:
	    if not(nextState in checker):
		# make the new action
		nextAction = startAction[:]
		nextAction.append(action)

		# push the new expanded node
		queue.push((nextState, nextAction))
		checker.append(nextState)

    # return false
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # import Priority Queue
    from util import PriorityQueueWithFunction

    # initialize
    checker = []
    getAction = {}
    getCost = {}

    def keyValue(element):
	return getCost[element]

    queue = PriorityQueueWithFunction(keyValue)

    # push the start state in to stack and the checker
    getAction[problem.getStartState()] = []
    getCost[problem.getStartState()] = 0
    queue.push(problem.getStartState())
    checker.append(problem.getStartState())

    # UCS:
    while not(queue.isEmpty()):
	# pop out the *deepest node* and the action to get there
	startState = queue.pop()

	# goal state checking
	if problem.isGoalState(startState):
	    return getAction[startState]

	# get all the node that can be expanded
	successors = problem.getSuccessors(startState)

	"""
	optional - reverse the order of successors:

	successors.reverse()
	"""

	# find the new node to expand
	for nextState, action, cost in successors:
	    # make the new action
	    nextAction = getAction[startState][:]
	    nextAction.append(action)

	    nextCost = getCost[startState] + cost

	    if not(nextState in checker):
		getAction[nextState] = nextAction
		getCost[nextState] = nextCost

		# push the new expanded node
		queue.push(nextState)
		checker.append(nextState)

	    else:
		if getCost[nextState] > nextCost:
		    getAction[nextState] = nextAction
		    getCost[nextState] = nextCost

    # return false
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # import Priority Queue
    from util import PriorityQueueWithFunction

    # initialize
    checker = []
    getAction = {}
    getCost = {}

    def keyValue(element):
	return getCost[element] + heuristic(element, problem)

    queue = PriorityQueueWithFunction(keyValue)

    # push the start state in to stack and the checker
    getAction[problem.getStartState()] = []
    getCost[problem.getStartState()] = 0
    queue.push(problem.getStartState())
    checker.append(problem.getStartState())

    # A-Star:
    while not(queue.isEmpty()):
	# pop out the *deepest node* and the action to get there
        startState = queue.pop()

	# goal state checking
	if problem.isGoalState(startState):
	    return getAction[startState]

	# get all the node that can be expanded
	successors = problem.getSuccessors(startState)

	"""
	optional - reverse the order of successors:

	successors.reverse()
	"""

	# find the new node to expand
	for nextState, action, cost in successors:
	    # make the new action
	    nextAction = getAction[startState][:]
	    nextAction.append(action)

	    nextCost = getCost[startState] + cost

	    if not(nextState in checker):
		getAction[nextState] = nextAction
		getCost[nextState] = nextCost

		# push the new expanded node
		queue.push(nextState)
		checker.append(nextState)

            else:
		if getCost[nextState] > nextCost:
		    getAction[nextState] = nextAction
		    getCost[nextState] = nextCost

                    queue.push(nextState)



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
