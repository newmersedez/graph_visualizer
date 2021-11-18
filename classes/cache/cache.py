from queue import Queue
from classes.MVP.graph import *
import copy


class CacheItem:
    def __init__(self, graph: Graph):
        vertexList = graph.getVertexList()
        vergeList = graph.getVergeList()

        graph = Graph()
        for item in vertexList:
            graph.addVertex(item)

        for item in vergeList:
            graph.addVerge(item)

        self._cachedGraph = graph

    def getCachedGraph(self):
        return self._cachedGraph


class Cache:
    def __init__(self, size):
        self._size = size
        self._pos = -1
        self._cacheQueue = Queue(maxsize=self._size)

    def addState(self, cacheItem):
        if self._cacheQueue.qsize() < self._size:
            self._cacheQueue.put(cacheItem)
            self._pos += 1
        else:
            self._cacheQueue.get()
            self._cacheQueue.put(cacheItem)

    def clearAllStates(self):
        self._pos = -1
        self._cacheQueue.queue.clear()

    def getIncreasedState(self):
        vertexList = None
        vergeList = None

        if self._pos < self._cacheQueue.qsize() - 1:
            self._pos += 1
        graph = self._cacheQueue.queue[self._pos].getCachedGraph()
        return graph

    def getDecreasedState(self):
        vertexList = None
        vergeList = None

        if self._pos > 0:
            self._pos -= 1
        graph = self._cacheQueue.queue[self._pos].getCachedGraph()
        return graph
