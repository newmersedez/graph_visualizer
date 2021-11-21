from queue import Queue
from classes.graph.graph import *


class CacheItem:
    def __init__(self, graph: Graph):
        vertexList = graph.getVertexList().copy()
        edgeList = graph.getEdgeList().copy()
        self._cachedGraph = Graph()

        for item in vertexList:
            self._cachedGraph.addVertex(item)

        for item in edgeList:
            self._cachedGraph.addEdge(item)

    def print(self):
        print('Cached Vertex:')
        if len(self._cachedGraph.getVertexList()) != 0:
            for item in self._cachedGraph.getVertexList():
                print(item.getName())

        print('Cached edge:')
        if len(self._cachedGraph.getEdgeList()) != 0:
            for item in self._cachedGraph.getEdgeList():
                print(item.getStartVertex().getName(), ' -> ', item.getEndVertex().getName())

        print('\n')

    def getCachedGraph(self):
        return self._cachedGraph


class Cache:
    def __init__(self, size):
        self._size = size
        self._pos = -1
        self._cacheQueue = Queue(maxsize=self._size)

    def updateCache(self, cacheItem):
        if self._cacheQueue.qsize() < self._size:
            self._cacheQueue.put(cacheItem)
            self._pos += 1
        else:
            self._cacheQueue.get()
            self._cacheQueue.put(cacheItem)

        print('\n======================================================================')
        i = 0
        for item in self._cacheQueue.queue:
            print('State = ', i)
            print(item.print())
            i += 1

    def clearAllStates(self):
        self._pos = -1
        self._cacheQueue.queue.clear()

    def getIncreasedState(self):
        graph = None
        if self._pos < self._cacheQueue.qsize() - 1:
            self._pos += 1
            graph = self._cacheQueue.queue[self._pos].getCachedGraph()
        print('pos = ', self._pos)
        return graph

    def getDecreasedState(self):
        graph = None
        if self._pos > 0:
            self._pos -= 1
            graph = self._cacheQueue.queue[self._pos].getCachedGraph()
        print('pos = ', self._pos)
        return graph
