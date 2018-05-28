import logging
import os
from tornado.httpserver import HTTPServer
from tornado import ioloop

log = logging.getLogger('message-delivery')


def _setup_env():
    import site
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dating.settings.local_settings')
    site.addsitedir(os.path.dirname(__file__))
    from django import setup
    setup()


def start_server(app):
    http_server = HTTPServer(app)
    http_server.listen(3000)
    log.info("Running IO loop")
    ioloop.IOLoop.instance().start()


def main():
    _setup_env()
    from notifications_service.app import MessageDeliveryApp
    start_server(MessageDeliveryApp())


if __name__ == '__main__':
    main()
