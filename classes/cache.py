from queue import Queue


class CacheItem:
    def __init__(self, vertexList, vergeList):
        self._cachedVertexList = vertexList.copy()
        self._cachedVergeList = vergeList.copy()

    def print(self):
        print('Vertexes:')
        for vertex in self._cachedVertexList:
            print('\t', vertex.pos().x(), vertex.pos().y())

        print('Verges:')
        for verge in self._cachedVergeList:
            print('\t', verge.getStartVertex().x(), verge.getStartVertex().y(),
                  ' -> ', verge.getEndVertex().x(), verge.getEndVertex().y())
        print('\n')

    def getCachedVertexList(self):
        return self._cachedVertexList

    def getCachedVergeList(self):
        return self._cachedVergeList


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
        # print('Updated cache, current size = ', self._cacheQueue.qsize())
        # for item in self._cacheQueue.queue:
        #     if item is not None:
        #         item.print()

    def clear(self):
        self._pos = -1
        self._cacheQueue.queue.clear()

    def getIncreasedState(self):
        vertexList = None
        vergeList = None

        if self._pos < self._cacheQueue.qsize() - 1:
            self._pos += 1
            vertexList = self._cacheQueue.queue[self._pos].getCachedVertexList()
            vergeList = self._cacheQueue.queue[self._pos].getCachedVergeList()
        return vertexList, vergeList

    def getDecreasedState(self):
        vertexList = None
        vergeList = None

        if self._pos > 0:
            self._pos -= 1
            vertexList = self._cacheQueue.queue[self._pos].getCachedVertexList()
            vergeList = self._cacheQueue.queue[self._pos].getCachedVergeList()
        return vertexList, vergeList
