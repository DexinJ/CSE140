"""
This file contains incomplete versions of some agents that can be selected to control Pacman.
You will complete their implementations.

Good luck and happy searching!
"""

import logging

from pacai.core.actions import Actions
from pacai.core.directions import Directions
from pacai.core.search.position import PositionSearchProblem
from pacai.core.search.problem import SearchProblem
from pacai.agents.base import BaseAgent
from pacai.agents.search.base import SearchAgent
from pacai.core import distance
from pacai.student import search

DEFAULT_COST_FUNCTION = lambda x: 1

class CornersProblem(SearchProblem):
    def __init__(self, startingGameState):
        super().__init__()

        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top = self.walls.getHeight() - 2
        right = self.walls.getWidth() - 2
        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                logging.warning('Warning: no food in corner ' + str(corner))

        # *** Your Code Here ***
        self.costfn = DEFAULT_COST_FUNCTION

    def startingState(self):
        return (self.startingPosition, (False, False, False, False))

    def isGoal(self, state):
        a, b, c, d = state[1]
        if a and b and c and d:
            self._visitedLocations.add(state)
            coordinates = state[0]
            self._visitHistory.append(coordinates)
        return a and b and c and d

    def successorStates(self, state):
        successors = []
        for action in Directions.CARDINAL:
            x, y = state[0]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if (not self.walls[nextx][nexty]):
                corn = list(state[1])
                if (nextx, nexty) in self.corners:
                    for i in range(4):
                        if (nextx, nexty) == self.corners[i]:
                            corn[i] = True
                nextState = ((nextx, nexty), tuple(corn))
                cost = self.costfn(nextState)
                successors.append((nextState, action, cost))
        # Bookkeeping for display purposes (the highlight in the GUI).
        self._numExpanded += 1
        if (state not in self._visitedLocations):
            self._visitedLocations.add(state)
            # Note: visit history requires coordinates not states. In this situation
            # they are equivalent.
            coordinates = state[0]
            self._visitHistory.append(coordinates)
        return successors

    def actionsCost(self, actions):
        if (actions is None):
            return 999999

        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999

        return len(actions)

def cornersHeuristic(state, problem):
    # Useful information.
    # corners = problem.corners  # These are the corner coordinates
    # walls = problem.walls  # These are the walls of the maze, as a Grid.

    # *** Your Code Here ***
    pos = state[0]
    minDis = 999999
    minCorner = ()
    heu = 0
    visitHistory = list(state[1])
    neededCorners = []
    for i in range(4):
        if not visitHistory[i]:
            neededCorners.append(problem.corners[i])
    while neededCorners:
        for corner in neededCorners:
            dist = distance.manhattan(pos, corner)
            if dist < minDis:
                minDis = dist
                minCorner = corner
        neededCorners.remove(minCorner)
        pos = minCorner
        heu = heu + minDis
        minDis = 999999
    return heu  # Default to trivial solution

def foodHeuristic(state, problem):
    position, foodGrid = state
    foodList = foodGrid.asList()
    # print (problem)
    # *** Your Code Here ***
    heu = 0
    maxPath = 0
    for food in foodList:
        pLength = distance.maze(position, food, problem.startingGameState)
        if pLength > maxPath:
            maxPath = pLength
    heu = maxPath
    return heu  # Default to the null heuristic.

class ClosestDotSearchAgent(SearchAgent):
    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def registerInitialState(self, state):
        self._actions = []
        self._actionIndex = 0

        currentState = state

        while (currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState)  # The missing piece
            self._actions += nextPathSegment

            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' %
                            (str(action), str(currentState)))

                currentState = currentState.generateSuccessor(0, action)

        logging.info('Path found with cost %d.' % len(self._actions))

    def findPathToClosestDot(self, gameState):
        # Here are some useful elements of the startState
        # startPosition = gameState.getPacmanPosition()
        # food = gameState.getFood()
        # walls = gameState.getWalls()
        # problem = AnyFoodSearchProblem(gameState)

        # *** Your Code Here ***
        problem = AnyFoodSearchProblem(gameState)

        return search.uniformCostSearch(problem)

class AnyFoodSearchProblem(PositionSearchProblem):
    def __init__(self, gameState, start = None):
        super().__init__(gameState, goal = None, start = start)

        # Store the food for later reference.
        self.food = gameState.getFood()

    def isGoal(self, state):
        return state in self.food.asList()

class ApproximateSearchAgent(BaseAgent):
    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
