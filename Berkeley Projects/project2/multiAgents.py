# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #get distances between remaining food positions and new position of pacman
        food_list = newFood.asList()    #food coordinates in a list
        food_distances = []
        for food_position in food_list: #append manhattan distances in a list
            food_distances.append(manhattanDistance(newPos,food_position))
        
        #get distances between new ghost positions and new position of pacman
        ghost_list = newGhostStates
        ghost_positions = []
        for ghost in ghost_list:    #get the positions of ghosts
            ghost_positions.append(ghost.getPosition())
        ghost_distances = []
        for ghost_position in ghost_positions:  #append manhattan distances in a list
            ghost_distances.append(manhattanDistance(newPos,ghost_position))

        evaluation = 0
        if (successorGameState.isWin()):  #if no more food-win
            return 99999
        
        #if there is still food left-follow it and gain points
        evaluation += 1/min(food_distances)

        if (min(ghost_distances) == 1):    #if ghost gets too close
            evaluation -= min(ghost_distances)  #lose points - stay away
              
        return successorGameState.getScore() + evaluation 

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        return self.Minimax(gameState)
        util.raiseNotDefined()

    def Minimax(self,state,agent=0,depth=0):
        #depth refresh
        if (agent==state.getNumAgents()):   #if last ghost (agent 'num_agents-1') is done,
            agent=0                         #it's pacman's (agent '0') turn
            depth+=1                        #and a single search ply is done
        #base case
        if (state.isWin() or state.isLose() or depth==self.depth):  #win/lose state or leaf
            return self.evaluationFunction(state)   
        #pacman
        if (agent==0): 
            score = -float('inf')
            #for every legal action of pacman
            for action in state.getLegalActions(agent):
                previous = score
                #compute the maximum value between the ghost states-values
                score = max(score,self.Minimax((state.generateSuccessor(agent,action)),agent+1,depth))
                if (score>previous):    #keep the action towards the maximum value
                    root_action = action
            if (depth==0):              #and if the action comes from root,
                return root_action      #return it
            return score                #or return the value
        #ghosts
        else:
            score = float('inf')
            #for every legal action of ghost
            for action in state.getLegalActions(agent):
                #compute the minimum value between the pacman states-values
                score = min(score,self.Minimax((state.generateSuccessor(agent,action)),agent+1,depth))
            return score

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.AlphaBeta(gameState)
        util.raiseNotDefined()

    def AlphaBeta(self,state,agent=0,depth=0,a=-float('inf'),b=float('inf')):
        #depth refresh
        if (agent==state.getNumAgents()):
            agent=0
            depth+=1
        #base case
        if (state.isWin() or state.isLose() or depth==self.depth):
            return self.evaluationFunction(state)   
        #pacman
        if (agent==0): 
            score = -float('inf')
            for action in state.getLegalActions(agent):
                previous = score
                score = max(score,self.AlphaBeta((state.generateSuccessor(agent,action)),agent+1,depth,a,b))
                #if score becomes greater than beta, MIN will avoid it, so break-prune
                if (score>b):
                    break
                a=max(a,score) #alpha has the best score that has been found along the path   
                if (score>previous):
                    root_action = action
            if (depth==0):
                return root_action
            return score
        #ghosts
        else:
            score = float('inf')
            for action in state.getLegalActions(agent):
                score = min(score,self.AlphaBeta((state.generateSuccessor(agent,action)),agent+1,depth,a,b))
                #if score becomes less than alpha, MAX will avoid it, so break-prune
                if (score<a):
                    break
                b=min(b,score)  #beta has the worst score that has been found along the path    
            return score

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        return self.Expectimax(gameState)
        util.raiseNotDefined()

    def Expectimax(self,state,agent=0,depth=0):
        #depth refresh
        if (agent==state.getNumAgents()):
            agent=0
            depth+=1
        #base case
        if (state.isWin() or state.isLose() or depth==self.depth):
            return self.evaluationFunction(state)   
        #pacman
        if (agent==0): 
            score = -float('inf')
            for action in state.getLegalActions(agent):
                previous = score
                score = max(score,self.Expectimax((state.generateSuccessor(agent,action)),agent+1,depth))
                if (score>previous):
                    root_action = action
            if (depth==0):
                return root_action
            return score
        #ghosts
        else:
            probability = 1.0/len(state.getLegalActions(agent)) #same probability for every child-node
            score = 0
            for action in state.getLegalActions(agent):
                #value of the chance node is probability*score_of_child1+probability*score_of_child2...
                score+=probability*self.Expectimax((state.generateSuccessor(agent,action)),agent+1,depth)
            return score

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <readme>
    """
    "*** YOUR CODE HERE ***"
    
    # Useful information extracted from a GameState (pacman.py)
    pac_pos = currentGameState.getPacmanPosition()
    food_list = currentGameState.getFood().asList()
    ghost_states = currentGameState.getGhostStates()

    #get distances between remaining food positions and position of pacman
    food_distances = []
    for food_position in food_list: #append manhattan distances in a list
        food_distances.append(manhattanDistance(pac_pos,food_position))
    
    #get distances between ghost positions and position of pacman
    ghost_list = ghost_states
    ghost_positions = []
    for ghost in ghost_list:    #get the positions of ghosts
        ghost_positions.append(ghost.getPosition())
    ghost_distances = []
    for ghost_position in ghost_positions:  #append manhattan distances in a list
        ghost_distances.append(manhattanDistance(pac_pos,ghost_position))

    evaluation = 0
    if (currentGameState.isWin()):  #if no more food-win
        return 99999
        
        # #if there is still food left-follow it and gain points
    evaluation += 1/min(food_distances)

    if (min(ghost_distances) == 1):    #if ghost gets too close
        evaluation -= min(ghost_distances)  #lose points - stay away
              
    return currentGameState.getScore() + evaluation
    util.raiseNotDefined()
    
# Abbreviation
better = betterEvaluationFunction
