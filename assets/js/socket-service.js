var Socket = (function($, _, SockJS) {

    var domain = 'http://localhost',
        port = 3000,
        namespace = '/msg-listen',
        SELF_USER_INFO = '/accounts/user/self/',
        _AUTHORIZED_USER;

    return {
        socket: null,
        init: function() {
            var self = this;
            this.connect();
            this.bindEvents();
            window.Thread.subscribe(function(thread) {
                self.notifications.forEach(function(item) {
                    switch (item.data._type) {
                        case 'started-chat':
                            (thread['uuid'] === item.data.thread.uuid) && self.markNotificationAsViewed(item);
                            break;
                        case 'new-message':
                            (thread['uuid'] === item.data.thread) && self.markNotificationAsViewed(item);
                            break;
                    }
                });
            });
        },
        bindEvents: function() {
            var self = this;
            this.socket.onmessage = function(e) {
                // Get the content
                var content = JSON.parse(e.data);
                console.log(content, 'socket content');
                self.notifications.push(content);
                self.published(content);
            };

            // Open the connection
            this.socket.onopen = function() {
                self.getUserInfo(function(user) {
                    _AUTHORIZED_USER = user;
                    self.send({action: "authorization", user: user});
                });
            };

            // On connection close
            this.socket.onclose = function() {
                console.log('socket close');
                setTimeout(self.connect, 5000);
            };
        },
        getUserInfo: function(cb) {
            if (!_AUTHORIZED_USER) {
                $.get(SELF_USER_INFO, function(data) {
                    cb(data);
                });
            } else {
                cb(_AUTHORIZED_USER);
            }
        },
        markNotificationAsViewed: function(notification) {
            var url = '/messages/notifications/' + notification.data._uuid + '/mark_viewed/',
                self = this;
            $.post(url, {}, function(data) {
                self.notifications = _.reject(self.notifications, function(item){ return notification.data._uuid === item.data._uuid; });
                window.NotificationRouter.render(self.notifications);
            });
        },
        connect: function() {
            this.socket = new SockJS(domain + ':' + port + namespace);
        },
        send: function(data) {
            this.socket.send(JSON.stringify(data))
        },
        published: function(notification) {
            var self = this;
            self.subscribed.forEach(function(item) {
                item.cb.call(item.context, notification);
            });
        },
        subscribed: [],
        notifications: [],
        subscribe: function(cb, context) {
            this.subscribed.push({cb: cb, context: context});
        }
    };
}(jQuery, _, window.SockJS));

$(function() {
    Socket.init();
});
