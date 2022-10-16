from CS312Graph import *


class PQueueArray:
  #dict pathList, node : [distance, prevNode]
  #set visitedNodes
  def __init__(self, list=None):
    self.pathList = dict()
    self.visitedNodes = set()

    if list is not None:
      self.make_queue(list)

  # Set up dictionary of nodes, with max len distances
  def make_queue(self, list):
    for i in range(len(list)):
      if isinstance(list[i], CS312GraphNode):
        # Put the keys in the dictionary, with null distance and prevNode
        self.pathList[list[i]] = [None, None]

  def insert(self):
    return
  def decrease_key(self):
    return

  #aka visit next node
  def delete_min(self):
    # delete __find_min()
    return
  def __find_min(self):
    #iterate through nodeKey dictionary to find the item with min priority
    return

  def __str__(self):
    string = "\nVisited Nodes: "
    if len(self.visitedNodes) != 0 :
      string += ", ".join(map(str,self.visitedNodes)) + '\n'
    else:
      string += "*empty*\n"

    table_data = [["NodeKey","[Dist, PrevNode]"]]
    for key, value in self.pathList.items():
      table_data.append([])
      if isinstance(key, CS312GraphNode):
        table_data[len(table_data) - 1].append(key.node_id)
      prevNode = value[1]
      if prevNode is not None and isinstance(prevNode, CS312GraphNode):
        prevNode = prevNode.node_id
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
