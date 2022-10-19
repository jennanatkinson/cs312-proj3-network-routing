from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from CS312Graph import CS312Graph
from NetworkRoutingSolver import NetworkRoutingSolver

#Tests for computeShortestPaths()

# Test single node as start node and end node
def test_should_returnZero_when_singleNodeNoEdges():
  solver = NetworkRoutingSolver()
  nodes, edgeList = [QPointF(0,0)], [[]] #empty list of edges
  graph = CS312Graph(nodes, edgeList)
  solver.initializeNetwork(graph)
  sourceId = 0
  
  solver.computeShortestPaths(sourceId)
  assert(solver.sourceId == sourceId)
  assert(solver.queueArray.get_dist_by_id(sourceId) == 0)
  
  answer = solver.getShortestPath(sourceId)
  assert(answer['cost'] == 0)
  assert(answer['path'] == [])

# Test two nodes, one as start and one as end
def test_should_returnEdgeLen_when_twoNodesOneEdge():
  solver = NetworkRoutingSolver()
  # Array of nodes, array of neighborsForEachNode < array of edges < [index of edgeNode, weight of edge]
  nodes = [QPointF(0,0), QPointF(10, 10)]
  sourceId = 0
  edgeLen = 5
  destId = 1
  edgeList = [[[destId,edgeLen]], []]
  graph = CS312Graph(nodes, edgeList)
  solver.initializeNetwork(graph)
  
  
  solver.computeShortestPaths(sourceId)
  assert(solver.sourceId == sourceId)
  assert(solver.queueArray.get_dist_by_id(sourceId) == 0)
  assert(solver.queueArray.get_dist_by_id(destId) == edgeLen)
  
  answer = solver.getShortestPath(destId)
  assert(answer['cost'] == edgeLen)

# Test two nodes with no path between them
def should_returnInf_when_noPath():
  return

# Test three nodes, with the single edge to dest being larger, but the two combined edges being smaller
def should_returnSmallerCombinedEdge_when_multipleNodesMultipleEdges():
  return

# Test example from slides
def should_pass_when_complexGraph():
  return