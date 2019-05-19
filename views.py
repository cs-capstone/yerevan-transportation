
from pyramid.response import Response
from pyramid.view import view_config

from db.meta import DbSession
from transport_schema import TransportSchema
from db.models import Transport, Station, Street

db_session = DbSession().get_session()
transport_schema = TransportSchema(db_session)


@view_config(route_name='ping')
def ping(request):
    return Response('pong')


@view_config(route_name='streets', renderer='json')
def load_streets(request):
    return db_session.query(Street).all()


@view_config(route_name='stations', renderer='json')
def load_stations(request):
    street_id = request.params.get('street_id')
    q = db_session.query(Station)

    if street_id:
        q = q.filter(Station.street_id == street_id)

    return q.all()


@view_config(route_name='transports', renderer='json')
def load_transports(request):
    return {
        'data': db_session.query(Transport).all()
    }


@view_config(route_name='shortest_path', renderer='json')
def shortest_euclidean_distance(request):
    sid = int(request.params.get('start_id'))
    eid = int(request.params.get('end_id'))
    return transport_schema.find_path(sid, eid)


@view_config(route_name='minimum_transfers', renderer='json')
def minimum_transfers_path(request):
    sid = int(request.params.get('start_id'))
    eid = int(request.params.get('end_id'))
    return transport_schema.minimize_transfers(sid, eid)
