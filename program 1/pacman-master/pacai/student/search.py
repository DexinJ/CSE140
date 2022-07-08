"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""
from pacai.util.stack import Stack
from pacai.util.queue import Queue
from pacai.util.priorityQueue import PriorityQueue
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """
    # *** Your Code Here ***
    # initializing variable and states
    fringes = Stack()
    path = []
    history = []
    pathMap = {}
    previousState = None
    move = None
    start = problem.startingState()
    fringes.push((start, move, previousState, move))
    # depth first search
    while not fringes.isEmpty():
        child, move, previousState, previousMove = fringes.pop()
        if child not in history:
            history.append(child)
            pathMap[(child, move)] = (previousState, previousMove)
            if problem.isGoal(child):
                path.append(move)
                while previousState is not None:
                    path.insert(0, previousMove)
                    previousState, previousMove = pathMap[(previousState, previousMove)]
                path.pop(0)
                return path
            for s in problem.successorStates(child):
                if s[0] not in history:
                    fringes.push((s[0], s[1], child, move))
    return []

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """
    # *** Your Code Here ***
    fringes = Queue()
    path = []
    history = []
    pathMap = {}
    previousState = None
    move = None
    start = problem.startingState()
    fringes.push((start, move, previousState, move))
    while not fringes.isEmpty():
        child, move, previousState, previousMove = fringes.pop()
        if child not in history:
            history.append(child)
            pathMap[(child, move)] = (previousState, previousMove)
            if problem.isGoal(child):
                path.append(move)
                while previousState is not None:
                    path.insert(0, previousMove)
                    previousState, previousMove = pathMap[(previousState, previousMove)]
                path.pop(0)
                return path
            for s in problem.successorStates(child):
                if s[0] not in history:
                    fringes.push((s[0], s[1], child, move))
    return []

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    # *** Your Code Here ***
    fringes = PriorityQueue()
    path = []
    history = []
    pathMap = {}
    previousState = None
    move = None
    start = problem.startingState()
    fringes.push((start, move, 0, previousState, move), 0)
    while not fringes.isEmpty():
        child, move, cost, previousState, previousMove = fringes.pop()
        if child not in history:
            history.append(child)
            pathMap[(child, move)] = (previousState, previousMove)
            if problem.isGoal(child):
                path.append(move)
                while previousState is not None:
                    path.insert(0, previousMove)
                    previousState, previousMove = pathMap[(previousState, previousMove)]
                path.pop(0)
                return path
            for s in problem.successorStates(child):
                if s[0] not in history:
                    fringes.push((s[0], s[1], s[2] + cost, child, move), s[2] + cost)
    return []

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # *** Your Code Here ***
    fringes = PriorityQueue()
    path = []
    history = []
    pathMap = {}
    previousState = None
    move = None
    start = problem.startingState()
    fringes.push((start, move, 0, previousState, move), 0)
    while not fringes.isEmpty():
        child, move, cost, previousState, previousMove = fringes.pop()
        if child not in history:
            history.append(child)
            pathMap[(child, move)] = (previousState, previousMove)
            if problem.isGoal(child):
                path.append(move)
                while previousState is not None:
                    path.insert(0, previousMove)
                    previousState, previousMove = pathMap[(previousState, previousMove)]
                path.pop(0)
                return path
            for s in problem.successorStates(child):
                if s[0] not in history:
                    h = heuristic(s[0], problem)
                    fringes.push((s[0], s[1], s[2] + cost, child, move), s[2] + cost + h)
    return []
