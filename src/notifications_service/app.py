import logging

import tornadoredis
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from sockjs.tornado import SockJSConnection, SockJSRouter
from tornado import gen, web

from accounts.models import DatingUser
from core import json
from core.serializers import serialize_model
from . import conf
from .models import Notification, NotificationDelivery

log = logging.getLogger('message-delivery')


class _Dummy(object):
    pass


class MessageNotifier(SockJSConnection):

    def __init__(self, session):
        super(MessageNotifier, self).__init__(session)
        self._user = None

    def on_open(self, info):
        self._log('opened connection')
        # self.close_unauthenticated(30)

    def on_message(self, message):
        self._log('received incoming packet:', message)
        try:
            message = json.loads(message)
        except:
            self._log('JSON parse error')
            return
        if message.get('action') == 'authorization':
            user_as_dict = message.get('user')
            user = get_object_or_404(DatingUser,
                                     email=user_as_dict.get('email'))

            if not user:
                self._log('failed authentication')
                self.session.close(message='Authentication failed')
                return
            self._log('Authentication succeeded:', user)
            self._user = user
            self.app.register_connection(user, self)
            self._deliver_not_sent_notifications()
        else:
            self._log('packet type not recognized')

    @gen.coroutine
    def _deliver_not_sent_notifications(self):
        assert self._user
        yield gen.moment
        new_deliveries = NotificationDelivery.objects.filter(
            receiver=self._user, viewed_datetime=None
        ).select_related('notification').only('notification').order_by(
            '-notification__created'
        )
        for delivery in new_deliveries:
            self.deliver_notification(serialize_model(delivery.notification))
        new_deliveries.update(sent=True)

    def on_close(self):
        self._log('triggered on_close()')
        if self._user:
            self.app.unregister_connection(self._user, self)

    @gen.coroutine
    def close_unauthenticated(self, delay_sec):
        yield gen.sleep(delay_sec)
        if self._user is None:
            self._log('closing unauthenticated connection')
            self.session.close(message='Authentication token was not provided')

    @property
    def app(self):
        return self.session.server.__app__

    def deliver_message(self, message_info):
        message_to_send = message_info.build_socket_message()
        self._log('sending message to', self._user, '::', message_to_send)
        self.send(message_to_send)

    def deliver_notification(self, notification_data):
        self._log('sending notification to', self._user, '\n',
                  notification_data)
        self.send(json.dumps({
            'type': 'notification',
            'data': notification_data
        }))

    def _log(self, *message):
        message = ' '.join(map(str, message))
        log.debug('{} #{}:\n{}'.format(type(self).__name__, id(self), message))


class MessageDeliveryApp(web.Application):

    def __init__(self, default_host="", transforms=None, **settings):
        sockjs_path = settings.pop('sockjs_path', '/msg-listen')
        self.router = SockJSRouter(MessageNotifier, sockjs_path)
        self.router.__app__ = self
        super(MessageDeliveryApp, self).__init__(
            self.router.urls, default_host, transforms, **settings)
        self._registry = {}
        self._redis_client = None
        self.init_redis()
        self._authenticator = TokenAuthentication()
        self._log('initialized')

    @gen.coroutine
    def init_redis(self):
        self._redis_client = tornadoredis.Client(
            host=conf.MESSAGING_REDIS_HOST,
            port=conf.MESSAGING_REDIS_PORT,
        )
        self._redis_client.connect()

        channel = conf.MESSAGING_REDIS_CHANNEL
        yield gen.Task(self._redis_client.subscribe, channel)
        self._redis_client.listen(self.on_redis_event)
        self._log('Redis client fully initialized')

    def on_redis_event(self, message):
        if message.kind != 'message':
            return
        info = json.loads(message.body)
        if info['type'] == 'message':
            self.deliver_message(info['data'])
        elif info['type'] == 'notification':
            self.deliver_notification(info['data'])

    def deliver_message(self, data):
        self._log('got message to deliver:', data)
        info = MessageInfo.from_dict(data)
        for conn in self.get_connections(info.receiver_ids, flat=True):
            conn.deliver_message(info)

    def deliver_notification(self, data):
        notification = Notification.objects.get(id=data['id'])
        notification_data = serialize_model(notification)
        self._log('got notification to deliver:', notification_data)

        # mapping "user -> delivery"
        delivery_by_users = dict(
            NotificationDelivery.objects
                .filter(notification=notification)
                .values_list('receiver_id', 'id')
        )

        # select connections of all online users
        connection_by_users = self.get_connections(delivery_by_users.keys())

        # perform sending to receivers
        for user_id, connections in connection_by_users.items():
            for conn in connections:
                conn.deliver_notification(notification_data)

    def get_connections(self, user_ids, flat=False):
        if flat:
            return [
                conn
                for user_id in user_ids
                for conn in self._registry.get(user_id, [])
            ]
        else:
            user_ids = set(user_ids)
            conns = {
                user_id: connections
                for user_id, connections in self._registry.items()
                if user_id in user_ids
            }
            return conns

    def register_connection(self, user, connection):
        conn_lst = self._registry.setdefault(user.id, [])
        if connection not in conn_lst:
            conn_lst.append(connection)
        self._log('registered connection for', user, '::', *map(id, conn_lst))

    def unregister_connection(self, user, connection):
        conn_lst = self._registry.get(user.id)
        if conn_lst is not None:
            if connection in conn_lst:
                conn_lst.remove(connection)
            if len(conn_lst) == 0:
                del self._registry[user.id]
            self._log('connection', id(connection), 'for', user,
                      'is unregistered ::', *map(id, conn_lst))

    def perform_authentication(self, token):
        django_request = _Dummy()
        django_request.META = {
            'HTTP_AUTHORIZATION': token or ''
        }
        try:
            auth_tuple = self._authenticator.authenticate(django_request)
            if auth_tuple is not None:
                return auth_tuple[0]
        except AuthenticationFailed:
            return None

    def _log(self, *message):
        message = ' '.join(map(str, message))
        log.debug('{}:\n{}'.format(type(self).__name__, message))


class MessageInfo(object):

    def __init__(self, message_repr, thread_uuid, rcvd_time, receiver_ids):
        self.message_repr = message_repr
        self.thread_uuid = thread_uuid
        self.rcvd_time = rcvd_time
        self.receiver_ids = receiver_ids
        self._msg_cache = None

    @staticmethod
    def loads(string):
        data = json.loads(string)
        return MessageInfo.from_dict(data)

    @staticmethod
    def from_dict(dictionary):
        return MessageInfo(
            message_repr=dictionary['message_repr'],
            thread_uuid=dictionary['thread_uuid'],
            rcvd_time=dictionary['rcvd_time'],
            receiver_ids=dictionary['receiver_ids'],
        )

    def dumps(self):
        return json.dumps(self.as_dict())

    def as_dict(self):
        return {
            'message_repr': self.message_repr,
            'thread_uuid': str(self.thread_uuid),
            'rcvd_time': str(self.rcvd_time),
            'receiver_ids': self.receiver_ids,
        }

    def build_socket_message(self, force_reencode=False):
        if self._msg_cache is None or force_reencode:
            dct = self.as_dict()
            self._msg_cserver.pyache = json.dumps({
                'type': 'message',
                'data': {
                    'thread': dct['thread_uuid'],
                    'message': dct['message_repr'],
                    'received_time': dct['rcvd_time']
                }
            })
        return self._msg_cache
