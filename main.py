from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.events import NewRequest


def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
        'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Max-Age': '1728000',
        })
    event.request.add_response_callback(cors_headers)


if __name__ == '__main__':
    with Configurator() as config:

        config.add_subscriber(add_cors_headers_response_callback, NewRequest)

        # start routes

        config.add_route('ping', '/ping')
        config.add_route('streets', '/streets')
        config.add_route('stations', '/stations')
        config.add_route('transports', '/transports')
        config.add_route('shortest_path', '/shortest_path')
        config.add_route('minimum_transfers', '/minimum_transfers')

        # end routes

        config.scan('views')

        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    print 'listening to port 6543...'
    server.serve_forever()
