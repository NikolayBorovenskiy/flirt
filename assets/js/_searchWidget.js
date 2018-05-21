'use strict';

var Search = (function() {
    return {
        init: function($widget) {
            this.$root = $widget;
            this.bindEvents();
        },
        bindEvents: function() {
            var self = this;
            self.$root
                .on('keyup', _.debounce(function() {
                    self.changeValue($(this).val());
                }, 500));
        },
        changeValue: function(val) {
            if (val.length < 3) return this.published('');
            this.published(val);
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
    };
}());


$(function() {
    var $searchWidget = $('.j-search_widget');
    if (!$searchWidget.length) return;
    Search.init($searchWidget);
});