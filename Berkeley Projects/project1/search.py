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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    root_node = problem.getStartState() #initial state/root node
    fringe = util.Stack()   #stack is needed for dfs
    visited = set() #a set to keep visited nodes - avoiding cycles - better complexity
    fringe.push((root_node, [])) #push tuple of initial state and action - no need to push cost

    while fringe.isEmpty()==False:  #while there are nodes in the stack
        (node, past_actions) = fringe.pop() #pop the node with the highest priority
        if node not in visited: #set node = visited, if not already
            visited.add(node)
            if problem.isGoalState(node):   #check if the node is a valid goal state
                return past_actions #and return the actions to get to that node
            for child in problem.getSuccessors(node):   #get the children of node
                if child[0] not in visited: #and if they have not been visited yet,
                    fringe.push((child[0], past_actions + [child[1]]))  #push them in stack
                    #as stated in getSuccessors function 'successor is child[0]' and 'action is child[1]'

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    root_node = problem.getStartState()
    fringe = util.Queue()   #queue is needed for bfs
    visited = set()
    fringe.push((root_node, [])) #push tuple of initial state and action - no need to push cost

    while fringe.isEmpty()==False:  #same code as dfs
        (node, past_actions) = fringe.pop()
        if node not in visited:
            visited.add(node)
            if problem.isGoalState(node):
                return past_actions
            for child in problem.getSuccessors(node):
                if child[0] not in visited:
                    fringe.push((child[0], past_actions + [child[1]]))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    root_node = problem.getStartState()
    fringe = util.PriorityQueue()   #priorityqueue is needed for ucs
    visited = set()
    fringe.push((root_node, [], 0),0) #push tuple of initial state, action, cost and the priority-cost
    #in ucs we use the cost from initial to current state + current state's cost
    while fringe.isEmpty()==False:
        (node, past_actions, total_cost) = fringe.pop()
        if node not in visited:
            visited.add(node)
            if problem.isGoalState(node):
                return past_actions
            for child in problem.getSuccessors(node):
                if child[0] not in visited:
                    #push like dfs-bfs, but also push 'total_cost+current_cost' (child[2] is stepCost),
                    #as 3rd element of tuple and as the priority element
                    fringe.push((child[0], past_actions + [child[1]], total_cost + child[2]),total_cost + child[2])

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    root_node = problem.getStartState()
    fringe = util.PriorityQueue()   #priorityqueue is needed for A*
    visited = set()
    fringe.push((root_node, [], 0),0+heuristic(root_node,problem)) #priority now is cost plus the heuristic function

    while fringe.isEmpty()==False:
        (node, past_actions, total_cost) = fringe.pop()
        if node not in visited:
            visited.add(node)
            if problem.isGoalState(node):
                return past_actions
            for child in problem.getSuccessors(node):
                if child[0] not in visited:
                    #push like ucs, but also push the heuristic function in the cost-sum of priority
                    fringe.push((child[0], past_actions + [child[1]], total_cost + child[2]),total_cost + child[2] + 
                    heuristic(child[0],problem))

    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
