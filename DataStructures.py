from math import floor
from CS312Graph import *

# Space: O(|V|)
class PQueueArray:
  #Note: uses None as inf distance

  #idIncrement aka num to add to the ids (0 => the real index, 1=> offset by 1 like the GUI)
  #dict pathDict {CS312GraphNode node : [int distance, CS312GraphNode prevNode]}
  #set CS312GraphNode visitedNodes
  
  # Time: O(|V|)
  def __init__(self, list=None, sourceId:int=None):
    self._idIncrement = 1
    self.pathDict = dict() # Space: O(|V|)
    self.visitedNodes = set() # Space: O(|V|)

    if list is not None:
      self.make_queue(list, sourceId)

  # Time: O(|V|)
  # Set up dictionary of nodes, with max len distances
  def make_queue(self, list, sourceId:int=None):
    for i in range(len(list)):
      if isinstance(list[i], CS312GraphNode):
        # Put the keys in the dictionary, with null distance and prevNode
        if (list[i].node_id == sourceId):
          self.pathDict[list[i]] = [0, None]
        else:
          self.pathDict[list[i]] = [None, None]

  # Add node to set
  # Time: O(1)
  def insert(self, node:CS312GraphNode, dist:int, prevNode:CS312GraphNode):
    self.decrease_key(node, dist, prevNode)

  # Replace new shortest distance and prevNode for a specific node
  # Time: O(1)
  def decrease_key(self, node:CS312GraphNode, dist:int, prevNode:CS312GraphNode):
    self.set_dist(node, dist)
    self.set_dist_prev_node(node, prevNode)

  #Visit the next unvisited smallest node, return the node and the dist
  # Time: O(|V|)
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

  # Time: O(1)
  def get_num_visited(self):
    return len(self.visitedNodes)

  # Note: (below) Same helpers as PQueueHeap

  # Time: O(|V|)
  def get_node_by_id(self, nodeId:int):
    for key in self.pathDict:
      if (key.node_id == nodeId):
        return key
    return None

  # Time: O(1)
  def get_dist(self, node:CS312GraphNode):
    return self.pathDict.get(node)[0]

  # Time: O(|V|)
  def get_dist_by_id(self, id:int):
    return self.get_dist(self.get_node_by_id(id))

  # Time: O(1)
  def set_dist(self, node:CS312GraphNode, dist:int):
    self.pathDict.get(node)[0] = dist

  # Time: O(1)
  def get_dist_prev_node(self, node:CS312GraphNode):
    return self.pathDict.get(node)[1]
  
  # Time: O(|V|)
  def get_dist_prev_node_by_id(self, id:int):
    return self.get_dist_prev_node(self.get_node_by_id(id))

  # Time: O(1)
  def set_dist_prev_node(self, node:CS312GraphNode, prevNode:CS312GraphNode):
    self.pathDict.get(node)[1] = prevNode

  # Time: O(|V|)
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

  
# Space: O(|V|)
class PQueueHeap:
  #Note: uses inf for distance
  #pathDict => CS312GraphNodes : [dist:int, prev:CS312GraphNodes]
  #array of CS312GraphNodes, sorted by the min dist

  # Time: O(|V|log|V|)
  def __init__(self, list=None, sourceId:int=None):
    self._idIncrement = 1
    self.pathDict = dict() # Space: O(|V|)
    self.nodeQueue = [] # Space: O(|V|)

    if list is not None:
      self.make_queue(list, sourceId)

  # Set up dictionary of nodes, with max len distances
  # Time: O(|V|log|V|)
  def make_queue(self, list, sourceId:int=None):
    for i in range(len(list)):
      if isinstance(list[i], CS312GraphNode):
        # Put the keys in the dictionary, with distance and null prevNode
        dist = float('inf')
        if (list[i].node_id == sourceId):
          dist = 0
        self.insert(list[i], dist, None)
  
  # Time: O(log|V|)
  def insert(self, node:CS312GraphNode, dist=float('inf'), prevNode=None):
    # Add node to dict
    if (node != None):
      self.pathDict[node] = [dist, prevNode]
    # Add nodeId as the last element
    self.nodeQueue.append(node)
    # Reorder queue based on that new element
    self._reverseHeapify(len(self.nodeQueue)-1)

  # Replace new shortest distance and prevNode for a specific node
  # Time: O(log|V|)
  def decrease_key(self, node:CS312GraphNode, dist:int, prevNode:CS312GraphNode):
    assert(dist <= self.get_dist(node))
    self.set_dist(node, dist)
    self.set_dist_prev_node(node, prevNode)
    # Reorder queue based on the updated distance
    self._reverseHeapify(self.nodeQueue.index(node))

  # Finds the shortest dist node, delete it and return that node and the dist
  # Time: O(log|V|)
  def delete_min(self):
    if len(self.nodeQueue) == 0:
      return None, None
    oldRoot = self.nodeQueue[0]

    # Reorganize remaining queue elements
    # Replace root with last element
    self.nodeQueue[0] = self.nodeQueue[-1]
    # Delete last element
    del self.nodeQueue[-1]
    # Heapify new root
    self._heapify(0)

    return oldRoot, self.get_dist(oldRoot)

  # From the given index, check the parent for swaps and loop up the tree
  # Time: O(log|V|)
  def _reverseHeapify(self, startIndex:int):
    i = startIndex
    while i >= 0:
      self._heapify(i) # this call will not recurse, only potential swap parent with child
      i = floor((i-1)/2) # move up to the parent

  # From the given index, check the left and right children for swaps, recurses down the tree
  # Time: O(log|V|)
  def _heapify(self, initialIndex:int):
    smallestIndex = initialIndex
    leftIndex = 2*initialIndex + 1
    rightIndex = 2*initialIndex + 2
    
    # Check if left node dist is smaller
    if (leftIndex < len(self.nodeQueue) 
      and self.get_dist(self.nodeQueue[leftIndex]) < self.get_dist(self.nodeQueue[smallestIndex])):
      smallestIndex = leftIndex

    # Check if right node dist is smaller
    if (rightIndex < len(self.nodeQueue) 
      and self.get_dist(self.nodeQueue[rightIndex]) < self.get_dist(self.nodeQueue[smallestIndex])):
      smallestIndex = rightIndex

    # If smallest is not root, swap and look at sub-tree
    if (smallestIndex != initialIndex):
      self.nodeQueue[smallestIndex], self.nodeQueue[initialIndex] = self.nodeQueue[initialIndex], self.nodeQueue[smallestIndex]
      self._heapify(smallestIndex)

  # Time: O(1)
  def get_num_visited(self):
    # totalNodes - nodes left to visit
    return len(self.pathDict) - len(self.nodeQueue)

  # Note: (below) Same helpers as PQueueArray

  # Time: O(|V|)
  def get_node_by_id(self, nodeId:int):
      for key in self.pathDict:
        if (key.node_id == nodeId):
          return key
      return None

  # Time: O(1)
  def get_dist(self, node:CS312GraphNode):
    return self.pathDict.get(node)[0]

  # Time: O(|V|)
  def get_dist_by_id(self, id:int):
    return self.get_dist(self.get_node_by_id(id))

  # Time: O(1)
  def set_dist(self, node:CS312GraphNode, dist:int):
    self.pathDict.get(node)[0] = dist

  # Time: O(1)
  def get_dist_prev_node(self, node:CS312GraphNode):
    return self.pathDict.get(node)[1]
  
  # Time: O(|V|)
  def get_dist_prev_node_by_id(self, id:int):
    return self.get_dist_prev_node(self.get_node_by_id(id))

  # Time: O(1)
  def set_dist_prev_node(self, node:CS312GraphNode, prevNode:CS312GraphNode):
    self.pathDict.get(node)[1] = prevNode

  # Time: O(|V|)
  def __str__(self):
    string = "\nNodeId Queue: "
    if len(self.nodeQueue) != 0:
      for node in self.nodeQueue:
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
