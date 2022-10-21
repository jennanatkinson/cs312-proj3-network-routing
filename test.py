from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from CS312Graph import CS312Graph, CS312GraphNode
from DataStructures import PQueueHeap
from NetworkRoutingSolver import NetworkRoutingSolver

# Tests for Heap structure

def test_should_heapify_byWeight():
  heap = PQueueHeap()
  one, two = CS312GraphNode(1), CS312GraphNode(2)
  
  heap.pathDict = {one: [10, None], two: [5, None]}
  heap.nodeQueue = [one, two]
  balancedHeap = [two, one]

  heap._heapify(0)
  assert(heap.nodeQueue == balancedHeap)

def test_should_heapify_when_unbalancedRoot():
  heap = PQueueHeap()
  five, six, ten, eleven, thirteen, fifteen, twenty = CS312GraphNode(5), CS312GraphNode(6), CS312GraphNode(10), CS312GraphNode(11), CS312GraphNode(13), CS312GraphNode(15), CS312GraphNode(20)
  # Each id has a dist of the same weight
  heap.pathDict = {five: [5, None], six: [6, None], ten: [10, None], eleven: [11, None], thirteen: [13, None], fifteen: [15, None], twenty: [20, None]}
  heap.nodeQueue = [twenty, five, ten, fifteen, six, eleven, thirteen]
  balancedHeap = [five, six, ten, fifteen, twenty, eleven, thirteen]

  heap._heapify(0)
  assert(heap.nodeQueue == balancedHeap)

def test_should_heapify_when_unbalancedMiddleNode():
  heap = PQueueHeap()
  five, six, eleven, fourteen, fifteen, twenty = CS312GraphNode(5), CS312GraphNode(6), CS312GraphNode(11), CS312GraphNode(13), CS312GraphNode(14), CS312GraphNode(20)
  # Each id has a dist of the same weight
  heap.pathDict = {five: [5, None], six: [6, None], eleven: [11, None], fourteen: [14, None], fifteen: [15, None], twenty: [20, None]}
  heap.nodeQueue = [five, six, fourteen, fifteen, twenty, eleven]
  balancedHeap = [five, six, eleven, fifteen, twenty, fourteen]
  
  heap._heapify(2)
  assert(heap.nodeQueue == balancedHeap)

def test_should_reverseHeapify_when_unbalancedInsertInMiddle():
  heap = PQueueHeap()
  two, six, ten, fifteen = CS312GraphNode(2), CS312GraphNode(6), CS312GraphNode(10), CS312GraphNode(15)
  # Each id has a dist of the same weight
  heap.pathDict = {two: [2, None], six: [6, None], ten: [10, None], fifteen: [15, None]}
    
  heap.nodeQueue = [two, fifteen, six, ten]
  finalHeap = [two, ten, six, fifteen]

  heap._reverseHeapify(1)
  assert(heap.nodeQueue == finalHeap)
  assert(heap.pathDict.get(fifteen) != None) #make sure it didn't delete from pathDict

def test_should_reverseHeapify_when_unbalancedInsertAtEnd():
  heap = PQueueHeap()
  one, two, six, ten, fifteen = CS312GraphNode(1), CS312GraphNode(2), CS312GraphNode(6), CS312GraphNode(10), CS312GraphNode(15)
  # Each id has a dist of the same weight
  heap.pathDict = {one: [1, None], two: [2, None], six: [6, None], ten: [10, None], fifteen: [15, None]}
    
  heap.nodeQueue = [two, ten, six, fifteen, one]
  finalHeap = [one, two, six, fifteen, ten]

  heap._reverseHeapify(len(heap.nodeQueue)-1)
  assert(heap.nodeQueue == finalHeap)
  assert(heap.pathDict.get(one) != None) #make sure it didn't delete from pathDict

def test_should_makeQueue():
  heap = PQueueHeap()
  two, three, six, ten = CS312GraphNode(2), CS312GraphNode(3), CS312GraphNode(6), CS312GraphNode(10)
  # Each id has a dist of the same weight
  list = [two, three, six, ten]
  correctQueue = [ten, two, three, six]

  heap.make_queue(list, ten.node_id)
  print(heap)
  # The source should be first, with 0 dist
  assert(heap.nodeQueue[0] == correctQueue[0])
  assert(heap.get_dist(ten) == 0)
  # All other dist should be inf
  for i in range(1, len(list)):
    assert(heap.get_dist(heap.nodeQueue[i]) == float('inf'))

def test_should_deleteMin():
  heap = PQueueHeap()
  two, three, six, ten = CS312GraphNode(2), CS312GraphNode(3), CS312GraphNode(6), CS312GraphNode(10)
  # Each id has a dist of the same weight
  heap.pathDict = {two: [2, None], three: [3, None], six: [6, None], ten: [10, None]}
    
  heap.nodeQueue = [two, three, six, ten]
  finalHeap = [three, ten, six]

  heap.delete_min()
  assert(heap.nodeQueue == finalHeap)
  assert(heap.pathDict.get(two) != None) #make sure it didn't delete from pathDict

def test_should_insert():
  heap = PQueueHeap()
  one, two, three, six, ten = CS312GraphNode(1, None), CS312GraphNode(2, None), CS312GraphNode(3, None), CS312GraphNode(6, None), CS312GraphNode(10, None)
  # Each id has a dist of the same weight
  heap.pathDict = {two: [2, None], three: [3, None], six: [6, None], ten: [10, None]}
  heap.nodeQueue = [two, three, six, ten]
  finalHeap = [one, two, six, ten, three]
  heap.insert(one, 1)
  assert(heap.nodeQueue == finalHeap)
  assert(heap.pathDict.get(one) != None) #make sure it added to the dict
  assert(heap.get_dist(one) == 1) #make sure the weight is correct

def test_should_decreaseKey():
  heap = PQueueHeap()
  nodeToUpdate = CS312GraphNode(15, None)
  two, six, ten = CS312GraphNode(2, None), CS312GraphNode(6, None), CS312GraphNode(10, None)
  # Each id has a dist of the same weight
  heap.pathDict = {two: [2, None], six: [6, None], ten: [10, None], nodeToUpdate: [15, None]}
  
  heap.nodeQueue = [two, ten, six, nodeToUpdate]
  finalHeap = [nodeToUpdate, two, six, ten] #node 15 will have a weight of 1

  newDist = 1
  heap.decrease_key(nodeToUpdate, newDist, None)
  assert(heap.nodeQueue == finalHeap)
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