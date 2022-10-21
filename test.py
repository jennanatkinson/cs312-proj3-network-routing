from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from CS312Graph import CS312Graph, CS312GraphNode
from DataStructures import PQueueHeap
from NetworkRoutingSolver import NetworkRoutingSolver

# Tests for Heap structure

# Mock for CS312Node with node_id member
class MockNode:
  def __init__(self, id:int):
    self.node_id = id
  
def test_should_heapify_byWeight():
  heap = PQueueHeap()
  heap.pathDict = {MockNode(1): [10, None], MockNode(2): [5, None]}
  heap.nodeIdQueue = [1, 2]
  balancedHeap = [2, 1]

  heap._heapify(0)
  assert(heap.nodeIdQueue == balancedHeap)

def test_should_heapify_when_unbalancedRoot():
  heap = PQueueHeap()
  # Each id has a dist of the same weight
  heap.pathDict = {MockNode(5): [5, None], MockNode(6): [6, None], MockNode(10): [10, None], MockNode(11): [11, None], MockNode(13): [13, None], MockNode(15): [15, None], MockNode(20): [20, None]}
  heap.nodeIdQueue = [20, 5, 10, 15, 6, 11, 13]
  balancedHeap = [5, 6, 10, 15, 20, 11, 13]

  heap._heapify(0)
  assert(heap.nodeIdQueue == balancedHeap)

def test_should_heapify_when_unbalancedMiddleNode():
  heap = PQueueHeap()
  # Each id has a dist of the same weight
  heap.pathDict = {MockNode(5): [5, None], MockNode(6): [6, None], MockNode(11): [11, None], MockNode(14): [14, None], MockNode(15): [15, None], MockNode(20): [20, None]}
  heap.nodeIdQueue = [5, 6, 14, 15, 20, 11]
  balancedHeap = [5, 6, 11, 15, 20, 14]
  
  heap._heapify(2)
  assert(heap.nodeIdQueue == balancedHeap)

def test_should_reverseHeapify_when_unbalancedInsertInMiddle():
  heap = PQueueHeap()
  # Each id has a dist of the same weight
  heap.pathDict = {MockNode(2): [2, None], MockNode(6): [6, None], MockNode(10): [10, None], MockNode(15): [15, None]}
    
  heap.nodeIdQueue = [2, 15, 6, 10]
  finalHeap = [2, 10, 6, 15]

  heap._reverseHeapify(1)
  assert(heap.nodeIdQueue == finalHeap)
  assert(heap.get_node_by_id(15) != None) #make sure it didn't delete from pathDict

def test_should_reverseHeapify_when_unbalancedInsertAtEnd():
  heap = PQueueHeap()
  # Each id has a dist of the same weight
  heap.pathDict = {MockNode(1): [1, None], MockNode(2): [2, None], MockNode(6): [6, None], MockNode(10): [10, None], MockNode(15): [15, None]}
    
  heap.nodeIdQueue = [2, 10, 6, 15, 1]
  finalHeap = [1, 2, 6, 15, 10]

  heap._reverseHeapify(len(heap.nodeIdQueue)-1)
  assert(heap.nodeIdQueue == finalHeap)
  assert(heap.get_node_by_id(1) != None) #make sure it didn't delete from pathDict

def test_should_makeQueue():
  heap = PQueueHeap()
  # Each id has a dist of the same weight
  list = [CS312GraphNode(2, None), CS312GraphNode(3, None), CS312GraphNode(6, None), CS312GraphNode(10, None)]
  correctQueue = [10, 2, 3, 6]

  heap.make_queue(list, 10)

  # The source should be first, with 0 dist
  assert(heap.nodeIdQueue[0] == correctQueue[0])
  assert(heap.get_dist_by_id(heap.nodeIdQueue[0]) == 0)
  # All other dist should be inf
  for i in range(1, len(list)):
    assert(heap.get_dist_by_id(heap.nodeIdQueue[i]) == float('inf'))

def test_should_deleteMin():
  heap = PQueueHeap()
  # Each id has a dist of the same weight
  heap.pathDict = {MockNode(2): [2, None], MockNode(3): [3, None], MockNode(6): [6, None], MockNode(10): [10, None]}
    
  heap.nodeIdQueue = [2, 3, 6, 10]
  finalHeap = [3, 10, 6]

  heap.delete_min()
  assert(heap.nodeIdQueue == finalHeap)
  assert(heap.get_node_by_id(2) != None) #make sure it didn't delete from pathDict

def test_should_insert():
  heap = PQueueHeap()
  # Each id has a dist of the same weight
  heap.pathDict = {CS312GraphNode(2, None): [2, None], CS312GraphNode(3, None): [3, None], CS312GraphNode(6, None): [6, None], CS312GraphNode(10, None): [10, None]}
  heap.nodeIdQueue = [2, 3, 6, 10]
  finalHeap = [1, 2, 6, 10, 3]
  heap.insert(CS312GraphNode(1, None), 1)
  assert(heap.nodeIdQueue == finalHeap)
  assert(heap.get_node_by_id(1) != None) #make sure it added to the dict
  assert(heap.get_node_by_id(1).node_id == 1)
  assert(heap.get_dist_by_id(1) == 1) #make sure the weight is correct

def test_should_decreaseKey():
  heap = PQueueHeap()
  nodeToUpdate = CS312GraphNode(15, None)
  # Each id has a dist of the same weight
  heap.pathDict = {CS312GraphNode(2, None): [2, None], CS312GraphNode(6, None): [6, None], CS312GraphNode(10, None): [10, None], nodeToUpdate: [15, None]}
  
  heap.nodeIdQueue = [2, 10, 6, 15]
  finalHeap = [15, 2, 6, 10] #node 15 will have a weight of 1

  newDist = 1
  heap.decrease_key(nodeToUpdate, newDist, None)
  assert(heap.nodeIdQueue == finalHeap)
  assert(heap.get_dist(nodeToUpdate) == newDist) #make sure it didn't delete from pathDict

# Tests for computeShortestPaths() and getShortestPath()

def test_array_should_returnZero_when_singleNodeNoEdges():
  should_returnZero_when_singleNodeNoEdges(False)

def test_heap_should_returnZero_when_singleNodeNoEdges():
  should_returnZero_when_singleNodeNoEdges(True)

# Test single node as start node and end node
def should_returnZero_when_singleNodeNoEdges(use_heap=False):
  solver = NetworkRoutingSolver()
  nodes, edgeList = [QPointF(0,0)], [[]] #empty list of edges
  graph = CS312Graph(nodes, edgeList)
  solver.initializeNetwork(graph)
  sourceId = 0
  
  solver.computeShortestPaths(sourceId, use_heap)
  assert(solver.sourceId == sourceId)
  assert(solver.queue.get_dist_by_id(sourceId) == 0)
  
  answer = solver.getShortestPath(sourceId)
  assert(answer['cost'] == 0)
  assert(answer['path'] == [])

def test_array_should_returnEdgeLen_when_twoNodesOneEdge():
  should_returnEdgeLen_when_twoNodesOneEdge(False)

def test_heap_should_returnEdgeLen_when_twoNodesOneEdge():
  should_returnEdgeLen_when_twoNodesOneEdge(True)

# Test two nodes, one as start and one as end
def should_returnEdgeLen_when_twoNodesOneEdge(use_heap=False):
  solver = NetworkRoutingSolver()
  # Array of nodes, array of neighborsForEachNode < array of edges < [index of edgeNode, weight of edge]
  nodes = [QPointF(0,0), QPointF(10, 10)]
  sourceId, destId = 0, 1
  edgeLen = 5
  edgeList = [[[destId,edgeLen]], []]
  graph = CS312Graph(nodes, edgeList)
  solver.initializeNetwork(graph)
  
  solver.computeShortestPaths(sourceId, use_heap)
  assert(solver.sourceId == sourceId)
  assert(solver.queue.get_dist_by_id(sourceId) == 0)
  assert(solver.queue.get_dist_by_id(destId) == edgeLen)
  
  answer = solver.getShortestPath(destId)
  assert(answer['cost'] == edgeLen)

def test_array_should_returnInf_when_noPath():
  should_returnInf_when_noPath(False)

def test_heap_should_returnInf_when_noPath():
  should_returnInf_when_noPath(True)

# Test two nodes with no path between them
def should_returnInf_when_noPath(use_heap=False):
  solver = NetworkRoutingSolver()
  # Array of nodes, array of neighborsForEachNode < array of edges < [index of edgeNode, weight of edge]
  nodes = [QPointF(0,0), QPointF(10, 10)]
  sourceId, destId = 0, 1
  edgeList = [[], []]
  graph = CS312Graph(nodes, edgeList)
  solver.initializeNetwork(graph)
  
  solver.computeShortestPaths(sourceId, use_heap)
  assert(solver.sourceId == sourceId)
  assert(solver.queue.get_dist_by_id(sourceId) == 0)
  assert(solver.queue.get_dist_by_id(destId) == None 
  or solver.queue.get_dist_by_id(destId) == float('inf'))
  
  answer = solver.getShortestPath(destId)
  assert(answer['cost'] == float('inf'))

def test_array_should_returnSmallerCombinedEdge_when_multipleNodesMultipleEdges():
  should_returnSmallerCombinedEdge_when_multipleNodesMultipleEdges(False)

def test_heap_should_returnSmallerCombinedEdge_when_multipleNodesMultipleEdges():
  should_returnSmallerCombinedEdge_when_multipleNodesMultipleEdges(True)

# Test three nodes, with the single edge to dest being larger, but the two combined edges being smaller
def should_returnSmallerCombinedEdge_when_multipleNodesMultipleEdges(use_heap=False):
  solver = NetworkRoutingSolver()
  # Array of nodes, array of neighborsForEachNode < array of edges < [index of edgeNode, weight of edge]
  nodes = [QPointF(0,0), QPointF(10, 10), QPointF(0, 10)]
  sourceId, midId, destId = 0, 1, 2
  bigEdgeLen, smallEdgeLen1, smallEdgeLen2 = 10, 1, 2
  edgeList = [[[midId,smallEdgeLen1], [destId, bigEdgeLen]], [[destId, smallEdgeLen2]], []]
  graph = CS312Graph(nodes, edgeList)
  solver.initializeNetwork(graph)
  
  solver.computeShortestPaths(sourceId, use_heap)
  assert(solver.sourceId == sourceId)
  assert(solver.queue.get_dist_by_id(sourceId) == 0)
  assert(solver.queue.get_dist_by_id(midId) == smallEdgeLen1)
  assert(solver.queue.get_dist_prev_node_by_id(destId).node_id == midId)
  assert(solver.queue.get_dist_by_id(destId) == (smallEdgeLen1 + smallEdgeLen2))
  
  answer = solver.getShortestPath(midId)
  assert(answer['cost'] == smallEdgeLen1)

  answer = solver.getShortestPath(destId)
  assert(answer['cost'] == (smallEdgeLen1 + smallEdgeLen2))


def test_array_should_pass_when_complexGraph():
  should_pass_when_complexGraph(False)

def test_heap_should_pass_when_complexGraph():
  should_pass_when_complexGraph(True)

# Test example from class slides (lecture 9, slide 109)
def should_pass_when_complexGraph(use_heap=False):
  solver = NetworkRoutingSolver()
  # Array of nodes, array of neighborsForEachNode < array of edges < [index of edgeNode, weight of edge]
  nodes = [QPointF(0,0), QPointF(1, 1), QPointF(2, 2), QPointF(3, 3), QPointF(4, 4), QPointF(5, 5), QPointF(6, 6)]
  c, d, e, g, h, i, l = 0, 1, 2, 3, 4, 5, 6
  edgeList = [[[e, 5], [d, 15], [h, 2]], [[h, 3], [i, 4]], [[d, 6]], [[d, 2]], [[i, 1]], [[l, 2]], [[g, 3]]]
  graph = CS312Graph(nodes, edgeList)
  solver.initializeNetwork(graph)
  
  solver.computeShortestPaths(c, use_heap)
  assert(solver.sourceId == c)
  assert(solver.queue.get_dist_by_id(c) == 0)
  assert(solver.queue.get_dist_by_id(d) == 10)
  assert(solver.queue.get_dist_prev_node_by_id(d).node_id == g)
  assert(solver.queue.get_dist_by_id(e) == 5)
  assert(solver.queue.get_dist_prev_node_by_id(e).node_id == c)
  assert(solver.queue.get_dist_by_id(g) == 8)
  assert(solver.queue.get_dist_prev_node_by_id(g).node_id == l)
  assert(solver.queue.get_dist_by_id(h) == 2)
  assert(solver.queue.get_dist_prev_node_by_id(h).node_id == c)
  assert(solver.queue.get_dist_by_id(i) == 3)
  assert(solver.queue.get_dist_prev_node_by_id(i).node_id == h)
  assert(solver.queue.get_dist_by_id(l) == 5)
  assert(solver.queue.get_dist_prev_node_by_id(l).node_id == i)
  
  answer = solver.getShortestPath(d)
  assert(answer['cost'] == 10)