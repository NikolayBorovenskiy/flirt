var Messages = (function($, _) {
    var MESSAGE_URL,
        MESSAGE_TPL_URL = '/static/build/message.tpl';

    function Messages($messages) {
        if (!(this instanceof Messages)) {
            return new Messages($messages);
        }
        this.$root = $messages;
        this.$list = this.$root.find('.j-chatbody');
        this.$control = this.$root.find('.j-control');
        this.init();
    }

    var _thread = {};

    Messages.prototype = {
        constructor: Messages,
        init: function() {
            this.subscribe();
            this.bindEvents();
            this.$control.hide();
        },
        subscribe: function() {
            var self = this;
            window.Thread.subscribe(function(thread) {
                _thread = thread;
                self.makeMessageURL();
                self.showMessages();
            });
            window.Socket.subscribe(function(notification) {
                var notification_content = notification.data;
                if (notification_content._type == "new-message") {
                    if (notification_content.thread !== _thread['uuid']) {
                        window.Thread.addMessageTo(notification_content);
                    } else {
                        self.addMessageToList(notification_content.message);
                    }
                }
            });
        },
        makeMessageURL: function() {
            MESSAGE_URL = '/messages/thread/' + _thread['uuid'] + '/messages/';
        },
        bindEvents: function() {
            var self = this;
            self.$control.on('click', 'a', function() {
                self.sendMessage();
                return false;
            });
        },
        sendMessage: function() {
            var content = this.$control.find('input').val(),
                self = this;
            if (!content) return;
            $.post(MESSAGE_URL, {content: content}, function(data) {
                self.$control.find('input').val('');
                // self.addMessageToList(data);
            });
        },
        addMessageToList: function(message) {
            this.loadMessageTpl(this.renderMessage.bind(this, message));
        },
        loadMessageTpl: function(cb) {
            var self = this;
            $.get(MESSAGE_TPL_URL, function(template) {
                console.log(template);
                self.template = _.template(template);
                typeof cb == 'function' && cb();
            });
        },
        renderMessage: function(message) {
            console.log(message);
            var self = this,
                html = '';
            html += self.template(message);
            this.$list.find('.table').append(html);
        },
        showMessages: function() {
            var self = this;
            $.get(MESSAGE_URL, {}, function(data) {
                self.$list.html(data);
                self.$control.show();
            });
        },
        list: [],
        clear: function() {
            this.$list.html('');
            return this;
        }
    };

    return Messages;

}(jQuery, _));

$(function() {

    var $messages = $('#j-messages');
    if (!$messages.length) return;

    $messages.each(function() {
        new Messages($(this));
    });

});