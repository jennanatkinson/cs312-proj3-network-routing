#!/usr/bin/python3
from CS312Graph import *
from DataStructures import *
import time


class NetworkRoutingSolver:
    def __init__(self):
        pass

    def initializeNetwork(self, network):
        assert(type(network) == CS312Graph)
        self.network = network # Space: O(|V|)
        self.queue = None # Space: O(|V|)

    def getShortestPath(self, destIndex):
        # print(self.queue)
        self.dest = self.queue.get_node_by_id(destIndex)
        path_edges = []
        total_length = 0
        # If there is no possible distance to the destination
        if self.queue.get_dist(self.dest) is None or self.queue.get_dist(self.dest) == float('inf'):
            total_length = float('inf')
        else:
            total_length = self.queue.get_dist(self.dest)
            # Trace the destination node back to the source, working BACKWARDS, looking up the edges in the network
            currentNode = self.dest
            len = 0
            # print(f"Shortest Path: ({currentNode.node_id+self.queue._idIncrement})", end = '')
            while currentNode.node_id != self.sourceId:
                prevNode = self.queue.get_dist_prev_node(currentNode)
                edgeLen = self.network.getNodeEdge(prevNode.node_id, currentNode.node_id).length
                # print(f" <--{edgeLen:.2f}-- ({prevNode.node_id+self.queue._idIncrement})", end = '')
                path_edges.append((prevNode.loc, currentNode.loc, '{:.0f}'.format(edgeLen)))
                currentNode = prevNode
                len += edgeLen # to double check this is compounding properly
            # print('\n')
            assert(round(len, 5) == round(total_length, 5))
        # print(f'Total Cost: {total_length:.2f}')
        # print(f'Path: {path_edges}\n')
        return {'cost':total_length, 'path':path_edges}

    # ArrayTime: O(|V|**2) HeapTime: O(|V|log|V|)
    def computeShortestPaths(self, srcId, use_heap=False):
        self.sourceId = srcId
        t1 = time.time()
        if (use_heap):
            # Time: O(|V|log|V|)
            self.queue = PQueueHeap(self.network.nodes, self.sourceId)
        else:
            # Time: O(|V|)
            self.queue = PQueueArray(self.network.nodes, self.sourceId)
        # print(self.queue)

        # Run while there are unvisited nodes
        # ArrayTime: O(|V|**2) HeapTime: O(|V|log|V|)
        while self.queue.get_num_visited() < len(self.network.nodes):
            # Get the next smallest node/distance that hasn't been visited, add to visited
            node, dist = self.queue.delete_min() # ArrayTime: O(|V|) HeapTime: O(log|V|)
            if node is None or dist == float('inf'):
                break # the only nodes that are left are infinity
            
            # For each edge aka neighbor of the node
            # Time: O(1) bc we have constrained edges to 3
            for i in range(len(node.neighbors)):
                neighborNode = node.neighbors[i].dest
                # Get the shortest distance logged for that edge
                currentEdgeDist = self.queue.get_dist(neighborNode)
                # Calculate what the new distance could be
                newEdgeDist = dist + node.neighbors[i].length
                
                # If new possible distance is less than current distance, update
                if currentEdgeDist is None or newEdgeDist < currentEdgeDist:
                    #ArrayTime: O(1) HeapTime: O(log|V|)
                    self.queue.decrease_key(neighborNode, newEdgeDist, node)
            # print(self.queue)
        
        t2 = time.time()
        return (t2-t1)

