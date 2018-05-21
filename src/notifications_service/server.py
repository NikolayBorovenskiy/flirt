import logging

from tornado.httpserver import HTTPServer
from tornado import ioloop

log = logging.getLogger('message-delivery')


def start_server(app):
    http_server = HTTPServer(app)
    http_server.listen(3000)
    log.info("Running IO loop")
    ioloop.IOLoop.instance().start()


def main():
    from notifications_service.app import MessageDeliveryApp
    start_server(MessageDeliveryApp())


if __name__ == '__main__':
    main()
