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
  
  """
    - ajacent is List<Node>
    - cell is Cell
    - manhattan is Number
    - parent is Node
    - state is NodeState
  """
  def __init__(self, cell):
    self.cell = cell
    self._adjacent = []
    self._parent = None
    self._manhattan = None
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
    if other in self._adjacent:
      return
    self._adjacent.append(other)

  def isNeighbour(self, other):
    return other in self._adjacent

  def resetManhattan(self):
    self._manhattan = Node.infinite_manhattan

  def resetParent(self):
    self._parent = None

  def resetState(self):
    self._state = NodeState.WHITE

  def __eq__(self, other):
    if isinstance(other, Node):
      return self.cell.point == other.cell.point
    return False

  def __hash__(self, other):
    return hash(self.cell.point) + hash(self.cell.point)

class Edge:

  """
    - cost is Number
    - dst is Node
    - src is Node
  """
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

  def __str__(self):
    return "{} -> {}".format(str(self.src.cell.point), str(self.dst.cell.point))

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

  """
    - edges is List<Edge>
    - last_analyzed is Boolean
    - log is Logger
    - nodes is List<Node>
    - pq is PriorityNodes
    - solved is Boolean
    - start is Node
    - target is Node
  """
  def __init__(self, nodes, edges):
    self._log = Logger()
    self._nodes = nodes
    self._edges = edges
    self._last_analyzed = None
    self._solved = False
    self._start = None
    self._target = None
    self._pq = None
    self.resetAlgorithm()
    self._log.debug("Astar", "Init Object -- {} Nodes -- {} Edges".format(len(nodes), len(edges)))

  @property
  def last_analyzed(self):
    return self._last_analyzed

  @property
  def solved(self):
    return self._solved

  @property
  def start(self):
    return self._start

  @property
  def target(self):
    return self._target

  def nextIteration(self):
    current = self._pq.pop()
    self._last_analyzed = current
    
    if current.state == NodeState.TARGET:
      self._solved = True
      return
    
    if not current.state == NodeState.START:
      current.state = NodeState.BLACK
    
    for node in current.neighbours:
      if node.state == NodeState.BLACK:
        continue

      edge = self._edgeBy(current, node)

      if edge == None:
        self._log.info("Astar", "EXPECTED AN EDGE, BUT NONE WAS RETURNED")
        exit(1)

      left_to_target = self._target.cell.point.distance(node.cell.point)
      manhattan_value = current.manhattan + left_to_target + edge.cost

      if node.state == NodeState.WHITE or node.state == NodeState.TARGET:
        node.manhattan = manhattan_value
        node.parent = current
        node.state = NodeState.GRAY
        self._emplace(node.cell.point)  
      
      elif node.state == NodeState.GRAY or node.state == NodeState.TARGET:
        if node.manhattan > manhattan_value:
          node.manhattan = manhattan_value
          node.parent = current

      if self._target == node:
        self._solved = True
        return

  def nextIterationNeighbourPriority(self):
    current = self._pq.pop()
    if not self._last_analyzed == None:
      is_neighbour = current.isNeighbour(self._last_analyzed)
      if not is_neighbour or not self._last_analyzed.isNeighbour(current):
        return
    
    if current == None:
      self._target = None
      return
    
    self._last_analyzed = current
    
    if current.state == NodeState.TARGET:
      self._solved = True
      return
    
    if not current.state == NodeState.START:
      current.state = NodeState.BLACK
    
    for node in current.neighbours:
      if node.state == NodeState.BLACK:
        continue

      edge = self._edgeBy(current, node)

      if edge == None:
        self._log.info("Astar", "EXPECTED AN EDGE, BUT NONE WAS RETURNED")
        exit(1)

      left_to_target = self._target.cell.point.distance(node.cell.point)
      manhattan_value = current.manhattan + left_to_target + edge.cost

      if node.state == NodeState.WHITE or node.state == NodeState.TARGET:
        node.manhattan = manhattan_value
        node.parent = current
        node.state = NodeState.GRAY
        self._emplace(node.cell.point)  
      
      elif node.state == NodeState.GRAY or node.state == NodeState.TARGET:
        if node.manhattan > manhattan_value:
          node.manhattan = manhattan_value
          node.parent = current

      if self._target == node:
        self._solved = True
        return

  def noOptionsLeft(self):
    if not self._target == None:
      return self._pq.empty()
    return False

  def noSolution(self):
    return self._pq.empty()

  def resetLastAnalysed(self):
    self._last_analyzed = None

  def resetManhattan(self):
    for node in self._nodes:
      node.resetManhattan()

  def resetParents(self):
    for node in self._nodes:
      node.resetParent()

  def resetPriorityQueue(self):
    self._pq = PriorityNodes()
  
  def resetSolved(self):
    self._solved = False
  
  def resetStart(self):
    self._start = None
  
  def resetStates(self):
    for node in self._nodes:
      node.resetState()

  def resetTarget(self):
    self._target = None

  def resetAlgorithm(self):
    self.resetSolved()
    self.resetStates()
    self.resetManhattan()
    self.resetPriorityQueue()
    self.resetParents()
    self.resetStart()
    self.resetTarget()
    self.resetLastAnalysed()

  def updateNodeToStateStartBy(self, cell):
    self._updateStateOf(cell.point, NodeState.START)
    self._updateManhattanOf(cell.point, 0)
    self._emplace(cell.point)
    self._start = self._nodeByCoordinate(cell.point)

  def updateNodeToStateTargetBy(self, cell):
    self._updateStateOf(cell.point, NodeState.TARGET)
    self._target = self._nodeByCoordinate(cell.point)

  def _edgeBy(self, node, neighbour):
    for edge in self._edges:
      if edge.src.cell.point == node.cell.point and edge.dst.cell.point == neighbour.cell.point:
        # self._log.debug("Astar", "Returning the edge {}".format(str(edge)))
        return edge
      if edge.dst.cell.point == node.cell.point and edge.src.cell.point == neighbour.cell.point:
        # self._log.debug("Astar", "Returning the edge {}".format(str(edge)))
        return edge
    return None
  
  def _emplace(self, coord):
    node = self._nodeByCoordinate(coord)
    self._pq.insert(node)
  
  def _nodeByCoordinate(self, coord):
    for node in self._nodes:
      if node.cell.point == coord:
        return node
    return None

  def _updateManhattanOf(self, coord, val):
    current = self._nodeByCoordinate(coord)
    current.manhattan = val
  
  def _updateStateOf(self, coord, val):
    node = self._nodeByCoordinate(coord)
    node.state = val