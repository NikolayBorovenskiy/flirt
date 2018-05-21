var NotificationRouter = (function($, _) {

    return {
        $root: $('#j-total-notifications'),
        user: null,
        init: function() {
            this.$badge = this.$root.find('a > span');
            this.subscribe();
            this.$badge.hide();
        },
        subscribe: function() {
            var self = this;
            window.Socket.subscribe(function() {
                self.render(window.Socket.notifications);
            });
            window.Socket.getUserInfo(function(user) {
                self.user = user;
            });
        },
        render: function(notifications) {
            console.log(notifications);
            console.log(this.user);
            var self = this;
            var _notifications = _.reject(
                notifications,
                function(item){
                    if(item.data._type==="started-chat"){
                        return item.data.actor.email === self.user.email;
                    } else {
                        return item.data.message.author.email === self.user.email;
                    }
                });
            if (_notifications.length){
                this.$badge.text(_notifications.length).show();
            } else {
                this.$badge.hide();
            }
        },
    }

}(jQuery, _));

$(function() {
    var $totalNotifications = $('#j-total-notifications');
    if (!$totalNotifications.length) return;
    NotificationRouter.init();
});