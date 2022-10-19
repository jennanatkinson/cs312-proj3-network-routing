from CS312Graph import *


class PQueueArray:
  #dict pathDict {CS312Node node : [int distance, CS312Node prevNode]}
  #set CS312Node visitedNodes
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

  def get_node_by_id(self, nodeId:int):
    for key in self.pathDict:
      if (key.node_id == nodeId):
        return key
    return None

  def insert(self, node:CS312GraphNode, dist:int, prevNode:CS312GraphNode):
    self.set_dist(node, dist)
    self.set_dist_prev_node(node, prevNode)

  def addVisited(self, node:CS312GraphNode):
    self.visitedNodes.add(node)

  def decrease_key(self):
    return

  #Visit the next unvisited smallest node
  def delete_min(self):
    minNode, minDist = None, None
    # Iterate through dict to find min distance
    for key, value in self.pathDict.items():
      if (key not in self.visitedNodes):
        if (value[0] is not None) and (minDist is None or value[0] < minDist):
          minNode = key
          minDist = value[0]
    return minNode, minDist

  def get_dist(self, node:CS312GraphNode):
    return self.pathDict.get(node)[0]

  def get_dist_by_id(self, id:int):
    return self.get_dist(self.get_node_by_id(id))

  def set_dist(self, node:CS312GraphNode, dist:int):
    self.pathDict.get(node)[0] = dist

  def get_dist_prev_node(self, node:CS312GraphNode):
    return self.pathDict.get(node)[1]

  def set_dist_prev_node(self, node:CS312GraphNode, prevNode:CS312GraphNode):
    self.pathDict.get(node)[1] = prevNode



  # def __find_min_(self):
  #   minDist = -1
  #   minNode = None
  #   # Iterate through dict to find min distance
  #   for key, value in self.pathDict.items():
  #     if value[0] < minDist:
  #       minNode = key
  #   return minNode, minDist

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
        table_data[len(table_data) - 1].append(key.node_id+self._idIncrement)
      dist, prevNode = value[0], value[1]
      if prevNode is not None and isinstance(prevNode, CS312GraphNode):
        prevNode = prevNode.node_id+self._idIncrement
      if dist is not None:
        table_data[len(table_data) - 1].append(f"[{value[0]:.2f}, {prevNode}]")
      else:
        table_data[len(table_data) - 1].append(f"[{value[0]}, {prevNode}]")
    for row in table_data:
      string += "{: <7} {: <20}".format(*row) + '\n'

    return string

  

class PQueueHeap:
  def __init__(self):
    return
  def make_queue(self):
    return
  def insert(self):
    return
  def decrease_key(self):
    return
  def delete_min(self):
    return
  def __find_min(self):
    return
