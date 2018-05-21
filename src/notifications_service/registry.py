from collections import namedtuple

NOTIFICATION_TYPES = {}
NotificationTypeInfo = namedtuple(
    'NotificationType', [
        'send_mail', 'mail_template', 'mail_subject',
        'send_push', 'inform_admins', 'with_actor'
    ])


def register_notification_type(
        typename, mail_template=None, send_push=True, with_actor=True,
        inform_admins=True, mail_subject=None):
    if typename in NOTIFICATION_TYPES:
        raise Exception("Notification type {} already registered".format(typename))
    if (mail_template, send_push) == (None, False):
        raise Exception("Notification type is useless")
    NOTIFICATION_TYPES[typename] = NotificationTypeInfo(
        send_mail=mail_template is not None,
        send_push=send_push,
        mail_template=mail_template,
        inform_admins=inform_admins,
        mail_subject=mail_subject,
        with_actor=with_actor
    )


def get_notification_type_info(typename):
    return NOTIFICATION_TYPES[typename]
