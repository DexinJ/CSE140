import random
from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core import distance
from pacai.core.directions import Directions

class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Useful information you can extract.
        # newPosition = successorGameState.getPacmanPosition()
        # oldFood = currentGameState.getFood()
        # newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***
        newPosition = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood().asList()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]
        score = 0
        maxDist = 0
        minDist = 999999
        ghostPosition = []
        for ghostState in newGhostStates:
            a = ghostState.getPosition()
            ghostPosition.append((a[0], a[1]))
            ghostPosition.append((a[0], a[1] + 1))
            ghostPosition.append((a[0], a[1] - 1))
            ghostPosition.append((a[0] + 1, a[1]))
            ghostPosition.append((a[0] - 1, a[1]))
        if newFood:
            for food in newFood:
                dist = distance.manhattan(newPosition, food)
                if dist > maxDist:
                    maxDist = dist
                if dist < minDist:
                    minDist = dist
            score -= minDist * maxDist
        if len(newFood) < len(oldFood):
            score = 0
        if newPosition == currentGameState.getPacmanPosition():
            score -= 100
        if newPosition in ghostPosition:
            score -= 1000
        if not newFood:
            score = 1000
        return score

class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):

        # Collect legal moves.
        # legalMoves = gameState.getLegalActions()
        # Choose one of the best actions.
        (_, move) = self.maxValue(gameState, self._treeDepth)

        return move

    def maxValue(self, gameState, depth):
        if gameState.isOver() or depth <= 0:
            return (self.getEvaluationFunction()(gameState), Directions.STOP)
        value = -999999
        legalMoves = gameState.getLegalActions(0)
        for action in legalMoves:
            if not action == 'Stop':
                value2, _ = self.minValue(gameState.generateSuccessor(0, action), depth - 1, 1)
                if value2 > value:
                    value, move = value2, action
        return (value, move)

    def minValue(self, gameState, depth, agent):
        if gameState.isOver():
            return (self.getEvaluationFunction()(gameState), Directions.STOP)
        value = 999999
        agentN = self.getNextAgent(gameState, agent)
        legalMoves = gameState.getLegalActions(agent)
        for action in legalMoves:
            if agentN == 0:
                value2, _ = self.maxValue(gameState.generateSuccessor(agent, action), depth)
            else:
                value2, _ = self.minValue(gameState.generateSuccessor(agent, action), depth, agentN)
            if value2 < value:
                value, move = value2, action
        return (value, move)

    def getNextAgent(self, gameState, agentNum):
        agent = agentNum + 1
        if agent >= gameState.getNumAgents():
            agent = 0
        return agent

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):

        # Collect legal moves.
        # legalMoves = gameState.getLegalActions()
        # Choose one of the best actions.
        (_, move) = self.maxValue(gameState, self._treeDepth, -999999, 999999)

        return move

    def maxValue(self, gameState, depth, a, b):
        if gameState.isOver() or depth <= 0:
            return (self.getEvaluationFunction()(gameState), Directions.STOP)
        value = -999999
        legalMoves = gameState.getLegalActions(0)
        for action in legalMoves:
            if not action == 'Stop':
                newState = gameState.generateSuccessor(0, action)
                value2, _ = self.minValue(newState, depth - 1, 1, a, b)
                if value2 > value:
                    value, move = value2, action
                    a = max(a, value)
                if value >= b:
                    return (value, move)
        return (value, move)

    def minValue(self, gameState, depth, agent, a, b):
        if gameState.isOver():
            return (self.getEvaluationFunction()(gameState), Directions.STOP)
        value = 999999
        agentN = self.getNextAgent(gameState, agent)
        legalMoves = gameState.getLegalActions(agent)
        for action in legalMoves:
            newState = gameState.generateSuccessor(agent, action)
            if agentN == 0:
                value2, _ = self.maxValue(newState, depth, a, b)
            else:
                value2, _ = self.minValue(newState, depth, agentN, a, b)
            if value2 < value:
                value, move = value2, action
                b = min(b, value)
            if value <= a:
                return (value, move)
        return (value, move)

    def getNextAgent(self, gameState, agentNum):
        agent = agentNum + 1
        if agent >= gameState.getNumAgents():
            agent = 0
        return agent

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):

        # Collect legal moves.
        # legalMoves = gameState.getLegalActions()
        # Choose one of the best actions.
        (_, move) = self.maxValue(gameState, self._treeDepth)

        return move

    def maxValue(self, gameState, depth):
        if gameState.isOver() or depth <= 0:
            return (self.getEvaluationFunction()(gameState), Directions.STOP)
        value = -999999
        legalMoves = gameState.getLegalActions(0)
        for action in legalMoves:
            if not action == 'Stop':
                value2, _ = self.minValue(gameState.generateSuccessor(0, action), depth - 1, 1)
                if value2 > value:
                    value, move = value2, action
        return (value, move)

    def minValue(self, gameState, depth, agent):
        if gameState.isOver():
            return (self.getEvaluationFunction()(gameState), Directions.STOP)
        valueSum = 0
        agentN = self.getNextAgent(gameState, agent)
        legalMoves = gameState.getLegalActions(agent)
        for action in legalMoves:
            if agentN == 0:
                value2, _ = self.maxValue(gameState.generateSuccessor(agent, action), depth)
            else:
                value2, _ = self.minValue(gameState.generateSuccessor(agent, action), depth, agentN)
            valueSum += value2
        value = valueSum / len(legalMoves)
        move = ""
        return (value, move)

    def getNextAgent(self, gameState, agentNum):
        agent = agentNum + 1
        if agent >= gameState.getNumAgents():
            agent = 0
        return agent

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """

    Position = currentGameState.getPacmanPosition()
    Foods = currentGameState.getFood().asList()
    GhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.getScaredTimer() for ghostState in GhostStates]
    score = 0
    maxDist = 0
    minDist = 999999
    ghostPosition = []
    for ghostState in GhostStates:
        a = ghostState.getPosition()
        ghostPosition.append((a[0], a[1]))
        ghostPosition.append((a[0], a[1] + 1))
        ghostPosition.append((a[0], a[1] - 1))
        ghostPosition.append((a[0] + 1, a[1]))
        ghostPosition.append((a[0] - 1, a[1]))
    if Foods:
        for food in Foods:
            dist = distance.manhattan(Position, food)
            if dist > maxDist:
                maxDist = dist
            if dist < minDist:
                minDist = dist
        score -= minDist + maxDist
    if Position in ghostPosition and not newScaredTimes:
        score -= 100
    return currentGameState.getScore() + score

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
