#!/usr/bin/python3
from CS312Graph import *
from DataStructures import *
import time


class NetworkRoutingSolver:
    def __init__(self):
        pass

    def initializeNetwork(self, network):
        assert(type(network) == CS312Graph)
        self.network = network
        self.queue = None

    def getShortestPath(self, destIndex):
        print(self.queue)
        self.dest = self.queue.get_node_by_id(destIndex)
        path_edges = []
        total_length = 0
        # If there is no possible distance to the destination
        if self.queue.get_dist(self.dest) is None:
            total_length = float('inf')
        else:
            total_length = self.queue.get_dist(self.dest)
            # Trace the destination node back to the source, working BACKWARDS, looking up the edges in the network
            currentNode = self.dest
            len = 0
            print(f"Shortest Path: ({currentNode.node_id+self.queue._idIncrement})", end = '')
            while currentNode.node_id != self.sourceId:
                prevNode = self.queue.get_dist_prev_node(currentNode)
                edgeLen = self.network.getNodeEdge(prevNode.node_id, currentNode.node_id).length
                print(f" <--{edgeLen:.2f}-- ({prevNode.node_id+self.queue._idIncrement})", end = '')
                path_edges.append((prevNode.loc, currentNode.loc, '{:.0f}'.format(edgeLen)))
                currentNode = prevNode
                len += edgeLen # to double check this is compounding properly
            print('\n')
            assert(round(len, 5) == round(total_length, 5))
        print(f'Total Cost: {total_length:.2f}')
        # print(f'Path: {path_edges}')
        print('\n')
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths(self, srcId, use_heap=False):
        self.sourceId = srcId
        t1 = time.time()
        if (use_heap):
            self.queue = PQueueHeap(self.network.nodes, self.sourceId)
        else:
            self.queue = PQueueArray(self.network.nodes, self.sourceId)
        # Run while there are unvisited nodes
        #print(self.queueArray)
        while self.queue.get_num_visited() < len(self.network.nodes):
            # Get the next smallest node/distance that hasn't been visited
            node, dist = self.queue.delete_min()
            if node is None:
                break # the only nodes that are left are infinity
            # For each edge aka neighbor of the node
            for i in range(len(node.neighbors)):
                neighborNode = node.neighbors[i].dest
                # Get the shortest distance logged for that edge
                currentEdgeDist = self.queue.get_dist(neighborNode)
                # Calculate what the new distance could be
                newEdgeDist = dist + node.neighbors[i].length
                # If new possible distance is less than current distance, update
                if currentEdgeDist is None or newEdgeDist < currentEdgeDist:
                    self.queue.decrease_key(neighborNode, newEdgeDist, node)
            # Add to visitedNodes
            self.queue.add_visited(node)
            #print(self.queueArray)

        t2 = time.time()
        return (t2-t1)

