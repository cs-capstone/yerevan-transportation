from queue import Queue
from collections import deque


# Implementation of undirected graph using adjacency list
class Vertex:
    def __init__(self, id, data):
        self.id = id
        self.best_3 = [None] * 3
        self.data = data
        self.neighbors = {}

    def add_neighbor(self, v, w=0):
        self.neighbors[v] = w

    def add_neighbors(self, neighbors, weights):
        for i, n in enumerate(neighbors):
            self.add_neighbor(n, weights[i])

    def get_neighbors(self):
        return self.neighbors.keys()

    def get_weight(self, neighbor):
        return self.neighbors[neighbor]


class Graph:
    def __init__(self):
        self.vertices = {}
        self.size = 0

    def __len__(self):
        return self.size

    def __iter__(self):
        return iter(self.vertices.values())

    def __str__(self):
        result = ''
        for v_id, v in self.vertices.iteritems():
            neighbors = '----->'
            for n in v.get_neighbors():
                neighbors += str(n.data) + ', '
            result += '{0} {1}\n'.format(v_id, neighbors)
        return result

    def add_vertex(self, key, data):
        self.size += 1
        v = Vertex(key, data)
        self.vertices[key] = v
        return v

    def add_neighbor(self, vertex_key, neighbor_key, w):
        v = self.vertices[vertex_key]
        n = self.vertices[neighbor_key]
        v.add_neighbor(n, w=w)

    # Breadth first search algorithm
    def bfs(self, src, goal_test):
        # keep track of visited vertices
        visited = {}
        q = Queue()

        # first visit src node
        q.enqueue(src)
        visited[src.data] = True

        while not q.is_empty():
            # test next node in the queue for goal
            curr = q.dequeue()
            if goal_test(curr):
                return curr
            # add unvisited neighbors to the queue
            for v in curr.get_neighbors():
                if v.data not in visited:
                    q.enqueue(v)
                    visited[v.data] = True

    # Recursive Depth first search algorithm
    def dfs(self, src, goal_test, path=[]):
        # found the goal -> stop
        if goal_test(src, path):
            return path
        # add current vertex to the path
        path += [src]
        for v in src.get_neighbors():
            # don't visit same vertex twice
            if v not in path:
                path = self.dfs(v, goal_test, path)
        return path

    # Recursively detect if graph has a cycle
    def has_cycle(self, v, parent=None, visited={}):
        # mark current as visited
        visited[v] = True

        for n in v.get_neighbors():
            # found an unvisited neighbor -> check for cycle
            if not n not in visited:
                if self.has_cycle(n, v, visited):
                    return True
            # if n is visited and is not a parent of current -> there is a cycle
            elif n != parent:
                return True

        return False

    def num_of_edges(self):
        num = 0
        for v in self:
            num += len(v.get_neighbors())
        # for an undirected graph
        return num / 2

    def bellman_ford(self, start):
        # Initialize the distance to all nodes to be infinity
        # except for the start node which is zero.
        dist1 = {}
        for v in self:
            dist1[v.data.id] = float('inf')
        dist2 = {k: v for k, v in dist1.iteritems()}
        dist3 = {k: v for k, v in dist1.iteritems()}
        dist1[start.id] = dist2[start.id] = dist3[start.id] = 0

        # For each vertex, apply relaxation for all the edges
        for i in range(len(self)):
            for vertex in self:
                for neighbor, w in vertex.neighbors.iteritems():
                    v = vertex.data.id
                    n = neighbor.data.id
                    if dist1[v] + w < dist1[n]:
                            neighbor.best_3[0] = vertex
                            dist1[n] = dist1[v] + w
                    elif dist1[n] < dist2[v] + w < dist2[n]:
                            neighbor.best_3[1] = vertex
                            dist2[n] = dist2[v] + w
                    elif dist1[n] < dist2[n] < dist3[v] + w < dist3[n]:
                            neighbor.best_3[2] = vertex
                            dist3[n] = dist3[v] + w

        return dist1, dist2, dist3

    def dijkstra(self, start, end):
        inf = float('inf')

        # Set the distance to zero for our initial node and to infinity for other nodes.
        dist = {v: inf for v in self.vertices}
        dist[start.id] = 0

        # Mark all nodes unvisited
        previous_vertices = {
            v: None for v in self.vertices
        }

        vertices = self.vertices.keys()

        while vertices:
            # Select the unvisited node with the smallest distance
            current = min(vertices, key=lambda v: dist[v])

            # if the smallest distance among the unvisited nodes is infinity.
            if dist[current] == inf:
                break

            # Find unvisited neighbors for the current node
            # and calculate their distances through the current node.
            for neighbour, cost in self.vertices[current].neighbors.iteritems():
                alternative_route = dist[current] + cost

                # Compare the newly calculated distance to the assigned
                # and save the smaller one.
                if alternative_route < dist[neighbour.id]:
                    dist[neighbour.id] = alternative_route
                    previous_vertices[neighbour.id] = current

            # Mark the current node as visited
            # and remove it from the unvisited set.
            vertices.remove(current)

        path = deque()
        candidates = [k for k in dist.keys() if type(k) is str and 'station{}'.format(end.id) in k]
        current_vertex = min(candidates, key=lambda x: dist[x])

        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
            dist[end.id] = dist[path[-1]] + 0.1
            path.append(end.id)

        return path
