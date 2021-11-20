from queue import Queue
from classes.graph.graph import *


class CacheItem:
    def __init__(self, graph: Graph):
        vertexList = graph.getVertexList()
        edgeList = graph.getEdgeList()

        self._cachedGraph = Graph()

    def getCachedGraph(self):
        return self._cachedGraph


class Cache:
    def __init__(self, size):
        self._size = size
        self._pos = -1
        self._cacheQueue = Queue(maxsize=self._size)

    def addState(self, cacheItem):
        if self._cacheQueue.qsize() < self._size:
            print('add new')
            self._cacheQueue.put(cacheItem)
            self._pos += 1
        else:
            print('update')
            self._cacheQueue.get()
            self._cacheQueue.put(cacheItem)
        print('pos = ', self._pos)

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
