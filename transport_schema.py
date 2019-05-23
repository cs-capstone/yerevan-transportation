import re

from db.models import Station, Transport, ConnectedStations
from graph import Graph


class TransportSchema:
    def __init__(self, db_session):
        self.transport_graph = Graph()
        self.db_session = db_session
        self.stations = db_session.query(Station).all()
        self.transports = db_session.query(Transport).all()

        self.station_dict = {s.id: s for s in self.stations}

        for s in self.stations:
            self.transport_graph.add_vertex(s.id, s)

        for s in self.stations:
            for n in s.neighbor_stations:
                self.transport_graph.add_neighbor(s.id, n.id, 1)

    def __str__(self):
        return self.transport_graph.__str__()

    def find_path(self, start_id, end_id):
        """Finds shortest path from start to end and returns the transports which pass through path.

        :param start_id: Station id from where search should start
        :param end_id: Station id we need to reach
        :returns: transports which pass through shortest path
        :rtype: list of transports
        """
        if not self.transport_graph:
            return

        start = self.station_dict.get(start_id)
        end = self.station_dict.get(end_id)

        if not start or not end:
            return

        # set best 3 parents for all nodes
        self.transport_graph.bellman_ford(start)

        best3 = {i: [] for i in range(3)}

        # find best 3 paths by traversing parents
        for i in range(3):
            end_vertex = self.transport_graph.vertices[end.id]
            path = [end_vertex.data]
            parent = end_vertex.best_3[i]
            while parent is not None:
                path.append(parent.data)
                parent = parent.best_3[i]
            best3[i] = list(reversed(path))

        result = {}

        for i in range(3):
            if len(best3[i]):
                result[i] = {
                    'path': best3[i],
                    'transport': self.get_transport_from_path(best3[i]),
                }

        return result

    def get_transport_from_path(self, path):
        """Find transports which cover the path

        :param path: list of stations
        :returns: transports
        :rtype: list of transports
        """
        if not len(path):
            return

        results = {s.id: [] for s in path}
        current_transports = path[0].transports
        for station in path:
            results[station.id] = [t for t in station.transports if t in current_transports]
            current_transports = station.transports

        return results

    def get_common_transport(self, start, end):
        """Get transports passing through both start and end

        :param start: Station
        :param end: Station
        :returns: transports
        :rtype: dict of structure {transport.id: distance}
        """
        if not isinstance(start, Station) or not isinstance(end, Station):
            return None
        # find transports which pass through both stations
        common_transport = [t for t in start.transports if t in end.transports]

        # if there are 3 paths without transfer -> return
        if len(common_transport) >= 3:
            dist = {t.id: float('inf') for t in common_transport}

            for t in common_transport:
                dist[t.id] = self.get_traveling_distance(t, start, end)

            return sorted([(value, key) for (key, value) in dist.items()])
        else:
            return self.minimize_transfers(start, end)

    def get_traveling_distance(self, transport, start, end):
        """Compute distance needed to reach to end from start using given transport

        :param transport: Transport
        :param start: Station
        :param end: Station
        :returns: distance
        :rtype: number
        """
        # if no data is loaded
        if not self.stations:
            return
        # if transport does not reach end
        if transport not in [t for t in start.transports if t in end.transports]:
            return float('inf')

        dist = 0
        current = start
        previous = current
        while True:
            for n in current.neighbor_stations:
                if transport in n.transports and n.id != previous.id:
                    previous = current
                    current = n
                    dist += ConnectedStations(previous.id, current.id).get_distance()
                    break
            if current.id == end.id:
                break

        return dist

    def get_reachable_stations_by_transport(self, station, transport):
        """get all stations which can be reached from given station by given transport

        :param transport: Transport
        :param station: Station
        :returns: stations
        :rtype: dict of structure {station.id: distance}
        """
        result = {}
        current = station
        current_dist = 0
        while current is not None:
            next_stations = filter(lambda s: transport in s.transports, current.neighbor_stations)
            not_visited = [s for s in next_stations if s.id not in result]
            next = not_visited[0] if not_visited else None
            if next:
                result[next.id] = current_dist + ConnectedStations(current.id, next.id).get_distance()
                current_dist = result[next.id]
            current = next

        return result

    def get_reachable_stations(self, station):
        """get all stations which can be used from given

        :param station: Station
        :returns: stations
        :rtype: dict of structure {transport.id: {station.id: distance}}
        """
        result = {t.id: {} for t in station.transports}
        for t in station.transports:
            result[t.id] = self.get_reachable_stations_by_transport(station, t)
        return result

    def minimize_transfers(self, start_id, end_id):
        start = self.station_dict[start_id]
        end = self.station_dict[end_id]
        mtg = MinimumTransfersGraph(self.station_dict)

        # for v in mtg:
        #     print v.id, '---->', ', '.join(map(lambda x: x.id, v.neighbors.keys()))
        path = list(mtg.graph.dijkstra(start, end))
        result = []
        for s in path:
            if type(s) is str:
                id_regex = 'station(\d+):transport(\d+)'
                match = re.match(id_regex, s)
                station_id = int(match.group(1))
                transport_id = int(match.group(2))
                result.append({
                    'station': self.station_dict[station_id],
                    'transport': filter(lambda x: x.id == transport_id, self.station_dict[station_id].transports)
                })
        return result


# Graph to find path with minimum transfers
class MinimumTransfersGraph:
    TRANSFER_COST = 1000000

    def __init__(self, stations_dict):
        graph = self.graph = Graph()

        self.init_station_transports(stations_dict, graph)

        self.init_transfers(stations_dict, graph)

        self.init_routes(stations_dict, graph)

    @staticmethod
    def init_station_transports(stations_dict, graph):
        for s_id, s in stations_dict.iteritems():
            graph.add_vertex(s.id, s.id)
            for t in s.transports:
                current_id = 'station{0}:transport{1}'.format(s_id, t.id)
                graph.add_vertex(current_id, current_id)
                graph.add_neighbor(s.id, current_id, 0.1)

    @staticmethod
    def init_transfers(stations_dict, graph):
        for s_id, station in stations_dict.iteritems():
            for t1 in station.transports:
                for t2 in station.transports:
                    if t1 != t2:
                        v1_id = 'station{0}:transport{1}'.format(s_id, t1.id)
                        v2_id = 'station{0}:transport{1}'.format(s_id, t2.id)
                        graph.add_neighbor(v1_id, v2_id, MinimumTransfersGraph.TRANSFER_COST)

    @staticmethod
    def init_routes(stations_dict, graph):
        for v_id, vertex in graph.vertices.iteritems():
            if type(v_id) is str:
                id_regex = 'station(\d+):transport(\d+)'
                match = re.match(id_regex, v_id)
                if match:
                    station_id = int(match.group(1))
                    transport_id = int(match.group(2))
                    station = stations_dict[station_id]
                    for neighbor in station.neighbor_stations:
                        if transport_id in map(lambda t: t.id, neighbor.transports):
                            graph.add_neighbor(v_id, 'station{0}:transport{1}'.format(neighbor.id, transport_id),
                                               ConnectedStations(neighbor.id, transport_id).get_distance())
