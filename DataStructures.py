from math import floor
from CS312Graph import *

class PQueueArray:
  #idIncrement aka num to add to the ids (0 => the real index, 1=> offset by 1 like the GUI)
  #dict pathDict {CS312GraphNode node : [int distance, CS312GraphNode prevNode]}
  #set CS312GraphNode visitedNodes
  def __init__(self, list=None, sourceId=None):
    self._idIncrement = 1
    self.pathDict = dict()
    self.visitedNodes = set()

    if list is not None:
      self.make_queue(list, sourceId)

  # Set up dictionary of nodes, with max len distances
  def make_queue(self, list, sourceId=None):
    for i in range(len(list)):
      if isinstance(list[i], CS312GraphNode):
        # Put the keys in the dictionary, with null distance and prevNode
        if (list[i].node_id == sourceId):
          self.pathDict[list[i]] = [0, None]
        else:
          self.pathDict[list[i]] = [None, None]

  # Add node to set
  def insert(self, node:CS312GraphNode, dist:int, prevNode:CS312GraphNode):
    self.decrease_key(node, dist, prevNode)

  # Replace new shortest distance and prevNode for a specific node
  def decrease_key(self, node:CS312GraphNode, dist:int, prevNode:CS312GraphNode):
    self.set_dist(node, dist)
    self.set_dist_prev_node(node, prevNode)

  #Visit the next unvisited smallest node, return the node and the dist
  def delete_min(self):
    minNode, minDist = None, None
    # Iterate through dict to find min distance
    for key, value in self.pathDict.items():
      if (key not in self.visitedNodes):
        if (value[0] is not None) and (minDist is None or value[0] < minDist):
          minNode = key
          minDist = value[0]
    if minNode is not None:
      self.visitedNodes.add(minNode)
    return minNode, minDist

  def get_num_visited(self):
    return len(self.visitedNodes)

  # Same helpers as PQueueHeap
  def get_node_by_id(self, nodeId:int):
    for key in self.pathDict:
      if (key.node_id == nodeId):
        return key
    return None

  def get_dist(self, node:CS312GraphNode):
    return self.pathDict.get(node)[0]

  def get_dist_by_id(self, id:int):
    return self.get_dist(self.get_node_by_id(id))

  def set_dist(self, node:CS312GraphNode, dist:int):
    self.pathDict.get(node)[0] = dist

  def get_dist_prev_node(self, node:CS312GraphNode):
    return self.pathDict.get(node)[1]
  
  def get_dist_prev_node_by_id(self, id:int):
    return self.get_dist_prev_node(self.get_node_by_id(id))

  def set_dist_prev_node(self, node:CS312GraphNode, prevNode:CS312GraphNode):
    self.pathDict.get(node)[1] = prevNode

  def __str__(self):
    string = "\nVisited Nodes: "
    if len(self.visitedNodes) != 0:
      for node in self.visitedNodes:
        string += f"{node.node_id+self._idIncrement} "
      string += '\n'
    else:
      string += "*empty*\n"

    table_data = [["NodeKey","[Dist, PrevNode]"]]
    for key, value in self.pathDict.items():
      table_data.append([])
      if isinstance(key, CS312GraphNode):
        table_data[-1].append(key.node_id+self._idIncrement)
      dist, prevNode = value[0], value[1]
      if prevNode is not None and isinstance(prevNode, CS312GraphNode):
        prevNode = prevNode.node_id+self._idIncrement
      if dist is not None:
        table_data[-1].append(f"[{value[0]:.2f}, {prevNode}]")
      else:
        table_data[-1].append(f"[{value[0]}, {prevNode}]")
    for row in table_data:
      string += "{: <7} {: <20}".format(*row) + '\n'

    return string

  

class PQueueHeap:
  def __init__(self, list=None, sourceId=None):
    self._idIncrement = 1
    self.pathDict = dict() #CS312GraphNodes : [dist:int, prev:CS312GraphNodes]
    self.nodeIdQueue = [] #array of nodeIds, sorted by the min dist, 

    if list is not None:
      self.make_queue(list, sourceId)

  # Set up dictionary of nodes, with max len distances
  def make_queue(self, list, sourceId=None):
    for i in range(len(list)):
      if isinstance(list[i], CS312GraphNode):
        # Put the keys in the dictionary, with distance and null prevNode
        dist = float('inf')
        if (list[i].node_id == sourceId):
          dist = 0
        self.insert(list[i], dist, None)
  
  def insert(self, node:CS312GraphNode, dist=float('inf'), prevNode=None):
    # Add node to dict
    if (node != None):
      self.pathDict[node] = [dist, prevNode]
    # Add nodeId as the last element
    self.nodeIdQueue.append(node.node_id)
    # Reorder queue based on that new element
    self._reverseHeapify(len(self.nodeIdQueue)-1)

  # Replace new shortest distance and prevNode for a specific node
  def decrease_key(self, node:CS312GraphNode, dist:int, prevNode:CS312GraphNode):
    self.set_dist(node, dist)
    self.set_dist_prev_node(node, prevNode)
    # Reorder queue based on the updated distance
    self._reverseHeapify(self.nodeIdQueue.index(node.node_id))

  # Finds the shortest dist node, delete it and return that node and the dist
  def delete_min(self):
    if len(self.nodeIdQueue) == 0:
      return None, None
    oldRoot = self.get_node_by_id(self.nodeIdQueue[0])

    # Reorganize remaining queue elements
    # Replace root with last element
    self.nodeIdQueue[0] = self.nodeIdQueue[-1]
    # Delete last element
    del self.nodeIdQueue[-1]
    # Heapify new root
    self._heapify(0)

    return oldRoot, self.get_dist(oldRoot)

  # From the given index, check the parent for swaps and loop up the tree
  def _reverseHeapify(self, startIndex:int):
    i = startIndex
    print(f"i:{i}")
    while i >= 0:
      print(self.pathDict)
      self._heapify(i) # this call will not recurse, only potential swap parent with child
      i = floor((i-1)/2) # move up to the parent
      print(f"i:{i}")

  # From the given index, check the left and right children for swaps, recurses down the tree
  def _heapify(self, initialIndex:int):
    smallestIndex = initialIndex
    leftIndex = 2*initialIndex + 1
    rightIndex = 2*initialIndex + 2

    # Check if left node dist is smaller
    if (leftIndex < len(self.nodeIdQueue) 
      and self.get_dist_by_id(self.nodeIdQueue[leftIndex]) < self.get_dist_by_id(self.nodeIdQueue[smallestIndex])):
      smallestIndex = leftIndex

    # Check if right node dist is smaller
    if (rightIndex < len(self.nodeIdQueue) 
      and self.get_dist_by_id(self.nodeIdQueue[rightIndex]) < self.get_dist_by_id(self.nodeIdQueue[smallestIndex])):
      smallestIndex = rightIndex

    # If smallest is not root, swap and look at sub-tree
    if (smallestIndex != initialIndex):
      self.nodeIdQueue[smallestIndex], self.nodeIdQueue[initialIndex] = self.nodeIdQueue[initialIndex], self.nodeIdQueue[smallestIndex]
      self._heapify(smallestIndex)

  def get_num_visited(self):
    # totalNodes - nodes left to visit
    return len(self.pathDict) - len(self.nodeIdQueue)

  # Same helpers as PQueueArray
  def get_node_by_id(self, nodeId:int):
      for key in self.pathDict:
        if (key.node_id == nodeId):
          return key
      return None

  def get_dist(self, node:CS312GraphNode):
    return self.pathDict.get(node)[0]

  def get_dist_by_id(self, id:int):
    return self.get_dist(self.get_node_by_id(id))

  def set_dist(self, node:CS312GraphNode, dist:int):
    self.pathDict.get(node)[0] = dist

  def get_dist_prev_node(self, node:CS312GraphNode):
    return self.pathDict.get(node)[1]
  
  def get_dist_prev_node_by_id(self, id:int):
    return self.get_dist_prev_node(self.get_node_by_id(id))

  def set_dist_prev_node(self, node:CS312GraphNode, prevNode:CS312GraphNode):
    self.pathDict.get(node)[1] = prevNode

  def __str_(self):
    string = "\nNodeId Queue: "
    if len(self.nodeIdQueue) != 0:
      for node in self.nodeIdQueue:
        string += f"{node.node_id+self._idIncrement} "
      string += '\n'
    else:
      string += "*empty*\n"

    table_data = [["NodeKey","[Dist, PrevNode]"]]
    for key, value in self.pathDict.items():
      table_data.append([])
      if isinstance(key, CS312GraphNode):
        table_data[-1].append(key.node_id+self._idIncrement)
      dist, prevNode = value[0], value[1]
      if prevNode is not None and isinstance(prevNode, CS312GraphNode):
        prevNode = prevNode.node_id+self._idIncrement
      if dist is not None:
        table_data[-1].append(f"[{value[0]:.2f}, {prevNode}]")
      else:
        table_data[-1].append(f"[{value[0]}, {prevNode}]")
    for row in table_data:
      string += "{: <7} {: <20}".format(*row) + '\n'

    return string
