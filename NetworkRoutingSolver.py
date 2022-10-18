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
        self.queueArray = None

    def getShortestPath(self, destIndex):
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE
        self.dest = self.queueArray.get_node_by_id(destIndex)
        path_edges = []
        total_length = 0
        # If there is no possible distance to the destination
        if self.queueArray.get_shortest_dist(self.dest) is None:
            total_length = float('inf')
        else:
            # Trace the destination node back to the source, looking up the edges in the table
            currentNode = self.dest
            print(f"Shortest Path: {currentNode.node_id+self.queueArray._idIncrement}", end = '')
            while currentNode.node_id != self.sourceId:
                edgeLen = self.queueArray.get_shortest_dist(currentNode)
                otherNode = self.queueArray.get_shortest_dist_prev_node(currentNode)
                path_edges.append((currentNode.loc, otherNode.loc, '{:.0f}'.format(edgeLen)))
                total_length += edgeLen
                currentNode = otherNode
                print(f" <- {otherNode.node_id+self.queueArray._idIncrement}", end = '')
            print('\n')
            # node = self.network.nodes[self.source]
            # edges_left = 3
            # while edges_left > 0:
            #     edge = node.neighbors[2]
            #     path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            #     total_length += edge.length
            #     node = edge.dest
            #     edges_left -= 1
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths(self, srcId, use_heap=False):
        self.sourceId = srcId
        t1 = time.time()
        self.queueArray = PQueueArray(self.network.nodes, self.sourceId)
        # Run while there are unvisited nodes
        print(self.queueArray)
        while len(self.queueArray.visitedNodes) < len(self.network.nodes):
            # Get the next smallest node/distance that hasn't been visited
            node, dist = self.queueArray.delete_min()
            # For each edge aka neighbor of the node
            for i in range(len(node.neighbors)):
                neighborNode = node.neighbors[i].dest
                # Get the shortest distance logged for that edge
                currentEdgeDist = self.queueArray.get_shortest_dist(neighborNode)
                # Calculate what the new distance could be
                newEdgeDist = dist + node.neighbors[i].length
                # If new possible distance is less than current distance, update
                if currentEdgeDist is None or newEdgeDist < currentEdgeDist:
                    self.queueArray.insert(neighborNode, newEdgeDist, node)
            # Add to visitedNodes
            self.queueArray.addVisited(node)
            print(self.queueArray)

        t2 = time.time()
        return (t2-t1)

