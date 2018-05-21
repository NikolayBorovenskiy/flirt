'use strict';

var Thread = (function($, _) {
    var THREAD_TPL_URL = '/static/build/thread.tpl';

    return {
        $root: $('#j-threads'),

        init: function() {
            var self = this;
            this.bindEvents();
            window.Socket.subscribe(function(notification) {
                var notification_content = notification.data;
                console.log(self.$root);
                if (notification_content._type !== "started-chat" || !self.$root.length)  return;
                self.addThreadToList(notification_content.thread);
            });
        },

        bindEvents: function() {
            var self = this;
            self.$root
                .on('click', 'a', function(e) {
                    var $el = $(this);
                    if (!$el.data().uuid) return;
                    self.select($el);
                    return false;
                })
        },

        select: function($el) {
            var data = _.extend({}, $el.data());
            $el.removeClass('unread').addClass('active');
            $el.siblings().each(function() {
                $(this).removeClass('active');
            });
            this.published(data);
        },
        addThreadToList: function(thread) {
            this.loadMessageTpl(this.renderThread.bind(this, thread));
        },
        addMessageTo: function(message) {
            console.log(message);
            this.markedAsUnread(message.thread);
        },
        markedAsUnread: function(thread, cb) {
            var foundExisted = false;
            this.$root.children().each(function() {
                if (!foundExisted && thread === $(this).data().uuid) {
                    foundExisted = !foundExisted;
                    $(this).addClass('unread');
                }
            });
            typeof cb === 'function' && cb(foundExisted);
        },
        renderThread: function(thread) {
            var authentificatedUser;
            window.Socket.getUserInfo(function(user) {
                authentificatedUser = user
            });
            console.log(thread);
            thread['user'] = authentificatedUser;
            var self = this,
                html = '';
            html += self.template(thread);
            this.markedAsUnread(thread.uuid, function(unread) {
                if (!unread) {
                    this.$root.append(html);
                    this.$root.children().last().addClass('unread');
                }
            })
        },
        loadMessageTpl: function(cb) {
            var self = this;
            $.get(THREAD_TPL_URL, function(template) {
                console.log(template);
                self.template = _.template(template);
                typeof cb === 'function' && cb();
            });
        },
        published: function(params) {
            var self = this;
            self.subscribed.forEach(function(item) {
                item.cb.call(item.context, params);
            });
        },

        subscribed: [],

        subscribe: function(cb, context) {
            this.subscribed.push({cb: cb, context: context});
        }

    }
}(jQuery, _));


$(function() {
    if ($('#j-threads')) {
        Thread.init();
    }
});