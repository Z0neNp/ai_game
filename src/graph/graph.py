from enum import Enum

from src.logger.logger import Logger

class NodeState(Enum):
  START = 0
  TARGET = 1
  GRAY = 2
  BLACK = 3
  WHITE = 4

class Node:
  infinite_manhattan = 100000
  
  def __init__(self, cell):
    self.cell = cell
    self._adjacent = []
    self.resetParent()
    self.resetManhattan()
    self.resetState()

  @property
  def cell(self):
    return self._cell

  @property
  def manhattan(self):
    return self._manhattan
  
  @property
  def neighbours(self):
    return self._adjacent
  
  @property
  def parent(self):
    return self._parent

  @property
  def state(self):
    return self._state

  @cell.setter
  def cell(self, val):
    self._cell = val

  @manhattan.setter
  def manhattan(self, val):
    self._manhattan = val

  @parent.setter
  def parent(self, val):
    self._parent = val

  @state.setter
  def state(self, val):
    self._state = val

  def addNeighbour(self, other):
    if other in self.neighbours:
      return
    self.neighbours.append(other)

  def resetManhattan(self):
    self.manhattan = Node.infinite_manhattan

  def resetParent(self):
    self.parent = None

  def resetState(self):
    self.state = NodeState.WHITE

  def __eq__(self, other):
    if isinstance(other, Node):
      return self.cell.point == other.cell.point
    return False

  def __hash__(self, other):
    return hash(self.cell.point) + hash(self.cell.point)

class Edge:

  def __init__(self, src, dst, cost):
    self.src = src
    self.dst = dst
    self.cost = cost

  @property
  def cost(self):
    return self._cost
  
  @property
  def dst(self):
    return self._dst
  
  @property
  def src(self):
    return self._src

  @cost.setter
  def cost(self, val):
    self._cost = val

  @dst.setter
  def dst(self, val):
    self._dst = val

  @src.setter
  def src(self, val):
    self._src = val

class PriorityNodes:

  def __init__(self):
    self._entries = []

  def empty(self):
    return len(self._entries) == 0

  def insert(self, node):
    self._entries.append(node)

  def pop(self):
    self._entries.sort(key=lambda node: node.manhattan, reverse=True)
    removed = self._entries.pop()
    return removed


class Astar():

  def __init__(self, nodes, edges):
    self._log = Logger()
    self.nodes = nodes
    self.edges = edges
    self.resetManhattan()
    self.resetPriorityQueue()
    self.resetSolved()
    self.resetStates()
    self.resetTarget()
    self._log.debug("Astar", "Init Object -- {} Nodes -- {} Edges".format(len(nodes), len(edges)))

  @property
  def edges(self):
    return self._edges

  @property
  def nodes(self):
    return self._nodes

  @property
  def pq(self):
    return self._pq

  @property
  def solved(self):
    return self._solved

  @property
  def target(self):
    return self._target

  @edges.setter
  def edges(self, val):
    self._edges = val

  @nodes.setter
  def nodes(self, val):
    self._nodes = val

  @solved.setter
  def solved(self, val):
    self._solved = val

  @target.setter
  def target(self, val):
    self._target = val

  def edgeBy(self, node, neighbour):
    for edge in self.edges:
      if edge.src == node and edge.dst == neighbour:
        return edge
    return None

  def emplace(self, coord):
    target = self.nodeByCoordinate(coord)
    self.pq.insert(target)

  def nextIteration(self):
    current = self.pq.pop()
    
    if current.state == NodeState.TARGET:
      self.solved = True
      return
    
    if not current.state == NodeState.START:
      current.state = NodeState.BLACK
    
    for node in current.neighbours:
      if node.state == NodeState.BLACK:
        continue

      edge = self.edgeBy(current, node)

      if edge == None:
        self._log.info("Astar", "EXPECTED AN EDGE, BUT NONE WAS RETURNED")
        exit(1)

      left_to_target = self.target.cell.point.distance(node.cell.point)
      manhattan_value = current.manhattan + left_to_target + edge.cost

      if node.state == NodeState.WHITE:
        node.manhattan = manhattan_value
        node.parent = current
        node.state = NodeState.GRAY
        self.emplace(node.cell.point)  
      
      elif node.state == NodeState.GRAY:
        if node.manhattan > manhattan_value:
          node.manhattan = manhattan_value
          node.parent = current

      if self.target == node:
        self.solved = True
        return

  def nodeByCoordinate(self, coord):
    for node in self.nodes:
      if node.cell.point == coord:
        return node
    return None

  def noSolution(self):
    return self.pq.empty()

  def resetManhattan(self):
    for node in self.nodes:
      node.resetManhattan()

  def resetParents(self):
    for node in self.nodes:
      node.resetParent()

  def resetPriorityQueue(self):
    self._pq = PriorityNodes()
  
  def resetSolved(self):
    self._solved = False
  
  def resetStates(self):
    for node in self.nodes:
      node.resetState()

  def resetTarget(self):
    self.target = None

  def updateManhattanOf(self, coord, val):
    current = self.nodeByCoordinate(coord)
    current.manhattan = val

  def updateStateOf(self, coord, val):
    current = self.nodeByCoordinate(coord)
    current.state = val